import psycopg2
import pandas as pd
import configparser

def connect_to_database():
    # Load configuration from config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get database configuration parameters
    host = config['Spotify']['host']
    database = config['Spotify']['database']
    user = config['Spotify']['user']
    password = config['Spotify']['password']
    port = config['Spotify']['port']

    # Establish a connection to the database
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    return conn

def create_ac_dc_spotify_table(conn):
    # Create a cursor object
    cur = conn.cursor()

    # Create ac_dc_spotify table in the database if it does not exist
    create_table = '''CREATE TABLE IF NOT EXISTS ac_dc_spotify (
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

    # Close the cursor and connection
    cur.close()
    conn.close()

# Connect to the database
connection = connect_to_database()

# Create the ac_dc_spotify table
create_ac_dc_spotify_table(connection)
