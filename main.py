import datetime as dt
from bs4 import BeautifulSoup
import requests


def ask_for_year() -> str:
    """Recursively ask user for the year to time travel back to."""

    year = input(
        'Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n')

    # Date input validation
    date_format = '%Y-%m-%d'  # YYYY-MM-DD
    try:
        dateObject = dt.datetime.strptime(year, date_format)
        # print(dateObject)
        return year
    except ValueError:
        print('Incorrect date format. Should be YYYY-MM-DD')
        ask_for_year()


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


# year = ask_for_year()
url = 'https://www.billboard.com/charts/hot-100/2000-08-12/'
response = requests.get(url)
markup = response.text
soup = BeautifulSoup(markup, 'html.parser')
top100Songs = get_top100Songs(soup)

print(top100Songs)
