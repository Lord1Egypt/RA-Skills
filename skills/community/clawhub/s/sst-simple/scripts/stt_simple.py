#!/usr/bin/env python3
"""
Simple Local STT - Whisper Speech-to-Text Processor

Usage:
    /root/.openclaw/venv/stt-simple/bin/python stt_simple.py <audio_file> [model] [language] [session_id]

Example:
    python stt_simple.py voice.ogg small zh
    python stt_simple.py audio.wav base en
    python stt_simple.py audio.ogg small zh agent-main-whatsapp
"""

import sys
import os
import json
from pathlib import Path
import uuid

BASE_OUTPUT_DIR = "/root/.openclaw/workspace/stt_output"

def transcribe(audio_path: str, model: str = "small", language: str = "zh", session_id: str = None) -> dict:
    """Transcribe audio using Whisper.
    
    Args:
        audio_path: Path to audio file
        model: Whisper model (tiny/base/small/medium/large)
        language: Language code (zh/en/ja/etc.)
        session_id: Optional session/agent identifier for output isolation
    """
    import whisper
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    print(f"Loading model: {model}...", file=sys.stderr)
    whisper_model = whisper.load_model(model)
    
    print(f"Transcribing: {audio_path}", file=sys.stderr)
    result = whisper_model.transcribe(audio_path, language=language, verbose=False)
    
    # Determine output directory based on session_id
    if session_id:
        # Use session-specific subdirectory for multi-Agent isolation
        output_dir = os.path.join(BASE_OUTPUT_DIR, session_id)
    else:
        # Default shared directory
        output_dir = BASE_OUTPUT_DIR
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate unique filename with timestamp to avoid collisions
    base_name = Path(audio_path).stem
    timestamp = uuid.uuid4().hex[:8]
    output_txt = os.path.join(output_dir, f"{base_name}_{timestamp}.txt")
    
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"Output: {output_txt}", file=sys.stderr)
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python stt_simple.py <audio_file> [model] [language] [session_id]")
        print("  model: tiny, base, small, medium, large (default: small)")
        print("  language: zh, en, ja, etc. (default: zh)")
        print("  session_id: optional agent/session identifier for output isolation")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "small"
    language = sys.argv[3] if len(sys.argv) > 3 else "zh"
    session_id = sys.argv[4] if len(sys.argv) > 4 else None
    
    try:
        result = transcribe(audio_path, model, language, session_id)
        
        # Determine output file path for response
        if session_id:
            output_dir = os.path.join(BASE_OUTPUT_DIR, session_id)
        else:
            output_dir = BASE_OUTPUT_DIR
        
        output = {
            "success": True,
            "text": result["text"].strip(),
            "language": result.get("language", language),
            "duration": result.get("duration", 0),
            "session_id": session_id,
            "output_dir": output_dir,
            "output_file_pattern": f"{Path(audio_path).stem}_*.txt"
        }
        
        print(json.dumps(output, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
