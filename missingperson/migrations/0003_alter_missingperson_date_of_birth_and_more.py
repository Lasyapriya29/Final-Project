# Generated by Django 5.0.1 on 2024-02-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missingperson', '0002_remove_missingperson_identification_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missingperson',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='missingperson',
            name='missing_from',
            field=models.DateField(blank=True, null=True),
        ),
    ]