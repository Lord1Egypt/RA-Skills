#!/usr/bin/env python3
"""
Transcribe audio/video files using OpenAI Whisper API.
Supports batch processing and timestamp extraction.
"""

import subprocess
import requests
import json
import sys
import os
from pathlib import Path


WHISPER_ENDPOINT = "http://192.168.0.11:8080/v1/audio"


def extract_audio_from_video(video_file):
    """Extract audio from video file using ffmpeg."""
    audio_file = f"{video_file}.wav"
    
    cmd = [
        "ffmpeg", "-y", "-i", video_file,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        audio_file
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    return audio_file


def transcribe_audio(file_path, language=None, extract_timestamps=False):
    """Transcribe audio file using Whisper API."""
    
    # Extract audio from video if needed
    actual_file = file_path
    if Path(file_path).suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
        actual_file = extract_audio_from_video(file_path)
    
    # Prepare request
    with open(actual_file, 'rb') as audio:
        files = {'file': audio}
        data = {
            'model': 'whisper-small'
        }
        
        if language:
            data['language'] = language
        
        response = requests.post(
            f"{WHISPER_ENDPOINT}/transcriptions",
            files=files,
            data=data
        )
    
    result = response.json()
    
    # Clean up extracted audio
    if actual_file != file_path and os.path.exists(actual_file):
        os.remove(actual_file)
    
    return result


def transcribe_simple(file_path, language=None):
    """Quick transcription for CLI usage."""
    
    # Extract audio from video if needed
    actual_file = file_path
    if Path(file_path).suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
        actual_file = extract_audio_from_video(file_path)
    
    with open(actual_file, 'rb') as audio:
        files = {'file': audio}
        data = {'model': 'whisper-small'}
        
        if language:
            data['language'] = language
        
        response = requests.post(
            f"{WHISPER_ENDPOINT}/transcriptions",
            files=files,
            data=data
        )
    
    result = response.json()
    
    # Clean up extracted audio
    if actual_file != file_path and os.path.exists(actual_file):
        os.remove(actual_file)
    
    return result.get('text', '')
    
    result = response.json()
    
    # Clean up extracted audio
    if actual_file != file_path and os.path.exists(actual_file):
        os.remove(actual_file)
    
    return result


def transcribe_with_timestamps(file_path, language=None):
    """Transcribe with word-level timestamps."""
    
    # Extract audio from video if needed
    actual_file = file_path
    if Path(file_path).suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
        actual_file = extract_audio_from_video(file_path)
    
    data = {
        'model': 'whisper-small',
        'timestamp': 'word'
    }
    
    if language:
        data['language'] = language
    
    with open(actual_file, 'rb') as audio:
        files = {'file': audio}
        response = requests.post(
            f"{WHISPER_ENDPOINT}/transcriptions",
            files=files,
            data=data
        )
    
    result = response.json()
    
    # Clean up extracted audio
    if actual_file != file_path and os.path.exists(actual_file):
        os.remove(actual_file)
    
    return result


def batch_transcribe(file_paths, language=None):
    """Transcribe multiple files."""
    results = []
    
    for file_path in file_paths:
        try:
            result = transcribe_audio(file_path, language)
            results.append({
                'file': file_path,
                'success': True,
                'text': result.get('text', ''),
                'language': result.get('language', 'unknown')
            })
        except Exception as e:
            results.append({
                'file': file_path,
                'success': False,
                'error': str(e)
            })
    
    return results


def main():
    """CLI interface for transcription."""
    if len(sys.argv) < 2:
        print("Usage: transcribe_audio.py <file> [options]")
        print("Options:")
        print("  --language <code>  Specify language code (e.g., 'es', 'en')")
        print("  --timestamps       Include word-level timestamps")
        print("  --batch <files...> Process multiple files")
        sys.exit(1)
    
    file_path = sys.argv[1]
    language = None
    timestamps = False
    
    # Parse options
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--language' and i + 1 < len(sys.argv):
            language = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--timestamps':
            timestamps = True
            i += 1
        elif sys.argv[i] == '--batch':
            if i + 1 < len(sys.argv):
                files = sys.argv[i + 1].split(',')
                results = batch_transcribe(files, language)
                for r in results:
                    print(f"\n=== {r['file']} ===")
                    if r['success']:
                        print(r['text'])
                        print(f"Language: {r['language']}")
                    else:
                        print(f"Error: {r['error']}")
                sys.exit(0)
            i += 1
        else:
            i += 1
    
    if timestamps:
        result = transcribe_with_timestamps(file_path, language)
        print(json.dumps(result, indent=2))
    else:
        text = transcribe_simple(file_path, language)
        print(text)


if __name__ == "__main__":
    main()
