#!/usr/bin/env python3
"""
Simple transcription script for quick use.
"""

import subprocess
import requests
import sys


WHISPER_ENDPOINT = "http://192.168.0.11:8080/v1"


def transcribe(file_path):
    """Quick transcription without options."""
    with open(file_path, 'rb') as audio:
        files = {'file': audio}
        data = {'model': 'whisper-small'}
        
        response = requests.post(
            f"{WHISPER_ENDPOINT}/transcriptions",
            files=files,
            data=data
        )
    
    result = response.json()
    return result.get('text', '')


def main():
    if len(sys.argv) < 2:
        print("Usage: transcribe_simple.py <file>")
        sys.exit(1)
    
    text = transcribe(sys.argv[1])
    print(text)


if __name__ == "__main__":
    main()
