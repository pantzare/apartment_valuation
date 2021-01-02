# Generated by Django 3.1.4 on 2021-01-02 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='title',
            new_name='rooms',
        ),
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
        migrations.AddField(
            model_name='post',
            name='size',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
