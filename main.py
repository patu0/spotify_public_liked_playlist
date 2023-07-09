import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

scope = 'user-library-read playlist-modify-public'

#initialize client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

#get users saved tracks list
results = sp.current_user_saved_tracks()
users_saved_tracks = results['items']

#paginate through tracks
while results['next']:
    results = sp.next(results)
    users_saved_tracks.extend(results['items'])

# batches for adding tracks
batch_size = 100

#split tracks into batches
track_batches = [users_saved_tracks[i:i+batch_size] for i in range(0, len(users_saved_tracks), batch_size)]

#create playlist
playlist_name = 'My Liked Songs - Public'

existing_playlists = sp.current_user_playlists()
existing_playlist = next((playlist for playlist in existing_playlists['items'] if playlist['name'] == playlist_name), None)

if existing_playlist: 
    playlist_id = existing_playlist['id']
    existing_tracks = sp.playlist_items(playlist_id, fields='items(track.id,total)')
    existing_track_ids = [track['track']['id'] for track in existing_tracks['items']]

else: 
    #create a new playlist
    playlist_description = 'All songs I have ever saved for the public'
    playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name, public=True, description=playlist_description)
    playlist_id = playlist['id']
    existing_track_ids = []

# Add tracks to the playlist in batches
for batch in track_batches:
    track_ids = [track['track']['id'] for track in batch if track['track']['id'] not in existing_track_ids]
    if track_ids:
        sp.playlist_add_items(playlist_id, track_ids)