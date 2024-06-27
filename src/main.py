from appwrite.client import Client
import os

"""
# This is your Appwrite function
# It's executed each time we get a request
def main(context):
    # Why not try the Appwrite SDK?
    #
    # client = (
    #     Client()
    #     .set_endpoint("https://cloud.appwrite.io/v1")
    #     .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
    #     .set_key(os.environ["APPWRITE_API_KEY"])
    # )

    # You can log messages to the console
    context.log("Hello, Logs!")

    # If something goes wrong, log an error
    context.error("Hello, Errors!")

    # The `ctx.req` object contains the request data
    if context.req.method == "GET":
        # Send a response with the res object helpers
        # `ctx.res.send()` dispatches a string back to the client
        return context.res.send("Hello, World!")

    # `ctx.res.json()` is a handy helper for sending JSON
    return context.res.json(
        {
            "motto": "Build like a team of hundreds_",
            "learn": "https://appwrite.io/docs",
            "connect": "https://appwrite.io/discord",
            "getInspired": "https://builtwith.appwrite.io",
        }
    )
"""

import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_data])
        return transcript
    except Exception as e:
        return str(e)

def generate_gemini_content(transcript_text, prompt):
    api_key = os.getenv("AIzaSyBfkJtHOipUFdLt8rkY7zb6poNZSpIXFYs")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    data = {
        "prompt": prompt + transcript_text,
        "model": "gemini-pro"
    }
    response = requests.post('https://api.google.com/generativeai/gemini-pro', json=data, headers=headers)
    return response.json().get('text', 'Error generating summary')

def main(request):
    try:
        data = request.json
        youtube_link = data.get('youtubeLink')
        prompt = """You are a YouTube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words. Please provide the summary of the text given here: """
        
        transcript_text = extract_transcript_details(youtube_link)
        if "Error" in transcript_text:
            return {"error": transcript_text}
        
        summary = generate_gemini_content(transcript_text, prompt)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}
