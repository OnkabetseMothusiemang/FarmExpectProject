# Generated by Django 4.2.16 on 2024-09-05 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase', models.CharField(max_length=200)),
                ('ai_image', models.ImageField(upload_to='ChatApp')),
            ],
        ),
    ]
