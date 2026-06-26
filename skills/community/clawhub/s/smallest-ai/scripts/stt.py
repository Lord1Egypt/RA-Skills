#!/usr/bin/env python3
"""
Smallest AI STT — Speech-to-Text via Pulse model.

64ms time-to-first-token. Speaker diarization. Word timestamps. Emotion detection.

Usage:
    python3 stt.py recording.wav
    python3 stt.py meeting.mp3 --diarize --timestamps --emotions
    python3 stt.py podcast.ogg --lang hi --format text

Output: JSON transcription or plain text
"""

import argparse
import json
import os
import subprocess
import sys


CONTENT_TYPE_MAP = {
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".m4a": "audio/mp4",
    ".webm": "audio/webm",
}


def transcribe_requests(audio_path, lang, diarize, timestamps, emotions, api_key):
    """Transcribe using the requests library."""
    import requests

    ext = os.path.splitext(audio_path)[1].lower()
    content_type = CONTENT_TYPE_MAP.get(ext, "audio/wav")

    params = {
        "model": "pulse",
        "language": lang,
        "diarize": str(diarize).lower(),
        "word_timestamps": str(timestamps).lower(),
        "emotion_detection": str(emotions).lower(),
    }

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    response = requests.post(
        "https://api.smallest.ai/waves/v1/pulse/get_text",
        params=params,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
        },
        data=audio_data,
        timeout=120,
    )

    if response.status_code == 200:
        return response.json()
    else:
        error_msgs = {
            401: "Invalid or expired API key.",
            429: "Rate limited. Wait and retry.",
            413: "Audio file too large. Split into smaller segments.",
            400: f"Bad request: {response.text}",
        }
        msg = error_msgs.get(response.status_code, f"HTTP {response.status_code}: {response.text}")
        print(f"Error: {msg}", file=sys.stderr)
        return None


def transcribe_curl(audio_path, lang, diarize, timestamps, emotions, api_key):
    """Fallback transcription using curl."""
    ext = os.path.splitext(audio_path)[1].lower()
    content_type = CONTENT_TYPE_MAP.get(ext, "audio/wav")

    params = (
        f"model=pulse&language={lang}"
        f"&diarize={'true' if diarize else 'false'}"
        f"&word_timestamps={'true' if timestamps else 'false'}"
        f"&emotion_detection={'true' if emotions else 'false'}"
    )

    result = subprocess.run(
        [
            "curl", "-s",
            "--connect-timeout", "15",
            "--max-time", "120",
            "-X", "POST",
            f"https://api.smallest.ai/waves/v1/pulse/get_text?{params}",
            "-H", f"Authorization: Bearer {api_key}",
            "-H", f"Content-Type: {content_type}",
            "--data-binary", f"@{audio_path}",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0 and result.stdout.strip():
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"transcription": result.stdout.strip()}
    else:
        print(f"Error: curl failed: {result.stderr}", file=sys.stderr)
        return None


def format_output(data, fmt, diarize):
    """Format the transcription output."""
    if data is None:
        return ""

    if fmt == "text":
        if isinstance(data, dict):
            return data.get("transcription", data.get("text", json.dumps(data)))
        return str(data)

    elif fmt == "summary" and diarize:
        # Pretty-print diarized output
        lines = []
        if isinstance(data, dict):
            text = data.get("transcription", "")
            lines.append(f"Transcription: {text}\n")

            words = data.get("words", [])
            if words:
                current_speaker = None
                current_text = []
                for w in words:
                    speaker = w.get("speaker", 0)
                    if speaker != current_speaker:
                        if current_text:
                            lines.append(f"  Speaker {current_speaker}: {' '.join(current_text)}")
                        current_speaker = speaker
                        current_text = [w.get("word", "")]
                    else:
                        current_text.append(w.get("word", ""))
                if current_text:
                    lines.append(f"  Speaker {current_speaker}: {' '.join(current_text)}")
        return "\n".join(lines)

    else:
        return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Smallest AI Speech-to-Text (Pulse model)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s meeting.wav --diarize --timestamps
  %(prog)s voicenote.mp3 --lang hi --format text
  %(prog)s interview.wav --diarize --emotions --format summary

Supported formats: WAV, MP3, OGG, FLAC, M4A, WebM
Languages: en, hi, es, fr, de, ja, ko, zh, pt, ar, and 25+ more
        """,
    )
    parser.add_argument("audio", help="Path to audio file")
    parser.add_argument("--lang", default="en", help="Language code (default: en)")
    parser.add_argument("--diarize", action="store_true", help="Identify speakers")
    parser.add_argument("--timestamps", action="store_true", help="Word-level timestamps")
    parser.add_argument("--emotions", action="store_true", help="Emotion detection")
    parser.add_argument("--format", choices=["json", "text", "summary"], default="json",
                        help="Output format (default: json)")
    args = parser.parse_args()

    # Validate
    api_key = os.environ.get("SMALLEST_API_KEY")
    if not api_key:
        print("Error: Set SMALLEST_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(args.audio):
        print(f"Error: File not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    file_size = os.path.getsize(args.audio)
    if file_size > 25 * 1024 * 1024:
        print(f"Warning: Large file ({file_size // (1024*1024)}MB). May take longer.", file=sys.stderr)

    # Try transcription
    result = None

    try:
        result = transcribe_requests(
            args.audio, args.lang, args.diarize, args.timestamps, args.emotions, api_key
        )
    except ImportError:
        pass
    except Exception as e:
        print(f"HTTP error: {e}. Falling back to curl.", file=sys.stderr)

    if result is None:
        try:
            result = transcribe_curl(
                args.audio, args.lang, args.diarize, args.timestamps, args.emotions, api_key
            )
        except Exception as e:
            print(f"curl error: {e}", file=sys.stderr)
            sys.exit(1)

    if result is not None:
        output = format_output(result, args.format, args.diarize)
        print(output)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
