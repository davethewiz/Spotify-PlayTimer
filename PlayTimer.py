import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError

scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public'

username = '12155444941'#input("Enter username ID: ")

token = util.prompt_for_user_token(
    username=username,
    scope=scope,
    client_id='611a7d394d7f4c9da84e9b05058fdcca',
    client_secret='????',
    redirect_uri='https://example.com/callback/')

# Create our spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token, requests_session=True)

# User information
user = spotifyObject.current_user()
print("Hello, user " + user['display_name'] + ", you scrub.")
print("Welcome to my app! This is the first one, it's still a console thing,")
print("but hopefully I can take it further haha oh god")
print()

playlists = spotifyObject.user_playlists(username)

newPlayListName = 'API TEST'
if (playlists['items'][0]['name'] != newPlayListName):
    spotifyObject.user_playlist_create(username, newPlayListName, public=True)
    print(newPlayListName + " playlist sucessfully created!")
else:
    print(newPlayListName + " playlist already exists!")



