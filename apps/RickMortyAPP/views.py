# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests


# Create your views here.
def index(request):
    url = 'https://rickandmortyapi.com/api/episode/'
    req = requests.get(url).json()
    context = {}
    context['results'] = req['results']
    while req['info']['next'] != '':
        req = requests.get(req['info']['next']).json()
        context['results'].extend(req['results'])
    return render(request, 'index.html', context)

def episode(request,id):
    url = 'https://rickandmortyapi.com/api/episode/' + str(id)
    context = requests.get(url).json()
    characters = context['characters']
    characters_ids = []
    characters_info = []
    for i in characters:
        characters_ids.append(int(i.split('/')[-1]))
    url2 = 'https://rickandmortyapi.com/api/character/' + str(characters_ids)
    req = requests.get(url2).json()
    for i in req:
        characters_info.append([i['name'], i['id'], i['image']])
    context['characters_info'] = characters_info
    print(context)
    return render(request, 'episode.html', context)


def character(request, id):
    url = 'https://rickandmortyapi.com/api/character/' + str(id)
    context = requests.get(url).json()
    episodes_ids = []
    episodes_names = []
    for i in context['episode']:
        episodes_ids.append(int(i.split('/')[-1]))
    url2 = 'https://rickandmortyapi.com/api/episode/' + str(episodes_ids)
    req = requests.get(url2).json()
    for i in req:
        episodes_names.append([i['name'], i['id']])
    origin_name = context['origin']['name']
    origin_id = context['origin']['url'].split('/')[-1]
    location_name = context['location']['name']
    location_id = context['location']['url'].split('/')[-1]
    context['episode_info'] = episodes_names
    context['origin_name'] = origin_name
    context['origin_id'] = origin_id
    context['location_name'] = location_name
    context['location_id'] = location_id
    print(context)
    return render(request, 'characters.html', context)

def location(request, id):
    url= 'https://rickandmortyapi.com/api/location/' + str(id)
    context = requests.get(url).json()
    characters_ids = []
    for i in context['residents']:
        characters_ids.append(int(i.split('/')[-1]))
    url2 = 'https://rickandmortyapi.com/api/character/' + str(characters_ids)
    req = requests.get(url2).json()
    characters_info = []
    for i in req:
        characters_info.append([i['id'], i['name'], i['image']])
    context['characters_info'] = characters_info
    print(context)
    return render(request, 'location.html', context)
    
def searchs(request):
    context = {}
    name = request.GET['nombre']
    urlCharacter = 'https://rickandmortyapi.com/api/character/?name=' + name
    urlLocation = 'https://rickandmortyapi.com/api/location/?name=' + name
    urlEpisode = 'https://rickandmortyapi.com/api/episode/?name=' + name
    req = requests.get(urlCharacter).json()
    print('error' in req.keys())
    if not 'error' in req.keys():
        context = {'results_character': req['results']}
        while req['info']['next'] != '':
            req = requests.get(req['info']['next']).json()
            context['results_character'].extend(req['results'])
    else:
        context = {'results_character': None}
    req = requests.get(urlLocation).json()
    if not 'error' in req.keys():
        context['results_location'] = req['results']
        while req['info']['next'] != '':
            req = requests.get(req['info']['next']).json()
            context['results_location'].extend(req['results'])
            print('\n')
        print(context['results_location'])
        print('\n')
    else:
        context['results_location'] = None
    req = requests.get(urlEpisode).json()
    print(req)
    if not 'error' in req.keys():
        context['results_episode'] = req['results']
        while req['info']['next'] != '':
            req = requests.get(req['info']['next']).json()
            context['results_episode'].extend(req['results'])
    else:
        context['results_episode'] = None
    return render(request,  'searchs.html', context)
    