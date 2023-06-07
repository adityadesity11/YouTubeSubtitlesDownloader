import cv2
import os
import requests
from fpdf import FPDF
from flask import Flask,request,render_template,redirect,url_for,jsonify

API_KEY = "77a48dc1cdmshff0aa7b16b42021p1ab727jsn4cc19afa0c2b"
API_HOST = "youtube-media-downloader.p.rapidapi.com"
video_details_url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
subtitle_details_url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/subtitles"
app = Flask(__name__)

# Suppose the URL is https://www.youtube.com/watch?v=abc123 then the videoID here will be abc123.
# This function will simply extract the VideoID from the URL.
def get_video_id(videoURL):
    videoID = str(videoURL).split('/')       #create a list of substrings, where each substring is separated by the forward slash
    videoID = videoID[-1]                    #last element of the list
    if '=' in videoID:
        videoID = videoID.split('=')[-1]
    if not videoID[0].isalpha():             #if first char is not alphabet, it is removed by starting substring from 2nd char
        videoID = videoID[1:]
    print(type(videoID))
    return videoID



# This function takes the videoID and returns the subtitle URL for the video.
# This URL will show the subtitles in XML format.
def get_video_detail(videoID):
    url = video_details_url
    
    querystring = {"videoId": str(videoID)}

    headers = {
	    "X-RapidAPI-Key": "c465b2498amsh04a512c7594f9e9p19cf42jsnb6b3b1893295",
	    "X-RapidAPI-Host": "youtube-media-downloader.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    
    json_response =response.json()
    print(response)
    print(response.json())
    try:
        subtitleURL = json_response['subtitles']['items'][0]['url']
        print("Subtitle url: ",subtitleURL)
        return subtitleURL
    except:                                 
        #means that either the JSON structure does not match the expected format, or the expected keys are missing
        print('No subtitles in this video...')
        return None



# Now we will extract Text from this URL which is having subtitles in XML format.
# Takes a subtitle URL, sends a request to an API endpoint to retrieve the subtitle text, and returns the text response obtained from the API.
def get_subtitle_text(subtitleURL):
    url = subtitle_details_url
    headers = {
	"X-RapidAPI-Key": "c465b2498amsh04a512c7594f9e9p19cf42jsnb6b3b1893295",
	"X-RapidAPI-Host": "youtube-media-downloader.p.rapidapi.com"
    }
    querystring = {"subtitleUrl": subtitleURL}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text



# This function will help us put subtitle text in a PDF File and download it.
def Convert_And_Download_Subtitle(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.cell(200, 5, txt=line, ln=1)
    pdf.output("subtitle.pdf")
    print('Subtitles PDF Saved!!!')



# home() function will render home.html as our homepage.
# downloadsubs() will take the URL, extract its VideoID, extract its Subtitle URL, extract Subtitle text from the URL, put it in a PDF File, and finally save it.

@app.route('/',methods=["GET","POST"])
def home():
    subtitleURL=None
    subtitles=None
    if request.method == 'POST':
        subtitles = ""
        videoURL = request.form['yturl']
        videoID = get_video_id(videoURL)
        subtitleURL = get_video_detail(videoID)
        if subtitleURL:
            print("in")
            subtitles = get_subtitle_text(subtitleURL)
            Convert_And_Download_Subtitle(subtitles)
            print("Downloaded!")

        return render_template('home.html', url = subtitleURL, subtitletext = subtitles)
        
    return render_template('home.html')

# Note: I have removed route  '/downloads' , managed all functionalities in single route above

if __name__ == '__main__':
    app.run(debug=True)


    # Sample test links:
    # "https://www.youtube.com/watch?v=XVcRQ6T9RHo"
    # "https://www.youtube.com/watch?v=UrIaQbIK2E4"
    # "https://www.youtube.com/watch?v=HbTON0nb4DU"
