import sys
import spotipy
import spotipy.util as util
import codecs

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print('Usage %s Username ' % (sys.argv[0],))
    sys.exit()

scope = 'user-read-currently-playing'

token = spotipy.util.prompt_for_user_token(
    username, scope, redirect_uri='http://127.0.0.1/callback')

if token:
    sp = spotipy.Spotify(auth=token)
    current_song = sp.currently_playing()
    artist = current_song['item']['artists'][0]['name']
    name_song = current_song['item']['name']
    print(artist, name_song)

else:
    print("Can't get token for", username)
