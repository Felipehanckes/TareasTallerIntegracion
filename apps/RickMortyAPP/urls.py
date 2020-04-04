from django.conf.urls import url
from django.urls import include, path
from .views import episode, character, index, location, searchs
from apps.RickMortyAPP.views import episode, character, index, location, searchs

app_name = 'rickmortyapp'

urlpatterns = [
    path('', index, name ='index'),
    path('episode/<int:id>', episode, name='episode'),
    path('character/<int:id>', character, name='character'),
    path('location/<int:id>', location, name='location'),
    path('searchs/', searchs, name='searchs')
]