import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

with open('./config.dict', 'rb') as config_dict:
  cred = pickle.load(config_dict)

spotify_client_id = cred['spotify_client_id']
spotify_client_secret = cred['spotify_client_secret']
token = cred['token']

client_credentials_manager = SpotifyClientCredentials(
  client_id=spotify_client_id, 
  client_secret=spotify_client_secret
  )
sp = spotipy.Spotify(
  client_credentials_manager = client_credentials_manager)
sp = spotipy.Spotify(auth = token)

df = pd.read_csv("./data/cluster_data.csv", sep = ',')

for ii in set(df['cluster']):
  cluster = df[df['cluster'] == ii]
  ids = cluster['id'].tolist()
  pl_cluster = sp.user_playlist_create('128005742', "Bot"+str(ii))
  for jj in range(1 + len(ids)//100):
    start = jj*100
    stop = min((jj+1)*100, len(ids))
    sp.user_playlist_add_tracks('128005742', pl_cluster['id'], ids[start:stop])
