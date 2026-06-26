#!/usr/bin/env python3
"""Fetch YouTube video transcript and output as JSON."""

import argparse
import json
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats or bare ID."""
    patterns = [
        r'(?:youtube\.com/watch\?.*v=|youtu\.be/|youtube\.com/shorts/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    # Bare video ID
    if re.fullmatch(r'[a-zA-Z0-9_-]{11}', url):
        return url
    return None


def fetch_transcript(video_id: str, langs: list[str]) -> dict:
    """Fetch transcript preferring given languages in order."""
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=langs)
    full_text = " ".join(snippet.text for snippet in transcript)
    language = transcript.language
    return {"video_id": video_id, "language": language, "transcript": full_text}


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--lang", default="it,en", help="Comma-separated preferred languages (default: it,en)")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        print(json.dumps({"error": f"Could not extract video ID from: {args.url}"}))
        sys.exit(1)

    langs = [l.strip() for l in args.lang.split(",")]

    try:
        result = fetch_transcript(video_id, langs)
    except Exception as e:
        # If preferred languages fail, try any available language
        try:
            transcript_list = YouTubeTranscriptApi().list(video_id)
            available = list(transcript_list)
            if available:
                first = available[0]
                result = fetch_transcript(video_id, [first.language_code])
            else:
                print(json.dumps({"error": f"No transcripts available for video {video_id}"}))
                sys.exit(1)
        except Exception as e2:
            error_msg = str(e2)
            if "disabled" in error_msg.lower():
                print(json.dumps({"error": f"Transcripts are disabled for video {video_id}"}))
            elif "not found" in error_msg.lower() or "unavailable" in error_msg.lower():
                print(json.dumps({"error": f"Video not found or unavailable: {video_id}"}))
            else:
                print(json.dumps({"error": f"Failed to fetch transcript: {error_msg}"}))
            sys.exit(1)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
