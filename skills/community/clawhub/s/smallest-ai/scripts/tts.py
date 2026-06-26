#!/usr/bin/env python3
"""
Smallest AI TTS — Text-to-Speech via Lightning model.

Uses the smallestai SDK if installed, falls back to raw HTTP (requests/curl).
Sub-100ms latency. 30+ languages. Voice cloning support.

Usage:
    python3 tts.py "Hello world"
    python3 tts.py "Hello world" --voice arman --speed 1.2 --out greeting.wav
    python3 tts.py "नमस्ते" --voice mithali --lang hi

Output: MEDIA: <path_to_wav_file>
"""

import argparse
import json
import os
import subprocess
import sys
import time


def synthesize_sdk(text, voice, speed, rate, lang, out_path, api_key):
    """Use the official Smallest AI Python SDK."""
    from smallestai.waves import WavesClient

    client = WavesClient(api_key=api_key)
    client.synthesize(
        text=text,
        voice=voice,
        save_as=out_path,
        sample_rate=rate,
        speed=speed,
    )
    return True


def synthesize_requests(text, voice, speed, rate, lang, out_path, api_key):
    """Use the requests library for direct HTTP calls."""
    import requests

    response = requests.post(
        "https://api.smallest.ai/waves/v1/lightning-v3.1/get_speech",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "voice_id": voice,
            "sample_rate": rate,
            "speed": speed,
            "language": lang,
            "output_format": "wav",
        },
        timeout=30,
    )

    if response.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(response.content)
        return True
    else:
        error_msgs = {
            401: "Invalid or expired API key. Check SMALLEST_API_KEY.",
            429: "Rate limited. Wait a moment and try again.",
            400: f"Bad request: {response.text}",
        }
        msg = error_msgs.get(response.status_code, f"HTTP {response.status_code}: {response.text}")
        print(f"Error: {msg}", file=sys.stderr)
        return False


def synthesize_curl(text, voice, speed, rate, lang, out_path, api_key):
    """Last-resort fallback using curl subprocess."""
    payload = json.dumps({
        "text": text,
        "voice_id": voice,
        "sample_rate": rate,
        "speed": speed,
        "language": lang,
        "output_format": "wav",
    })

    result = subprocess.run(
        [
            "curl", "-s", "-o", out_path,
            "-w", "%{http_code}",
            "--connect-timeout", "10",
            "--max-time", "30",
            "-X", "POST",
            "https://api.smallest.ai/waves/v1/lightning-v3.1/get_speech",
            "-H", f"Authorization: Bearer {api_key}",
            "-H", "Content-Type: application/json",
            "-d", payload,
        ],
        capture_output=True,
        text=True,
    )

    http_code = result.stdout.strip()
    if http_code == "200":
        return True
    else:
        print(f"Error: curl returned HTTP {http_code}", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Smallest AI Text-to-Speech (Lightning model)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Good morning! Here's your briefing."
  %(prog)s "Meeting in 5 minutes" --voice arman --speed 1.3
  %(prog)s "आज का मौसम अच्छा है" --voice mithali --lang hi
  %(prog)s "Long text here" --out /tmp/narration.wav --rate 48000

Voices: sophia, robert, advika, vivaan, camilla
Languages: en, hi, es, fr, de, ja, ko, zh, pt, ar, and 20+ more
        """,
    )
    parser.add_argument("text", help="Text to convert to speech")
    parser.add_argument("--voice", default="sophia",
                        help="Voice ID (default: sophia)")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Speed 0.5-2.0 (default: 1.0)")
    parser.add_argument("--rate", type=int, default=24000,
                        help="Sample rate in Hz: 8000|16000|24000|48000 (default: 24000)")
    parser.add_argument("--lang", default="en",
                        help="Language code (default: en)")
    parser.add_argument("--out", default=None,
                        help="Output WAV file path (default: auto-named)")
    args = parser.parse_args()

    # Validate
    api_key = os.environ.get("SMALLEST_API_KEY")
    if not api_key:
        print("Error: Set SMALLEST_API_KEY environment variable.", file=sys.stderr)
        print("Get your key at https://waves.smallest.ai", file=sys.stderr)
        sys.exit(1)

    if not args.text.strip():
        print("Error: Text cannot be empty.", file=sys.stderr)
        sys.exit(1)

    if len(args.text) > 5000:
        print(f"Warning: Text is {len(args.text)} chars (limit ~5000). Consider splitting.", file=sys.stderr)

    if args.speed < 0.5 or args.speed > 2.0:
        print(f"Warning: Speed {args.speed} is outside recommended range (0.5-2.0).", file=sys.stderr)

    # Output path
    if args.out is None:
        os.makedirs("media", exist_ok=True)
        timestamp = int(time.time() * 1000)
        args.out = f"media/tts_{args.voice}_{timestamp}.wav"

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    # Try synthesis methods in order of preference
    success = False

    # Method 1: Official SDK
    try:
        success = synthesize_sdk(
            args.text, args.voice, args.speed, args.rate, args.lang, args.out, api_key
        )
    except ImportError:
        pass  # SDK not installed, try next
    except Exception as e:
        print(f"SDK error: {e}. Falling back to HTTP.", file=sys.stderr)

    # Method 2: requests library
    if not success:
        try:
            success = synthesize_requests(
                args.text, args.voice, args.speed, args.rate, args.lang, args.out, api_key
            )
        except ImportError:
            pass  # requests not installed, try next
        except Exception as e:
            print(f"HTTP error: {e}. Falling back to curl.", file=sys.stderr)

    # Method 3: curl subprocess
    if not success:
        try:
            success = synthesize_curl(
                args.text, args.voice, args.speed, args.rate, args.lang, args.out, api_key
            )
        except Exception as e:
            print(f"curl error: {e}", file=sys.stderr)
            sys.exit(1)

    if success:
        # Verify output
        if os.path.exists(args.out) and os.path.getsize(args.out) > 100:
            print(f"MEDIA: {args.out}")
        else:
            print("Error: Output file is missing or too small.", file=sys.stderr)
            sys.exit(1)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
