import spotipy
import spotipy.util as util
import random

scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public'

username = 'INSERT YOUR USER ID HERE'

token = util.prompt_for_user_token(
    username=username,
    scope=scope,
    client_id='INSERT YOUR CLIENT ID HERE',
    client_secret='INSERT YOUR CLIENT SECRET HERE',
    redirect_uri='https://example.com/callback/') #you can change this if you want

# Create our spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token, requests_session=True)

# User information
user = spotifyObject.current_user()
print("Hello, " + user['display_name'] + "!")
print("Welcome to the Spotify PlayTimer! Created by Dave Gershman!")
print()

playlists = spotifyObject.user_playlists(username)['items']
print("So here are your playlists: ")
for i in range(len(playlists)): #displays all your playlists in this format: "index : playlistName"
    print(str(i) + " : " + playlists[i]['name'])

playlistIndex = int(input("Enter the number that corresponds to the playlist you want: "))

minutes = int(input("How long do you want " + playlists[playlistIndex]['name'] + " to play for? "))

print()

latestPlaylist = spotifyObject.user_playlists(username)['items'][0]

newPlayListName = str(minutes) + " Minute " + playlists[playlistIndex]['name'] + " Playlist"
if (latestPlaylist['name'] != newPlayListName): #test whether or not the latest playlist has been made before
    spotifyObject.user_playlist_create(username, newPlayListName, public=True) #make one
    latestPlaylist = spotifyObject.user_playlists(username)['items'][0] #restablishes latestplaylist as the new one
    playlists = spotifyObject.user_playlists(username)['items'] #restablishes playlist including new one

    playlistTracks = spotifyObject.user_playlist(username, playlists[playlistIndex + 1]['id'], fields='tracks,next')['tracks']['items'] #selects a playlist and all of the items in it
    songs = []

    totalDuration = 0
    wantedLength = minutes * 60000  # 1min = 60,000ms

    #NOTE: adding tracks to a playlist requires that I access a track's URI

    while (totalDuration <= wantedLength):
        i = random.randint(0, len(playlistTracks) - 1)  # choose a random track index
        uri = playlistTracks[i]['track']['uri'] #set the uri to that random track index
        while (uri in songs): #if I've already used that track uri
            i = random.randint(0, len(playlistTracks) - 1)  # choose a new random track
            uri = playlistTracks[i]['track']['uri']
        duration = playlistTracks[i]['track']['duration_ms'] #get the duration of the track
        if totalDuration + duration <= wantedLength:
            if ('local' not in uri):  # makes sure it doesn't add any local files (URIs don't exist for them)
                totalDuration += duration
                songs.append(uri)
        else:
            break

    if len(songs) > 0:
        spotifyObject.user_playlist_add_tracks(username, latestPlaylist['id'], songs) #adds all songs to new playlist
        print(newPlayListName + " playlist successfully created!")
else:
    print(newPlayListName + " playlist already exists!")