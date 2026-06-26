# -*- coding: utf-8 -*-
"""Generate Snow White Story Podcast Audio

Usage:
    export TENCENT_TTS_SECRET_ID="your-secret-id"
    export TENCENT_TTS_SECRET_KEY="your-secret-key"
    python generate_snow_white_podcast.py
"""
import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tts_podcast import main
import json

# Snow White story text
SNOW_WHITE_TEXT = '''Once upon a time, there was a beautiful queen who gave birth to a lovely princess with skin as white as snow, lips as red as blood, and hair as black as ebony. Thus, people called her Snow White.

But shortly after Snow White was born, the queen passed away. The king married a new queen, who was very beautiful, but she asked the magic mirror every day who was the fairest of them all.'''

if __name__ == "__main__":
    # Load credentials from environment variables
    secret_id = os.environ.get("TENCENT_TTS_SECRET_ID", "YOUR_SECRET_ID_HERE")
    secret_key = os.environ.get("TENCENT_TTS_SECRET_KEY", "YOUR_SECRET_KEY_HERE")
    
    result = main({
        'Text': SNOW_WHITE_TEXT,
        'VoiceType': 502006,  # Xiao Xu voice
        'secret_id': secret_id,
        'secret_key': secret_key
    })

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()
    print(f'Audio file: {result.get("AudioUrl", "")}')
    print(f'Audio file path: {os.path.abspath(result.get("AudioUrl", ""))}')
