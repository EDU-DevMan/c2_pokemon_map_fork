# Generated by Django 2.2.24 on 2025-06-18 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0010_remove_pokemon_next_evolution'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='next_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.Pokemon', verbose_name='В кого эволюционирует'),
        ),
    ]
