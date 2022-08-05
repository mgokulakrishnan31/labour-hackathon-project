# Generated by Django 4.0.6 on 2022-08-05 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DigiResume', '0003_alter_person_aadhar'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InstitutionHistory',
            new_name='InstitutionActivity',
        ),
        migrations.RenameModel(
            old_name='OrganisationHistory',
            new_name='OrganisationActivity',
        ),
        migrations.RenameModel(
            old_name='SevaHistory',
            new_name='SevaActivity',
        ),
        migrations.RemoveField(
            model_name='organisationrequest',
            name='org_code',
        ),
        migrations.RemoveField(
            model_name='organisationrequest',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='sevarequest',
            name='seva_code',
        ),
        migrations.RemoveField(
            model_name='sevarequest',
            name='uid',
        ),
        migrations.DeleteModel(
            name='InstitutionRequest',
        ),
        migrations.DeleteModel(
            name='OrganisationRequest',
        ),
        migrations.DeleteModel(
            name='SevaRequest',
        ),
    ]
