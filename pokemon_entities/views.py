import folium
import json

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
    pokemons_db = Pokemon.objects.filter()
    pokemons_entity = PokemonEntity.objects.filter()

    pokemon = []
    for pokemon_show in pokemons_db:
        if pokemon_show.id == int(pokemon_id):
            requested_pokemon = pokemon_show
            pokemon.append({'title_ru': requested_pokemon.title,
                            'img_url': request.build_absolute_uri(
                                requested_pokemon.image.url)})
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    add_pokemon(folium_map, pokemons_entity[requested_pokemon.id].lat,
                pokemons_entity[requested_pokemon.id].lon,
                request.build_absolute_uri(requested_pokemon.image.url))

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon.pop()
        })
