# Generated by Django 4.0.5 on 2022-06-05 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_questions_order_usersanswers_results'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='questions',
            unique_together={('poll', 'order')},
        ),
    ]
