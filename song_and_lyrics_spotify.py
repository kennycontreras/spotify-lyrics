import sys
import spotipy
import spotipy.util as util
import requests
from config.config import USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from bs4 import BeautifulSoup

scope = 'user-read-currently-playing'

# To connect succesfully you need to provide your own Spotify Credentials
# You can do this signing up in https://developer.spotify.com/ and creating a new app.
token = spotipy.util.prompt_for_user_token(
    USERNAME, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)


if token:
    # Create a Spotify() instance with our token
    sp = spotipy.Spotify(auth=token)
    # method currently playing return an actual song on Spotify
    current_song = sp.currently_playing()
    # Extract artist from json response
    artist = current_song['item']['artists'][0]['name']
    # Extract song name from json response
    song_name = current_song['item']['name']
    # create a valid url for web scrapping using song name and artist
    song_url = '{}-{}-lyrics'.format(str(artist).strip().replace(' ', '-'),
                                     str(song_name).strip().replace(' ', '-'))

    print('\nSong: {}\nArtist: {}'.format(song_name, artist))

    # New request using song_url created before
    request = requests.get("https://genius.com/{}".format(song_url))

    # Verify status_code of request
    if request.status_code == 200:
        # BeautifulSoup library return an html code
        html_code = BeautifulSoup(request.text, features="html.parser")
        # Extract lyrics from beautifulsoup response using the correct prefix {"class": "lyrics"}
        lyrics = html_code.find("div", {"class": "lyrics"}).get_text()
        print(lyrics)

    else:
        print("Sorry, I can't find the actual song")

else:
    print("Can't get token for", username)
