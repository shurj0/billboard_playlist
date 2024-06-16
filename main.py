import requests
import datetime
from dateutil.parser import parse, ParserError
from dateutil.relativedelta import relativedelta  

def get_dates():
    try:
        dates = requests.get("https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/valid_dates.json")
        dates.raise_for_status()
    except requests.exceptions.HTTPError:
        print("An error occured fetching the data, sorry!")
    except Exception as err:
        print("There was an error!\n {err}")
    return dates.json()

def relevant_dates(birthday, dates):
    today = datetime.date.today()
    list_of_relevant_dates = list()
    while birthday < today:
        # the min() function sorts by timedelta between birthday and date. abs() is required because of negative values,
        # we want values closest to 0.
        list_of_relevant_dates.append(min(dates, key=lambda d: abs(birthday-d) if d <= birthday else datetime.timedelta.max))
        birthday = birthday + relativedelta(years=1)
    return list_of_relevant_dates

def relevant_charts(list_of_dates):
    URL = "https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/date/"
    list_of_charts = list()
    for date in list_of_dates:
        try:
            chart = requests.get("{}{}.json".format(URL, date.isoformat()))
            list_of_charts.append(chart.json())
        except requests.exceptions.HTTPError:
            pass
    return list_of_charts

def get_songs(list_of_charts, number_of_songs):
    """ Returns a list of list [chart_date, song_tuple_list]
        song_tuple_list is a list of song_tuples, which are formatted (song title, song artist)"""
    list_of_songs = list()
    for chart in list_of_charts:
        songs = list()
        i = 0
        while i < number_of_songs:
            try:
                songs.append((chart['data'][i]['song'], chart['data'][i]['artist']))
                i += 1
            except IndexError:
                break
        year_and_songs = [chart['date'], songs]
        list_of_songs.append(year_and_songs)
    return list_of_songs

def get_birthday_songs(birthday, number_of_songs):
    list_of_parsed_dates = [ parse(date).date() for date in get_dates() ]
    list_of_songs = get_songs(relevant_charts(relevant_dates(birthday, list_of_parsed_dates)), number_of_songs)
    return list_of_songs


def main():
    birthday = None
    while not birthday:
        try:
            birthday = parse(input("Please enter your birthday (YYYY-MM-DD): ")).date()
        except ParserError:
            print("That was not a valid date! Please try again.\n")
    while True:
        try:
            number_of_songs = int(input("How many songs do you want per year?: "))
            break
        except ValueError:
            print("That is not a number! Please try again. ")
    for chart_date, songlist in get_birthday_songs(birthday, number_of_songs):
        print("{}:".format(parse(chart_date).strftime("%Y")))
        for song in songlist:
            print("\t{}".format(song))

if __name__ == "__main__":
    main()