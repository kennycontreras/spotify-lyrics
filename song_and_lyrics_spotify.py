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

def sing():

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

    else:
        print("Can't get token for")

    return (song_url , (current_song['item']['duration_ms'] - current_song['progress_ms']) / 1000)


def notation(raw_song_name):

    song_notations = []
    
    # needed for a proper url extention

    # make & 'and'
    raw_song_name.replace('&' , 'and')

    # make ' fill in the gap ----------------------------------------------------------------------- # FIXME: not working can't remove the single quote
    raw_song_name.replace("'" , "")
    song_notations.append(raw_song_name)

    # make '---'  slice of what is left
    dashindexs = raw_song_name.find('---')
    song_notations.append(raw_song_name[:dashindexs + 1])

    return song_notations


def lyricsrequest(raw_names):
    
    # try different servers so you dont get blacklisted
    search_places = ['genius.com']

    for raw_name in raw_names:
        for server in search_places:
            # New request using song_url created before
            print(f"\nServer request: https://{server}/{raw_name}")
            request = requests.get(f"https://{server}/{raw_name}")

            # Verify status_code of request
            if request.status_code == 200:
                
                # BeautifulSoup library return an html code
                html_code = BeautifulSoup(request.text, features="html.parser")

                # fail safe
                if html_code.find("div", {"class": "lyrics"}) is None:
                    print('--------------------------------------making a new request because was redirected----------------------------------------------------')
                    time.sleep(2)
                    lyricsrequest([raw_name])
                    return False

                # Extract lyrics from beautifulsoup response using the correct prefix {"class": "lyrics"}
                lyrics = html_code.find("div", {"class": "lyrics"}).get_text()

                print(lyrics)
                print(f'Lyrics found on {server} with a search on {raw_name}')

                return True

            else:
                print("Sorry, I can't find the actual lyrics on this request")
    return False

if __name__ == "__main__":
    while True:
        raw_song_name , wait = sing()
        song_notations = notation(raw_song_name)
        lyricsrequest(song_notations)
        time.sleep(wait)
