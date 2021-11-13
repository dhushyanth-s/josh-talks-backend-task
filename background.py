import signal
import requests
import json
import datetime
import sqlite3
import time

def background():
    # Crating the database and table
    con = sqlite3.connect("cicket.db")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS videos (id TEXT NOT NULL PRIMARY KEY, title TEXT, channel_id TEXT, channel_title TEXT, published_at TIMESTAMP, description TEXT, thumbnail TEXT)"
    )
    # Getting the data from the API
    api_key = "AIzaSyB8ZlLq6r15oqWCGdA_NyVgOzB7MJWKSFc"
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=cricket&type=video&maxResults=50&order=date&key={}".format(
        api_key
    )
    while True:
        response = requests.get(url)
        json_response = json.loads(response.text)
        for item in json_response["items"]:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            published_date = datetime.datetime.strptime(
                item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
            )
            thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
            channel_id = item["snippet"]["channelId"]
            channel_title = item["snippet"]["channelTitle"]
            cur.execute(
                "INSERT OR IGNORE INTO videos (id, title, channel_id, channel_title, published_at, description, thumbnail) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    video_id,
                    title,
                    channel_id,
                    channel_title,
                    published_date,
                    description,
                    thumbnail,
                ),
            )
        con.commit()
        time.sleep(10)