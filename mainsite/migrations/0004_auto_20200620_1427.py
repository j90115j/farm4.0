# Generated by Django 3.0.7 on 2020-06-20 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0003_auto_20200620_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='thumi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('humi', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='tlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('light', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='tsoil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('soil', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ttemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('temp', models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name='Sensors',
        ),
    ]