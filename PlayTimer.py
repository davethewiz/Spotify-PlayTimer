import spotipy
import spotipy.util as util
import random

scope = 'playlist-modify-public'

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

print() #skip a line for looking clean

latestPlaylist = spotifyObject.user_playlists(username)['items'][0]

newPlayListName = str(minutes) + " Minute " + playlists[playlistIndex]['name'] + " Playlist"
#replace = (latestPlaylist['name'] == newPlayListName)
#print(replace)
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
    if ('local' not in uri):  # makes sure it doesn't add any local files (URIs don't exist for them)
        totalDuration += duration
        songs.append(uri)

if len(songs) > 0:
    spotifyObject.user_playlist_add_tracks(username, latestPlaylist['id'], songs) #populate the new playlist

    #deal with overshot:
    latestPlaylistTracks = spotifyObject.user_playlist(username, latestPlaylist['id'], fields='tracks,next')['tracks']['items'] #get new playlist tracks
    overShot = totalDuration - wantedLength + 30000 #calculate playlist overshot of duration
    for track in latestPlaylistTracks: #iterate through all new playlist tracks
        duration = track['track']['duration_ms']
        uri = track['track']['uri']
        if duration < overShot and duration > overShot-30000: #if track found is shorter than the overshot but longer than 30 seconds less than the overshot
            totalDuration -= duration
            spotifyObject.user_playlist_remove_all_occurrences_of_tracks(username, latestPlaylist['id'], [uri]) #get rid of it (only one occurance)
            break
    overShot = totalDuration - wantedLength

    print(newPlayListName + " playlist successfully created! (Duration " + str(overShot/1000) + " seconds off)")