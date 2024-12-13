import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import time 
import gspread
from dotenv import load_dotenv
import os

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'), client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'), redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'), scope=os.getenv('SCOPE')))

#tracks
def get_track_ids(songs):
    track_ids = []
    for song in songs['items']:
        track_ids.append(song['id'])
    return track_ids

def get_track_data(id):
    meta = sp.track(id)
    
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']

    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info

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


#insert to sheet
def insert_to_gsheet(ids, time_period, sheet):
    #create dataset
    if sheet == "songs":
        tracks = []
        for track_id in ids:
            time.sleep(.5)
            track = get_track_data(track_id)
            tracks.append(track)

        df = pd.DataFrame(tracks, columns=['name', 'album', 'artist', 'spotify_url', 'album_cover'])
    elif sheet == 'artists':
        artists = []
        for artist_id in ids:
            time.sleep(.5)
            artist = get_artist_data(artist_id)
            artists.append(artist)
        
        df = pd.DataFrame(artists, columns=['name', 'image', 'spotify_url'])
    #insert into google sheet
    gc = gspread.service_account(filename='C:/Users/roy/Desktop/spotify/grape-437111-f18ac7b19b29.json')
    sh = gc.open(sheet)
    worksheet = sh.worksheet(f'{time_period}')
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    print('done!!!')