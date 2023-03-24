import psycopg2
import pandas as pd
import configparser

# Load configuration from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Get database configuration parameters
host = config['Spotify']['host']
database = config['Spotify']['database']
user = config['Spotify']['user']
password = config['Spotify']['password']
port = config['Spotify']['port']

conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)

# Create a cursor object
cur = conn.cursor()

"""
# Create ac_dc_spotify table in the database
# Run this code once then comment it out database table is created only once!
create_table = '''CREATE TABLE ac_dc_spotify (
    danceability FLOAT,
    energy FLOAT,
    key INTEGER,
    loudness FLOAT,
    mode INTEGER,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    duration_ms TIME,
    time_signature INTEGER,
    track_name TEXT,
    album_name TEXT,
    release_date DATE
);'''

cur.execute(create_table)
conn.commit()
"""
df = pd.read_csv('acdc_spotify_data.csv')

# Insert data into the database
for index, row in df.iterrows():
    cur.execute("INSERT INTO ac_dc_spotify (danceability, energy, key, loudness, mode , speechiness, acousticness, instrumentalness, liveness, valence,tempo,duration_ms,time_signature,track_name,album_name,release_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)", (
        row['danceability'],
        row['energy'],
        row['key'],
        row['loudness'],
        row['mode'],
        row['speechiness'],
        row['acousticness'],
        row['instrumentalness'],
        row['liveness'],
        row['valence'],
        row['tempo'],
        row['duration_ms'],
        row['time_signature'],
        row['track_name'],
        row['album_name'],
        row['release_date']
    ))

conn.commit()

# Close the cursor and connection
cur.close()
conn.close()