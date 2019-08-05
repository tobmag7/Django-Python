# Generated by Django 2.1.7 on 2019-07-12 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ScrumyGoals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True)),
                ('moveable', models.BooleanField(default=True)),
                ('goal_name', models.CharField(max_length=200)),
                ('goal_id', models.CharField(max_length=200)),
                ('created_by', models.CharField(max_length=200)),
                ('moved_by', models.CharField(max_length=200)),
                ('owner', models.CharField(max_length=200)),
                ('goal_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tobmag1scrumy.GoalStatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScrumyHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moved_by', models.CharField(max_length=200)),
                ('created_by', models.CharField(max_length=200)),
                ('moved_from', models.CharField(max_length=200)),
                ('moved_to', models.CharField(max_length=200)),
                ('time_of_action', models.TimeField(verbose_name='time of action')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tobmag1scrumy.ScrumyGoals')),
            ],
        ),
    ]
