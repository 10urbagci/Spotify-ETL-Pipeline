import pandas as pd

def clean_data(file_path):
    
    df = pd.read_csv(file_path)

    # Convert release_date column to datetime format
    df['release_date'] = pd.to_datetime(df['release_date'])

    # Convert duration_ms column to milliseconds format
    df['duration_ms'] = pd.to_datetime(df['duration_ms'], unit='ms').dt.time 

    # Drop unnecessary columns
    df.drop(['type', 'id', 'uri', 'track_href', 'analysis_url', 'album_id', 'short_album_name'], axis=1, inplace=True)

    # Overwrite the original CSV file
    df.to_csv(file_path, index=False)

file_path = 'acdc_spotify_data.csv'
clean_data(file_path)
