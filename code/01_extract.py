import pickle
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import sample

with open('./config.dict', 'rb') as config_dict:
  cred = pickle.load(config_dict)

spotify_client_id = cred['spotify_client_id']
spotify_client_secret = cred['spotify_client_secret']

client_credentials_manager = SpotifyClientCredentials(
  client_id=spotify_client_id, 
  client_secret=spotify_client_secret
  )
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getPlaylistMetas(playlists):
  metas = []
  for index, row in playlists.iterrows():
    user = row['user']
    playlist_id = row['playlist_id']
    playlist = sp.user_playlist(user, playlist_id)
    nn = min(len(playlist['tracks']['items']), 50)
    for item in sample(playlist['tracks']['items'], nn):
      meta = item['track']
      meta = dict({
        'id': meta['id'],
        'name': meta['name'],
        'album': meta['album']['name'],
        'artist': meta['album']['artists'][0]['name'],
        'release_date': meta['album']['release_date'],
        'length': meta['duration_ms'],
        'popularity': meta['popularity']
      })
      metas.append(meta)
  return pd.DataFrame(metas)
  
playlists = pd.read_csv("./data_raw/playlist_ids.csv")
metas = getPlaylistMetas(playlists)
metas = metas.drop_duplicates()

track_ids = metas['id']
features = pd.DataFrame()
for ii in range(1 + len(track_ids)//100):
  start = ii*100
  stop = min(ii*100 + 100, len(track_ids))
  tracks = track_ids[start:stop]
  track_features = sp.audio_features(tracks)
  track_features = pd.DataFrame(track_features)
  features = features.append(track_features)

df = metas.set_index('id').join(features.set_index('id'))
df.to_csv("./data/track_features.csv", sep = ',')
