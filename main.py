from playlist import get_birthday_songs
from fastapi import FastAPI, HTTPException
from dateutil.parser import ParserError

app = FastAPI()

@app.get("/playlist")
async def playlist(b, s):
    try:
        playlist_json = get_birthday_songs(b, s)
    except (TypeError, ParserError):
        raise HTTPException(status_code=404, detail="Unreadable input. Please try again.")
    return playlist_json

