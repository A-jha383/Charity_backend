# Generated by Django 3.1.1 on 2020-10-20 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("other_data", "0002_cqcbrand_cqclocation_cqcprovider"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cqclocation",
            name="end_date",
            field=models.DateField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Location HSCA End Date",
            ),
        ),
        migrations.AlterField(
            model_name="cqcprovider",
            name="end_date",
            field=models.DateField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Provider HSCA End Date",
            ),
        ),
    ]
