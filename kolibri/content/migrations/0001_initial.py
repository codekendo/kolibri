# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-27 16:07
from __future__ import unicode_literals

import uuid

import django.db.models.deletion
import django.db.models.manager
import kolibri.content.models
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('author', models.CharField(blank=True, max_length=400, null=True)),
                ('theme', models.CharField(blank=True, max_length=400, null=True)),
                ('subscribed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContentCopyTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referenced_count', models.IntegerField(blank=True, null=True)),
                ('content_copy_id', models.CharField(max_length=400, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('kind', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=100)),
                ('total_file_size', models.IntegerField()),
                ('available', models.BooleanField(default=False)),
                ('sort_order', models.FloatField(blank=True, null=True)),
                ('license_owner', models.CharField(blank=True, max_length=200, null=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'verbose_name': 'Content Metadata',
            },
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checksum', models.CharField(blank=True, max_length=400, null=True)),
                ('extension', models.CharField(blank=True, max_length=100, null=True)),
                ('available', models.BooleanField(default=False)),
                ('file_size', models.IntegerField(blank=True, null=True)),
                ('content_copy', models.FileField(blank=True, max_length=200, storage=kolibri.content.models.ContentCopyStorage(), upload_to=kolibri.content.models.content_copy_name)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=False)),
                ('format_size', models.IntegerField(blank=True, null=True)),
                ('quality', models.CharField(blank=True, max_length=50, null=True)),
                ('contentmetadata', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='formats', to='content.ContentMetadata')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MimeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('readable_name', models.CharField(max_length=50)),
                ('machine_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrerequisiteContentRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contentmetadata_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_prerequisitecontentrelationship_1', to='content.ContentMetadata')),
                ('contentmetadata_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_prerequisitecontentrelationship_2', to='content.ContentMetadata')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedContentRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contentmetadata_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_relatedcontentrelationship_1', to='content.ContentMetadata')),
                ('contentmetadata_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_relatedcontentrelationship_2', to='content.ContentMetadata')),
            ],
        ),
        migrations.AddField(
            model_name='format',
            name='mimetype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.MimeType'),
        ),
        migrations.AddField(
            model_name='file',
            name='format',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='content.Format'),
        ),
        migrations.AddField(
            model_name='contentmetadata',
            name='is_related',
            field=models.ManyToManyField(blank=True, related_name='relate_to', through='content.RelatedContentRelationship', to='content.ContentMetadata'),
        ),
        migrations.AddField(
            model_name='contentmetadata',
            name='license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.License'),
        ),
        migrations.AddField(
            model_name='contentmetadata',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='content.ContentMetadata'),
        ),
        migrations.AddField(
            model_name='contentmetadata',
            name='prerequisite',
            field=models.ManyToManyField(blank=True, related_name='is_prerequisite_of', through='content.PrerequisiteContentRelationship', to='content.ContentMetadata'),
        ),
        migrations.AlterUniqueTogether(
            name='relatedcontentrelationship',
            unique_together=set([('contentmetadata_1', 'contentmetadata_2')]),
        ),
        migrations.AlterUniqueTogether(
            name='prerequisitecontentrelationship',
            unique_together=set([('contentmetadata_1', 'contentmetadata_2')]),
        ),
    ]
