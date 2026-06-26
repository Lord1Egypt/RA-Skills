#!/usr/bin/env python3
"""
Simple Local STT - Whisper Speech-to-Text Processor

Usage:
    /root/.openclaw/venv/stt-simple/bin/python stt_simple.py <audio_file> [model] [language]

Example:
    python stt_simple.py voice.ogg small zh
    python stt_simple.py audio.wav base en
"""

import sys
import os
import json
from pathlib import Path

OUTPUT_DIR = "/root/.openclaw/workspace/stt_output"

def transcribe(audio_path: str, model: str = "small", language: str = "zh") -> dict:
    """Transcribe audio using Whisper."""
    import whisper
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    print(f"Loading model: {model}...", file=sys.stderr)
    whisper_model = whisper.load_model(model)
    
    print(f"Transcribing: {audio_path}", file=sys.stderr)
    result = whisper_model.transcribe(audio_path, language=language, verbose=False)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    base_name = Path(audio_path).stem
    output_txt = os.path.join(OUTPUT_DIR, f"{base_name}.txt")
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"Output: {output_txt}", file=sys.stderr)
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python stt_simple.py <audio_file> [model] [language]")
        print("  model: tiny, base, small, medium, large (default: small)")
        print("  language: zh, en, ja, etc. (default: zh)")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "small"
    language = sys.argv[3] if len(sys.argv) > 3 else "zh"
    
    try:
        result = transcribe(audio_path, model, language)
        
        output = {
            "success": True,
            "text": result["text"].strip(),
            "language": result.get("language", language),
            "duration": result.get("duration", 0),
            "output_file": os.path.join(OUTPUT_DIR, f"{Path(audio_path).stem}.txt")
        }
        
        print(json.dumps(output, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
