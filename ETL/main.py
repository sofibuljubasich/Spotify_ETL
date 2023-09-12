from cfg import CLIENT_ID, SECRET,REDIRECT_URL, DB_CONNSTR
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
import pandas as pd
from models import TABLENAME
from sqlalchemy import create_engine

logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

scope = "user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret =SECRET,
                                                redirect_uri=REDIRECT_URL,
                                                scope=scope))
                            
def extract(date, limit=50):
    """Get last listen tracks

    Args:
        date (datetime): Date to query
        limit (int): Number of items to query        
    """


    date_unix = int(date.timestamp()) * 1000 #Convert date to unix format

    return sp.current_user_recently_played(limit=limit, after=date_unix)

def transform(raw_data, date):
    """Check if dataframe is empty, that all timestamps are of the parameter date
    and played_at is unique
    
    Args:
        raw_data (dataframe): Raw dataframe with recently played tracks
        date (datetime): Date to query
    
    Returns:
        dataframe: Cleaned dataframe
    """    
    song_names = []
    artist_names = []
    played_at_list = []

    for song in raw_data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "played_at" : played_at_list,
        "track" : song_names,
        "artist": artist_names
    }

    df = pd.DataFrame(song_dict, columns = ["played_at", "track", "artist"])
    
    if df.empty:
        logging.INFO("No songs dowloaded. Finishing execution")

    if df.isnull().values.any():
        logging.INFO("Null values found")
    if not df["played_at"].is_unique:
        logging.INFO("A value from played_at is not unique")
    

    return df

def load(df):

    """Load clean dataframe into the database
    
    Args:
        df (pd.DataFrame): Clean dataframe
    """
    engine = create_engine(DB_CONNSTR)
 
    try:
      
        df.to_sql(TABLENAME, con=engine, if_exists='append',index=False)
         logging.INFO("Loading complete")
    except:
        logging.ERROR("Something went wrong during the loading")
   



if __name__ == "__main__":
    
    date = datetime.now() - timedelta(days=1)
    #EXTRACT
    raw_data = extract(date)
    logging.INFO(f"Extracted {len(raw_data['items'])} registers")

    #TRANSFORM
    clean_df = transform(raw_data, date)
    
    #LOAD
    load(clean_df)
 
