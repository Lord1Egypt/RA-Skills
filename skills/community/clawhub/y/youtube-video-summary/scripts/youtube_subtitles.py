#!/usr/bin/env python3
"""
YouTube Subtitles Fetcher
Fetches subtitles/captions from public YouTube videos using youtube-transcript-api.
"""

import sys
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_youtube_subtitles(video_id, language=None):
    """
    Fetch subtitles from a YouTube video.
    
    Args:
        video_id (str): YouTube video ID
        language (str): Optional language code (e.g., 'en', 'zh', 'ja')
    
    Returns:
        str: Formatted subtitle text
    
    Raises:
        Exception: If subtitles cannot be fetched
    """
    try:
        if language:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        else:
            # Get the first available transcript
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = next(transcript_list.__iter__())
            transcript = transcript.fetch()
        
        formatter = TextFormatter()
        text = formatter.format_transcript(transcript)
        return text
    
    except Exception as e:
        error_msg = f"Error fetching subtitles: {str(e)}"
        print(error_msg, file=sys.stderr)
        raise Exception(error_msg)

def get_available_languages(video_id):
    """Get list of available subtitle languages for a video."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = []
        for transcript in transcript_list:
            languages.append({
                'code': transcript.language_code,
                'name': transcript.language,
                'generated': transcript.is_generated
            })
        return languages
    except Exception as e:
        print(f"Error listing languages: {str(e)}", file=sys.stderr)
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_subtitles.py <video-id> [language-code]", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python youtube_subtitles.py dQw4w9WgXcQ", file=sys.stderr)
        print("  python youtube_subtitles.py dQw4w9WgXcQ en", file=sys.stderr)
        print("  python youtube_subtitles.py dQw4w9WgXcQ zh-Hans", file=sys.stderr)
        sys.exit(1)
    
    video_id = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else None
    
    if language == '--list':
        # List available languages
        languages = get_available_languages(video_id)
        print(json.dumps(languages, indent=2, ensure_ascii=False))
        return
    
    try:
        text = get_youtube_subtitles(video_id, language)
        print(text)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
