# Generated by Django 3.0.6 on 2020-06-19 10:05

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ftc", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AreaOfOperation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("aootype", models.CharField(max_length=1)),
                ("aookey", models.IntegerField()),
                ("aooname", models.CharField(db_index=True, max_length=200)),
                ("aoosort", models.CharField(db_index=True, max_length=200)),
                ("welsh", models.BooleanField(verbose_name="In Wales")),
                (
                    "GSS",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=10,
                        null=True,
                        verbose_name="ONS Geocode for Local Authority",
                    ),
                ),
                (
                    "ISO3166_1",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=2,
                        null=True,
                        verbose_name="ISO3166-1 country code (2 character)",
                    ),
                ),
                (
                    "ISO3166_1_3",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=3,
                        null=True,
                        verbose_name="ISO3166-1 country code (3 character)",
                    ),
                ),
                (
                    "ISO3166_2_GB",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=6,
                        null=True,
                        verbose_name="ISO3166-2 region code (GB only)",
                    ),
                ),
                (
                    "ContinentCode",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=2,
                        null=True,
                        verbose_name="ISO3166-2 region code (GB only)",
                    ),
                ),
                (
                    "master",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="charity.AreaOfOperation",
                        verbose_name="Parent area",
                    ),
                ),
            ],
            options={
                "unique_together": {("aootype", "aookey")},
            },
        ),
        migrations.CreateModel(
            name="Vocabulary",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=200, unique=True)),
                ("single", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="VocabularyEntries",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(db_index=True, max_length=500)),
                ("title", models.CharField(db_index=True, max_length=500)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="charity.VocabularyEntries",
                    ),
                ),
                (
                    "vocabulary",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="charity.Vocabulary",
                    ),
                ),
            ],
            options={
                "unique_together": {("vocabulary", "code")},
            },
        ),
        migrations.CreateModel(
            name="CharityRaw",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("org_id", models.CharField(max_length=200)),
                ("spider", models.CharField(db_index=True, max_length=200)),
                (
                    "data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        encoder=django.core.serializers.json.DjangoJSONEncoder
                    ),
                ),
                (
                    "scrape",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ftc.Scrape"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Charity",
            fields=[
                (
                    "id",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("constitution", models.TextField(blank=True, null=True)),
                ("geographical_spread", models.TextField(blank=True, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                ("postcode", models.CharField(blank=True, max_length=200, null=True)),
                ("phone", models.CharField(blank=True, max_length=200, null=True)),
                ("active", models.BooleanField(db_index=True)),
                (
                    "date_registered",
                    models.DateField(blank=True, db_index=True, null=True),
                ),
                (
                    "date_removed",
                    models.DateField(blank=True, db_index=True, null=True),
                ),
                (
                    "removal_reason",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("web", models.URLField(blank=True, null=True)),
                ("email", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "company_number",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("activities", models.TextField(blank=True, null=True)),
                (
                    "source",
                    models.CharField(
                        blank=True, db_index=True, max_length=200, null=True
                    ),
                ),
                ("first_added", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "income",
                    models.BigIntegerField(blank=True, db_index=True, null=True),
                ),
                ("spending", models.BigIntegerField(blank=True, null=True)),
                ("latest_fye", models.DateField(blank=True, null=True)),
                ("dual_registered", models.BooleanField(blank=True, null=True)),
                (
                    "areas_of_operation",
                    models.ManyToManyField(to="charity.AreaOfOperation"),
                ),
                (
                    "classification",
                    models.ManyToManyField(to="charity.VocabularyEntries"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CharityName",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=200)),
                (
                    "normalisedName",
                    models.CharField(
                        blank=True, db_index=True, max_length=200, null=True
                    ),
                ),
                ("name_type", models.CharField(db_index=True, max_length=200)),
                (
                    "charity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="other_names",
                        to="charity.Charity",
                    ),
                ),
            ],
            options={
                "unique_together": {("charity", "name")},
            },
        ),
        migrations.CreateModel(
            name="CharityFinancial",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fyend", models.DateField(db_index=True)),
                ("fystart", models.DateField(blank=True, null=True)),
                ("income", models.BigIntegerField(blank=True, null=True)),
                ("spending", models.BigIntegerField(blank=True, null=True)),
                ("inc_leg", models.BigIntegerField(blank=True, null=True)),
                ("inc_end", models.BigIntegerField(blank=True, null=True)),
                ("inc_vol", models.BigIntegerField(blank=True, null=True)),
                ("inc_fr", models.BigIntegerField(blank=True, null=True)),
                ("inc_char", models.BigIntegerField(blank=True, null=True)),
                ("inc_invest", models.BigIntegerField(blank=True, null=True)),
                ("inc_other", models.BigIntegerField(blank=True, null=True)),
                ("inc_total", models.BigIntegerField(blank=True, null=True)),
                ("invest_gain", models.BigIntegerField(blank=True, null=True)),
                ("asset_gain", models.BigIntegerField(blank=True, null=True)),
                ("pension_gain", models.BigIntegerField(blank=True, null=True)),
                ("exp_vol", models.BigIntegerField(blank=True, null=True)),
                ("exp_trade", models.BigIntegerField(blank=True, null=True)),
                ("exp_invest", models.BigIntegerField(blank=True, null=True)),
                ("exp_grant", models.BigIntegerField(blank=True, null=True)),
                ("exp_charble", models.BigIntegerField(blank=True, null=True)),
                ("exp_gov", models.BigIntegerField(blank=True, null=True)),
                ("exp_other", models.BigIntegerField(blank=True, null=True)),
                ("exp_total", models.BigIntegerField(blank=True, null=True)),
                ("exp_support", models.BigIntegerField(blank=True, null=True)),
                ("exp_dep", models.BigIntegerField(blank=True, null=True)),
                ("reserves", models.BigIntegerField(blank=True, null=True)),
                ("asset_open", models.BigIntegerField(blank=True, null=True)),
                ("asset_close", models.BigIntegerField(blank=True, null=True)),
                ("fixed_assets", models.BigIntegerField(blank=True, null=True)),
                ("open_assets", models.BigIntegerField(blank=True, null=True)),
                ("invest_assets", models.BigIntegerField(blank=True, null=True)),
                ("cash_assets", models.BigIntegerField(blank=True, null=True)),
                ("current_assets", models.BigIntegerField(blank=True, null=True)),
                ("credit_1", models.BigIntegerField(blank=True, null=True)),
                ("credit_long", models.BigIntegerField(blank=True, null=True)),
                ("pension_assets", models.BigIntegerField(blank=True, null=True)),
                ("total_assets", models.BigIntegerField(blank=True, null=True)),
                ("funds_end", models.BigIntegerField(blank=True, null=True)),
                ("funds_restrict", models.BigIntegerField(blank=True, null=True)),
                ("funds_unrestrict", models.BigIntegerField(blank=True, null=True)),
                ("funds_total", models.BigIntegerField(blank=True, null=True)),
                ("employees", models.BigIntegerField(blank=True, null=True)),
                ("volunteers", models.BigIntegerField(blank=True, null=True)),
                (
                    "account_type",
                    models.CharField(
                        choices=[
                            ("basic", "Basic"),
                            ("consolidated", "Consolidated"),
                            ("charity", "Charity"),
                        ],
                        default="basic",
                        max_length=50,
                    ),
                ),
                (
                    "charity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="financial",
                        to="charity.Charity",
                    ),
                ),
            ],
            options={
                "unique_together": {("charity", "fyend")},
            },
        ),
    ]