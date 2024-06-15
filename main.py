import requests
import datetime
from dateutil.parser import parse, ParserError
from dateutil.relativedelta import relativedelta

def get_birthday():
    birthday = None
    while not birthday:
        try:
            birthday = parse(input("Please enter your birthday (YYYY-MM-DD):   "))
        except ParserError:
            print("That was not a valid date! Please try again.\n")
    return birthday.date()

def get_charts_and_dates():
    try:
        charts = requests.get("https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/all.json")
        dates = requests.get("https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/valid_dates.json")
        charts.raise_for_status()
        dates.raise_for_status()
    except requests.exceptions.HTTPError:
        print("An error occured fetching the data, sorry!")
    except Exception as err:
        print("There was an error!\n {err}")
    return charts.json(), dates.json()

def relevant_dates(birthday, dates):
    today = datetime.date.today()
    list_of_relevant_dates = list()
    while birthday < today:
        for date in dates:
            if date < birthday:
                prev_date = date
                continue
            elif date == birthday:
                list_of_relevant_dates.append(date)
                break
            else:
                list_of_relevant_dates.append(prev_date)
                break
        birthday = birthday + relativedelta(years=1)
    return list_of_relevant_dates



def relevant_charts(list_of_charts, birthday):
    relevant_charts_list = list()
    pass

def main():
    birthday = get_birthday()
    try:
        list_of_charts, list_of_dates = get_charts_and_dates()
    except Exception:
        exit()
    list_of_parsed_dates = [ parse(date).date() for date in list_of_dates ]
    print(relevant_dates(birthday, list_of_parsed_dates))


if __name__ == "__main__":
    main()