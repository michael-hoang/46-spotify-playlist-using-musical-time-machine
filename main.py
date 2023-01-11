import datetime as dt
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from prettyprinter import pprint


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = 'playlist-modify-private'
CACHE_PATH = 'token.txt'


def ask_for_date() -> str:
    """Recursively ask user for the date to time travel back to."""

    date = input(
        'Which date do you want to travel to? Type the date in this format YYYY-MM-DD:\n')

    # Date input validation
    date_format = '%Y-%m-%d'  # YYYY-MM-DD
    try:
        dateObject = dt.datetime.strptime(date, date_format)
        # print(dateObject)
        return date
    except ValueError:
        print('Incorrect date format. Should be YYYY-MM-DD')
        ask_for_date()


def get_top100Songs(beautifulSoup_object: BeautifulSoup) -> list:
    """Get a list of top 100 songs."""

    # Get h3 tags of top 100 songs
    class_no1 = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet'
    class_no2to100 = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only'
    songs_h3_tags = soup.findAll(
        'h3', attrs={'class': [class_no1, class_no2to100]})
    # Get song titles as a string
    top100Songs = [song.getText().strip() for song in songs_h3_tags]
    return top100Songs


def authenticate_with_spotify() -> spotipy.Spotify:
    """Create Spotify API client to authenticate user and create access token."""

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,
        scope=SCOPE, cache_path=CACHE_PATH, show_dialog=True))
    return sp


date = ask_for_date()
url = f'https://www.billboard.com/charts/hot-100/{date}/'
response = requests.get(url)
markup = response.text
soup = BeautifulSoup(markup, 'html.parser')
top100Songs = get_top100Songs(soup)
sp = authenticate_with_spotify()
user_id = sp.current_user()['id']

# Get Spotify song URI
song = top100Songs[0]
query = f'track:{song} year:{date[:4]}'
result = sp.search(q=query, type='track', limit=1)
pprint(result['tracks']['items'][0]['uri'])