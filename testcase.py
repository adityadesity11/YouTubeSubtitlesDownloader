# Just to check the smooth functioning of API

import requests

url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"

querystring = {"videoId":"G33j5Qi4rE8"}

headers = {
	"X-RapidAPI-Key": "c465b2498amsh04a512c7594f9e9p19cf42jsnb6b3b1893295",
	"X-RapidAPI-Host": "youtube-media-downloader.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())