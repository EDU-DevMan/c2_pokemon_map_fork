import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import (Pokemon,
                                     PokemonEntity,)

from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_db = Pokemon.objects.filter()
    pokemons_entity = PokemonEntity.objects.filter()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_map in pokemons_entity:
        if pokemon_map.disappeared_at and pokemon_map.appeared_at:
            deactivated_pokemons = localtime() < pokemon_map.disappeared_at
            not_activated_pokemons = localtime() > pokemon_map.appeared_at
            if deactivated_pokemons and not_activated_pokemons:
                add_pokemon(
                    folium_map,
                    pokemon_map.lat,
                    pokemon_map.lon,
                    request.build_absolute_uri(pokemon_map.pokemon.image.url),
                    )

    pokemons_on_page = []
    for pokemon in pokemons_db:
        if pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.image.url),
                'title_ru': pokemon.title,
                })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
                })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons_db = Pokemon.objects.all()
    pokemons_entity = PokemonEntity.objects.filter(pokemon=pokemon_id,).first()

    pokemon = []
    for pokemon_show in pokemons_db:
        next_evolution = pokemon_show.next_evolution
        previous_evolution = pokemon_show.previous_evolution
        if pokemon_show.id == int(pokemon_id):
            if next_evolution.first() and previous_evolution:
                pokemon.append({
                    'title_ru': pokemon_show.title,
                    'description': pokemon_show.description,
                    'title_en': pokemon_show.title_en,
                    'title_jp': pokemon_show.title_jp,
                    'img_url': request.build_absolute_uri(
                         pokemon_show.image.url),
                    'previous_evolution': {
                        'pokemon_id': previous_evolution.id,
                        'img_url': request.build_absolute_uri(
                            previous_evolution.image.url),
                        'title_ru': previous_evolution.title
                        },
                    'next_evolution': {
                        'pokemon_id': next_evolution.first().id,
                        'img_url': request.build_absolute_uri(
                            next_evolution.first().image.url),
                        'title_ru': next_evolution.first().title
                        },
                        })

            elif previous_evolution is None:
                pokemon.append({
                    'title_ru': pokemon_show.title,
                    'description': pokemon_show.description,
                    'title_en': pokemon_show.title_en,
                    'title_jp': pokemon_show.title_jp,
                    'img_url': request.build_absolute_uri(
                        pokemon_show.image.url),
                    'next_evolution': {
                        'pokemon_id': next_evolution.first().id,
                        'img_url': request.build_absolute_uri(
                            next_evolution.first().image.url),
                        'title_ru': next_evolution.first().title
                        },
                        })

            else:
                pokemon.append({
                    'title_ru': pokemon_show.title,
                    'description': pokemon_show.description,
                    'title_en': pokemon_show.title_en,
                    'title_jp': pokemon_show.title_jp,
                    'img_url': request.build_absolute_uri(
                        pokemon_show.image.url),
                    'previous_evolution': {
                        'pokemon_id': previous_evolution.id,
                        'img_url': request.build_absolute_uri(
                            previous_evolution.image.url),
                        'title_ru': previous_evolution.title
                        },
                        })
            break

    else:

        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    add_pokemon(folium_map,
                pokemons_entity.lat,
                pokemons_entity.lon,
                request.build_absolute_uri(pokemons_entity.pokemon.image.url),
                )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon.pop()
        })
