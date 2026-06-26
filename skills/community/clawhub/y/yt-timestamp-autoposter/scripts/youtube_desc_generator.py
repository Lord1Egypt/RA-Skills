#!/usr/bin/env python3
"""
YouTube Timestamp Generator + Auto-Poster

Two modes:
  1. YouTube URL  — fetches transcript from the video, generates timestamps,
                    and optionally posts it back to THAT specific video.
  2. Transcript file — reads a pre-made timestamped transcript (.txt),
                       generates timestamps, and optionally posts it to your
                       LATEST YouTube upload.
"""

import re
import os
import sys
import pickle
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# ---------- YouTube Data API setup ----------
# Path configuration to look in the same directory as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, 'credentials.json')
TOKEN_PICKLE = os.path.join(SCRIPT_DIR, 'token.pickle')


def get_authenticated_service():
    """Authenticate and return the YouTube API service."""
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Credentials file '{CREDENTIALS_FILE}' not found. "
                    "Download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_PICKLE, 'wb') as token:
                pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)


def get_latest_video(youtube):
    """Return (video_id, title, current_description) of the most recent upload."""
    request = youtube.search().list(
        part='snippet',
        forMine=True,
        maxResults=1,
        order='date',
        type='video'
    )
    response = request.execute()
    if not response['items']:
        raise Exception("No videos found on your channel.")
    video = response['items'][0]
    return (
        video['id']['videoId'],
        video['snippet']['title'],
        video['snippet']['description']
    )


def get_video_details(youtube, video_id):
    """Return the title and description of a specific video by ID."""
    response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    if not response['items']:
        raise Exception(f"Video {video_id} not found.")
    snippet = response['items'][0]['snippet']
    return snippet['title'], snippet['description']


def update_video_description(youtube, video_id, new_description):
    """Replace the description of a specific video."""
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    if not video_response['items']:
        raise Exception(f"Video {video_id} not found.")
    snippet = video_response['items'][0]['snippet']
    snippet['description'] = new_description

    youtube.videos().update(
        part='snippet',
        body={
            'id': video_id,
            'snippet': snippet
        }
    ).execute()
    print(f"✅ Description updated for video {video_id}.")


# ---------- Transcript helpers ----------
def extract_video_id(url):
    """Extract YouTube video ID from various URL formats, including Shorts."""
    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/live/|youtube\.com/shorts/)([^&?/]+)",
        r"^([a-zA-Z0-9_-]{11})$"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL or video ID")


def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def fetch_transcript_from_url(video_id):
    """Fetch and format a transcript from a YouTube video ID."""
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    transcript = transcript_list.find_transcript(['en'])
    snippets = transcript.fetch()

    formatted = ""
    for snippet in snippets:
        formatted += f"{format_time(snippet.start)} {snippet.text}\n"
    return formatted


# ---------- SEO generation ----------
def generate_timestamps_only(formatted_transcript, api_key):
    """
    Generate SEO-optimized timestamps from a formatted transcript.
    Returns timestamps_text.
    """
    timestamp_prompt = f"""
Output ONLY the timestamps. Do not include any introductory sentence, heading, label, or extra text before or after the timestamps. Start your response directly with 0:00.

Create SEO-optimized YouTube timestamps from this transcript following these best practices:

Format Requirements:
- First timestamp MUST be 0:00 (YouTube's requirement for chapters)
- Use MM:SS format (or HH:MM:SS for videos over 1 hour)
- Each timestamp on a new line
- Minimum 3 timestamps (YouTube's chapter requirement)
- Each segment at least 10 seconds long
- 3 - 5 Timestamps max for a video thats 10 minutes or under
- You can go over 5 timestamps if that video is longer than 10 minutes

SEO Best Practices:
- Include primary keywords naturally in each timestamp description
- Use action-oriented, descriptive language
- Think like a viewer searching for specific information
- Make each timestamp scannable and valuable

Add SEO Suffix Keywords at the end of each timestamp line such as:
(Overview) | (Tutorial) | (Full Guide) | (BEST) | (FREE) | (2026) | (How To) | (Review) | (Tips) | (Step by Step) | (Explained) | (Comparison) | (For Beginners) | (Pro Tips) | (vs. Other Tools) | (Setup) | (Walkthrough) | (Features) | (Demo) | (Hands On)

Transcript:
{formatted_transcript}

Important Formatting Notes:
- Put the PRIMARY KEYWORD or a variation of it in the FIRST timestamp (0:00)
- Include MAJOR PRODUCT NAMES as keywords naturally (e.g., Google Flow, Veo 3.1, Nano Banana 2)
- End with a CONCLUSION or FINAL THOUGHTS timestamp
- Keep each description under 8 words for scannability
"""

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

    timestamps = model.generate_content(timestamp_prompt).text

    return timestamps


# ---------- Main ----------
def main():
    parser = argparse.ArgumentParser(
        description="Generate SEO timestamps from a YouTube URL or transcript file."
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--url',  metavar='YOUTUBE_URL',      help='YouTube video URL — fetches transcript and appends back to THAT video')
    source.add_argument('--transcript', metavar='TRANSCRIPT_TEXT',  help='Raw timestamped transcript string — appends to your LATEST video')
    source.add_argument('--latest', action='store_true', help='Process your latest video automatically and check for existing timestamps')

    parser.add_argument('gemini_api_key', help='Gemini API key')
    parser.add_argument('--post', action='store_true', help='Automatically post the generated timestamps to YouTube')
    args = parser.parse_args()

    try:
        # --- Mode 1: YouTube URL ---
        if args.url:
            video_id = extract_video_id(args.url)
            print(f"Fetching transcript for video {video_id}...")
            formatted_transcript = fetch_transcript_from_url(video_id)
            target_video_id = video_id  # post back to THIS video

        # --- Mode 2: Latest Video ---
        elif args.latest:
            print("Authenticating to fetch latest video details...")
            youtube = get_authenticated_service()
            target_video_id, title, current_desc = get_latest_video(youtube)
            print(f"Targeting latest video: {title} ({target_video_id})")
            
            # Check if timestamps already exist
            if re.search(r'\b0:00\b|\b00:00\b', current_desc):
                print(f"✅ Timestamps already exist in the description for '{title}'. Exiting.")
                sys.exit(0)
                
            print(f"Fetching transcript for latest video {target_video_id}...")
            formatted_transcript = fetch_transcript_from_url(target_video_id)

        # --- Mode 3: Raw transcript text ---
        else:
            print("Processing provided transcript text...")
            formatted_transcript = args.transcript
            target_video_id = None  # will resolve to latest video at post time

        # --- Generate SEO content ---
        print("Generating timestamps...")
        timestamps = generate_timestamps_only(
            formatted_transcript, args.gemini_api_key
        )

        print(timestamps)

        # --- Optionally post to YouTube ---
        if args.post:
            youtube = get_authenticated_service()

            if target_video_id:
                # URL mode — post to the specified video
                title, current_desc = get_video_details(youtube, target_video_id)
                print(f"\nTarget video: {title} ({target_video_id})")
            else:
                # File mode — post to latest upload
                target_video_id, title, current_desc = get_latest_video(youtube)
                print(f"\nLatest video: {title} ({target_video_id})")

            # Append timestamps to the bottom of the current description
            new_description = current_desc.strip() + f"\n\n{timestamps}"

            # Proceed directly without manual confirmation
            update_video_description(youtube, target_video_id, new_description)
            print("Done.")
        else:
            print("\n(Use --post to automatically update the YouTube video description)")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
