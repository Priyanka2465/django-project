# Generated by Django 5.0.2 on 2024-03-14 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.ImageField(default='', upload_to='picture/'),
        ),
    ]
