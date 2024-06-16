import requests
from dateutil.parser import parse

URL = "http://127.0.0.1:8000/playlist?"

def get_response(b, s):
    response = requests.get(URL + "b={}&s={}".format(b, s))
    return response

def main():
    while True:
        try:
            birthday = input("Please enter your birthday (YYYY-MM-DD): ")
            number_of_songs = input("How many songs do you want per year?: ")
            response = get_response(birthday, number_of_songs)
            response.raise_for_status()
            break
        except Exception:
            print("Invalid input, please try again")
    response = response.json()
    for year, chart_dict in response.items():
        print(parse(year).strftime("%Y"), end=":")
        for rank, song_dict in chart_dict.items():
            if len(chart_dict) < 2:
                rankstr = ""
            else:
                rankstr = rank + ": "
            print("\t{}{} by {}".format(rankstr, song_dict["title"], song_dict["artist"]))

if __name__ == "__main__":
    main()