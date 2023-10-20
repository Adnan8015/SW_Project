# Generated by Django 4.2.4 on 2023-10-18 01:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0006_remove_profile_selected_companies_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userselectedcompany',
            options={'verbose_name': 'User Selected Company', 'verbose_name_plural': 'User Selected Companies'},
        ),
        migrations.AlterField(
            model_name='userselectedcompany',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='mainapp.companylist', verbose_name='Selected Company'),
        ),
        migrations.AlterField(
            model_name='userselectedcompany',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_companies', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddConstraint(
            model_name='userselectedcompany',
            constraint=models.UniqueConstraint(fields=('user', 'company'), name='unique_user_selected_company'),
        ),
    ]