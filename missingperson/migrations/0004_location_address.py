# Generated by Django 5.0.1 on 2024-03-08 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missingperson', '0003_alter_missingperson_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
