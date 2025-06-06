# Generated by Django 5.2.1 on 2025-05-30 12:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('units_required', models.PositiveIntegerField(default=1)),
                ('units_committed', models.PositiveIntegerField(default=0)),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('fulfilled', 'Fulfilled'), ('cancelled', 'Cancelled')], default='open', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('needed_by', models.DateField(blank=True, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DonationAcceptance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted_at', models.DateTimeField(auto_now_add=True)),
                ('units_committed', models.PositiveIntegerField(default=1)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations_accepted', to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acceptances', to='bloodrequest.bloodrequest')),
            ],
            options={
                'unique_together': {('request', 'donor')},
            },
        ),
    ]
