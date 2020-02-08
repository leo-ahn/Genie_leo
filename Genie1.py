import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbGenie

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

songs = soup.select('#body-content > newesttable > tbody > tr')

rank = 1
for song in songs:
    title = song.select_one('td.info > a.title')
    artist = song.select_one('td.info > a.artist')
    print(rank, title, artist)

    doc = {
        'rank': rank,
        'title': title,
        'artist': artist
    }
    db.songs.insert_one(doc)
    rank += 1
