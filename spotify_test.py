import sys
import spotipy
import spotipy.util as util
import requests
from bs4 import BeautifulSoup

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
    song_url = '{}-{}-lyrics'.format(str(artist).strip().replace(' ', '-'),
                                     str(name_song).strip().replace(' ', '-'))
    print(song_url)

    print('\nSong: {}\nArtist: {}'.format(name_song, artist))

    # Requests and BeautifulSoup code to show the lyrics of actual songs

    request = requests.get("https://genius.com/{}".format(song_url))

    # Veryfique if we found a lyric
    if request.status_code == 200:
        html_code = BeautifulSoup(request.text, features="html.parser")
        lyric = html_code.find("div", {"class": "lyrics"}).get_text()
        print(lyric)

    else:
        print("Sorry, I can't find the actual song")

else:
    print("Can't get token for", username)
