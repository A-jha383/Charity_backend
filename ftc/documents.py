import re
from itertools import groupby
from math import ceil

import tqdm
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl.search import Search
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import get_connection

from .models import Organisation, RelatedOrganisation


class SearchWithTemplate(Search):
    def execute(self, ignore_cache=False, params=None):
        """
        Execute the search and return an instance of ``Response`` wrapping all
        the data.
        :arg ignore_cache: if set to ``True``, consecutive calls will hit
            ES, while cached result will be ignored. Defaults to `False`
        """
        if ignore_cache or not hasattr(self, "_response"):
            es = get_connection(self._using)

            if params:
                search_body = es.render_search_template(
                    body={"source": self.to_dict(), "params": params},
                )["template_output"]
            else:
                search_body = self.to_dict()
            self._response = self._response_class(
                self, es.search(index=self._index, body=search_body, **self._params)
            )
        return self._response


class DSEPaginator(Paginator):
    """
    Override Django's built-in Paginator class to take in a count/total number of items;
    Elasticsearch provides the total as a part of the query results, so we can minimize hits.
    """

    def __init__(self, *args, params=None, **kwargs):
        super(DSEPaginator, self).__init__(*args, **kwargs)
        self._params = params
        self.count = None
        self.num_pages = None

    def validate_number(self, number):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_("That page number is not an integer"))
        if number < 1:
            raise EmptyPage(_("That page number is less than 1"))
        return number

    def page(self, number):
        """Return a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        return self._get_page(self.object_list[bottom:top], number, self)

    def _get_page(self, object_list, number, paginator):
        self.result = object_list.execute(params=self._params)
        if isinstance(self.result.hits.total, int):
            self.count = self.result.hits.total
        else:
            self.count = int(self.result.hits.total.value)

        if self.count == 0 and not self.allow_empty_first_page:
            return 0
        hits = max(1, self.count - self.orphans)
        self.num_pages = ceil(hits / self.per_page)
        return Page(self.result, number, self)


@registry.register_document
class FullOrganisation(Document):

    org_id = fields.KeywordField()
    complete_names = fields.CompletionField(
        contexts=[
            {"name": "organisationType", "type": "category", "path": "organisationType"}
        ]
    )
    orgIDs = fields.KeywordField()
    ids = fields.KeywordField()
    alternateName = fields.TextField()
    sortname = fields.KeywordField()
    organisationType = fields.KeywordField()
    organisationTypePrimary = fields.KeywordField()
    source = fields.KeywordField()
    domain = fields.KeywordField()
    location = fields.KeywordField()
    latestIncome = fields.IntegerField()

    @classmethod
    def search(cls, using=None, index=None):
        return SearchWithTemplate(
            using=cls._get_using(using),
            index=cls._default_index(index),
            doc_type=[cls],
            model=cls.django.model,
        )

    class Index:
        # Name of the Elasticsearch index
        name = "ftc_organisation"
        # See Elasticsearch Indices API reference for available settings
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    def prepare_complete_names(self, instance):
        words = set()
        for n in instance.alternateName + [instance.name]:
            if n:
                w = n.split()
                words.update([" ".join(w[r:]) for r in range(len(w))])
        return list(words)

    def _prepare_action(self, object_instance, action):
        result = super(FullOrganisation, self)._prepare_action(object_instance, action)
        result["_id"] = object_instance.org_id
        return result

    def prepare_orgIDs(self, instance):
        return instance.orgIDs

    def prepare_ids(self, instance):
        return [o.id for o in instance.orgIDs]

    def prepare_alternateName(self, instance):
        return instance.alternateName

    def prepare_sortname(self, instance):
        n = re.sub("[^0-9a-zA-Z ]+", "", instance.name.lower().strip())
        if n.startswith("the "):
            n = n[4:]
        n = re.sub(" +", " ", n).strip()
        return n

    def prepare_organisationType(self, instance):
        return list(instance.get_all("organisationType"))

    def prepare_organisationTypePrimary(self, instance):
        return instance.organisationTypePrimary_id

    def prepare_domain(self, instance):
        return instance.domain

    def prepare_location(self, instance):
        return instance.allGeoCodes

    def prepare_latestIncome(self, instance):
        return instance.latestIncome

    def prepare_source(self, instance):
        return list(instance.get_all("source_id"))

    def prepare_org_id(self, instance):
        return str(instance.org_id)

    def get_queryset(self):
        """
        Return the queryset that should be indexed by this doc type.
        """
        return self.django.model.objects.filter(linked_orgs__isnull=False).order_by(
            "linked_orgs"
        )

    def get_indexing_queryset(self):
        """
        Build queryset (iterator) for use by indexing.
        """
        qs = self.get_queryset()
        for k, orgs in groupby(
            tqdm.tqdm(
                qs.iterator(), total=qs.count(), position=0, smoothing=0.1, leave=True
            ),
            key=lambda o: o.linked_orgs,
        ):
            yield RelatedOrganisation(orgs)

    def bulk(self, actions, **kwargs):
        if self.django.queryset_pagination and "chunk_size" not in kwargs:
            kwargs["chunk_size"] = self.django.queryset_pagination
        return bulk(client=self._get_connection(), actions=actions, **kwargs)

    class Django:
        model = Organisation  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            "name",
            "postalCode",
            "dateModified",
            "active",
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        queryset_pagination = 3000

    def get_related_orgs(self):
        return Organisation.objects.filter(org_id__in=self.orgIDs)
