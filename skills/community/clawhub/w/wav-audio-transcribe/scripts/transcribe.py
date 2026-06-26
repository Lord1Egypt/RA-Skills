#!/usr/bin/env python3
"""
Audio Transcription Script
Supports local Whisper (CLI or Python package) for offline transcription.

Usage:
    python3 transcribe.py <audio_file> [output_format] [language]
    
Examples:
    python3 transcribe.py "/path/to/audio.wav"
    python3 transcribe.py "/path/to/audio.wav" txt
    python3 transcribe.py "/path/to/audio.wav" srt zh
"""

import sys
import os
import json
import subprocess
import argparse

SUPPORTED_FORMATS = ['txt', 'srt', 'json']


def check_whisper_available():
    """Check if whisper is available (CLI or Python package)."""
    # Check CLI first
    if subprocess.run(['which', 'whisper'], capture_output=True).returncode == 0:
        return 'cli'
    
    # Check Python package
    try:
        import whisper
        return 'python'
    except ImportError:
        return None


def install_whisper():
    """Attempt to install whisper via pip."""
    print("Installing whisper...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'openai-whisper'], 
                      check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def transcribe_with_cli(audio_path, output_format='txt', language=None):
    """Transcribe using whisper CLI."""
    cmd = ['whisper', audio_path, '--model', 'base']
    
    if language:
        cmd.extend(['--language', language])
    
    if output_format == 'srt':
        cmd.append('--output_format srt')
    elif output_format == 'json':
        cmd.append('--output_format json')
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Whisper CLI error: {result.stderr}")
    
    # Find output file
    base = os.path.splitext(audio_path)[0]
    ext = 'txt' if output_format == 'txt' else output_format
    output_path = f"{base}.{ext}"
    
    with open(output_path, 'r', encoding='utf-8') as f:
        return f.read()


def transcribe_with_python(audio_path, output_format='txt', language=None):
    """Transcribe using openai-whisper Python package."""
    import whisper
    
    model = whisper.load_model('small')
    
    options = {}
    if language:
        options['language'] = language
    
    result = model.transcribe(audio_path, **options)
    
    if output_format == 'json':
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    # For txt/srt, extract segments
    text_parts = []
    for segment in result.get('segments', []):
        if output_format == 'srt':
            start = segment['start']
            end = segment['end']
            text = segment['text']
            # Format: index\nHH:MM:SS,mmm --> HH:MM:SS,mmm\ntext\n\n
            start_str = format_timestamp(start)
            end_str = format_timestamp(end)
            srt_block = f"{segment.get('id', 1) + 1}\n{start_str} --> {end_str}\n{text}\n"
            text_parts.append(srt_block)
        else:
            text_parts.append(segment['text'])
    
    return '\n'.join(text_parts)


def format_timestamp(seconds):
    """Format seconds to SRT timestamp format HH:MM:SS,mmm."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def main():
    parser = argparse.ArgumentParser(description='Audio transcription with Whisper')
    parser.add_argument('audio_file', help='Path to audio file')
    parser.add_argument('output_format', nargs='?', default='txt', 
                       choices=SUPPORTED_FORMATS, help='Output format (default: txt)')
    parser.add_argument('language', nargs='?', default=None,
                       help='Language code (e.g., zh, en, auto-detect if not specified)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.audio_file):
        print(f"Error: File not found: {args.audio_file}")
        sys.exit(1)
    
    # Check for whisper
    whisper_type = check_whisper_available()
    
    if whisper_type is None:
        print("Whisper not found. Installing...")
        if not install_whisper():
            print("Failed to install whisper. Please run: pip install openai-whisper")
            sys.exit(1)
        whisper_type = 'python'
    
    print(f"Using Whisper ({whisper_type}) to transcribe: {args.audio_file}")
    
    try:
        if whisper_type == 'cli':
            transcript = transcribe_with_cli(args.audio_file, args.output_format, args.language)
        else:
            transcript = transcribe_with_python(args.audio_file, args.output_format, args.language)
        
        # Output to file
        base = os.path.splitext(args.audio_file)[0]
        output_path = f"{base}_transcript.{args.output_format}"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        print(f"Transcription saved to: {output_path}")
        print("\n--- Transcription ---")
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        
    except Exception as e:
        print(f"Transcription failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()