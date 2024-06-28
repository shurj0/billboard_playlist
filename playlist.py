import requests
import datetime
from dateutil.parser import parse, ParserError
from dateutil.relativedelta import relativedelta  
import asyncio
import aiohttp

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

def get_relevent_charts_tasks(session, list_of_dates):
    URL = "https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/date/"
    tasks = []
    for date in list_of_dates:
        tasks.append(session.get("{}{}.json".format(URL, date.isoformat())))
    return tasks

async def relevant_charts(list_of_dates):
    async with aiohttp.ClientSession() as session:
        tasks = get_relevent_charts_tasks(session, list_of_dates)
        responses = await asyncio.gather(*tasks)
    list_of_charts = [ await response.json(content_type=None) for response in responses ]
    return list_of_charts
"""    for date in list_of_dates:
        try:
            chart = requests.get("{}{}.json".format(URL, date.isoformat()))
            list_of_charts.append(chart.json())
        except requests.exceptions.HTTPError:
            pass"""

async def get_songs(chart_list, number_of_songs):
    dict_of_songs = dict()
    list_of_charts = await chart_list
    for chart in list_of_charts:
        songs = dict()
        i = 0
        while i < number_of_songs:
            try:
                songs[i+1] = {"title": chart['data'][i]['song'], "artist": chart['data'][i]['artist']}
                i += 1
            except IndexError:
                break
        #year_and_songs = [chart['date'], songs]
        dict_of_songs[chart['date']] = songs
    return dict_of_songs

async def get_birthday_songs(birthday, number_of_songs):
    birthday = parse(birthday).date()
    number_of_songs = int(number_of_songs)
    list_of_parsed_dates = [ parse(date).date() for date in get_dates() ]
    dict_of_songs = await get_songs(relevant_charts(relevant_dates(birthday, list_of_parsed_dates)), number_of_songs)
    return dict_of_songs

async def main():
    birthday = input("Please enter your birthday (YYYY-MM-DD): ")
    number_of_songs = input("How many songs do you want per year?: ")
    dict_of_songs = await get_birthday_songs(birthday, number_of_songs)
    print(dict_of_songs)
"""    for chart_date, songlist in get_birthday_songs(birthday, number_of_songs):
        print("{}:".format(parse(chart_date).strftime("%Y")))
        for song in songlist:
            print("\t{}".format(song))
    print(get_birthday_songs(birthday, number_of_songs))"""

if __name__ == "__main__":
    asyncio.run(main())