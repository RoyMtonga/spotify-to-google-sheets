import requests
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import time 
import datetime
import gspread

SPOTIPY_CLIENT_ID='5be830968d624ca1b2fc28fc11ea51f3'
SPOTIPY_CLIENT_SECRET='ffa6ef54ae034396929a879a8078e9b7'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:9090'
SCOPE='user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))

top_artists = sp.current_user_top_artists(limit=20, offset=0, time_range='short_term')

#artists
def get_artist_ids(artists):
    artist_ids = []
    for artist in artists['items']:
        artist_ids.append(artist['id'])
    return artist_ids

def get_artist_data(id):
    meta = sp.artist(id)

    name = meta['name']
    image = meta['images'][0]['url']
    spotify_url = meta['external_urls']['spotify']

    artist_info = [name, image, spotify_url]
    return artist_info

artist_ids = get_artist_ids(top_artists)
artists = []
for artist_id in artist_ids:
    time.sleep(.5)
    artist = get_artist_data(artist_id)
    artists.append(artist)

df = pd.DataFrame(artists, columns=['name', 'image', 'spotify_url'])

print(df)
