import requests
from dotenv import load_dotenv
import os
import pandas as pd

def extract_spotify_data():
    load_dotenv()

    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # Convert JSON
    auth_response_data = auth_response.json()

    # Save the access token
    access_token = auth_response_data['access_token']

    # The authorization process was done with the bearer token.
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    # Base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    # Track ID from the URI
    track_id = '6y0igZArWVi6Iz0rj35c1Y'

    # Actual GET request with proper header
    r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

    r = r.json()


    # AC/DC URL -> Copy from Spotify. You can click ... and copy link
    artist_id = '711MCceyCBcFnzjGY4Q7Un'

    # Pull all artist's albums
    r = requests.get(BASE_URL + 'artists/' + artist_id + '/albums', 
                     headers=headers, 
                     params={'include_groups': 'album', 'limit': 50})
    d = r.json()

    data = []   # Will hold all track info
    albums = [] # To keep track of duplicates

    # Loop over albums and get all tracks
    for album in d['items']:
        album_name = album['name']

        # Print albums before 2020
        trim_name = album_name.split('(')[0].strip()
        if trim_name.upper() in albums or int(album['release_date'][:4]) > 2020:
            continue
        albums.append(trim_name.upper()) 

        print(album_name)

        # Pull all tracks from this album
        r = requests.get(BASE_URL + 'albums/' + album['id'] + '/tracks', 
            headers=headers)
        tracks = r.json()['items']

        for track in tracks:
            # Get audio features (key, liveness, danceability, ...)
            f = requests.get(BASE_URL + 'audio-features/' + track['id'], 
                headers=headers)
            f = f.json()

            # Combine with album info
            f.update({
                'track_name': track['name'],
                'album_name': album_name,
                'short_album_name': trim_name,
                'release_date': album['release_date'],
                'album_id': album['id']
            })

            data.append(f)

    # Convert JSON data to a Pandas DataFrame
    df = pd.json_normalize(data)

    # Save to CSV file
    df.to_csv('acdc_spotify_data.csv', index=False)

extract_spotify_data()