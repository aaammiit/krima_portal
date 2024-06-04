# Generated by Django 4.2.5 on 2024-05-08 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Json', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='My_Upload_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('seg', models.CharField(max_length=100)),
                ('count', models.IntegerField(null=True)),
                ('from_date', models.CharField(max_length=100, null=True)),
                ('to_date', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]