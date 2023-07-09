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
    
#create playlist
playlist_name = 'My Liked Songs - Public'

existing_playlists = sp.current_user_playlists()
existing_playlist = next((playlist for playlist in existing_playlists['items'] if playlist['name'] == playlist_name), None)

if existing_playlist: 
    playlist_id = existing_playlist['id']
    sp.playlist_replace_items(playlist_id, [track['track']['id'] for track in users_saved_tracks])
    print('Playlist updated successfully!')

else: 
    #create a new playlist
    playlist_description = 'All songs I have ever saved for the public'
    playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name, public=True, description=playlist_description)
    sp.user_playlist_add_tracks(ssfp.current_user()['id'], playlist['id'], [track['track']['id'] for track in users_saved_tracks])
    print("Created playlist succesully")
