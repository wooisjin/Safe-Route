# Generated by Django 2.2.2 on 2019-11-09 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20191109_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='dict_database',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='destination',
        ),
        migrations.DeleteModel(
            name='origin',
        ),
    ]