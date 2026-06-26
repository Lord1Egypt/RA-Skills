#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Snow White Story Podcast
Using VoiceType: 502006 (Xiao Xu)

Usage:
    export TENCENT_TTS_SECRET_ID="your-secret-id"
    export TENCENT_TTS_SECRET_KEY="your-secret-key"
    python generate_snow_white.py
"""

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tts_podcast import main

# Snow White story text
SNOW_WHITE_STORY = """Once upon a time, there was a beautiful queen who gave birth to a lovely princess with skin as white as snow, lips as red as blood, and hair as black as ebony. Thus, people called her Snow White.

But shortly after Snow White was born, the queen passed away. The king married a new queen, who was very beautiful, but she asked the magic mirror every day who was the fairest of them all."""


def main_generate():
    """Main function: Generate voice podcast"""
    # Load credentials from environment variables
    secret_id = os.environ.get("TENCENT_TTS_SECRET_ID", "YOUR_SECRET_ID_HERE")
    secret_key = os.environ.get("TENCENT_TTS_SECRET_KEY", "YOUR_SECRET_KEY_HERE")
    
    print("Starting Snow White story podcast generation...")
    print(f"Story length: {len(SNOW_WHITE_STORY)} characters")
    print(f"Using voice: Xiao Xu (VoiceType: 502006)")
    
    result = main({
        "Text": SNOW_WHITE_STORY,
        "VoiceType": 502006,  # Xiao Xu voice
        "secret_id": secret_id,
        "secret_key": secret_key
    })
    
    print("\nGeneration result:")
    print(f"Code: {result.get('Code', 'N/A')}")
    print(f"Msg: {result.get('Msg', 'N/A')}")
    print(f"Filename: {result.get('filename', 'N/A')}")
    print(f"Duration: {result.get('duration', 'N/A')} minutes")
    
    if result.get('Code') == 0:
        print(f"\n✅ Podcast generated successfully!")
        print(f"Audio file: {result.get('filename')}")
    else:
        print(f"\n❌ Podcast generation failed: {result.get('Msg')}")


if __name__ == "__main__":
    main_generate()
