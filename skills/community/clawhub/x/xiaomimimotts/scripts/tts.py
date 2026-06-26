#!/usr/bin/env python3
"""MiMo TTS — generate speech audio from text via Xiaomi MiMo TTS API."""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE = "https://api.xiaomimimo.com/v1"
MODEL = "mimo-v2-tts"

VOICES = ["mimo_default", "default_zh", "default_en"]


def synthesize(text: str, voice: str, api_key: str, style: str | None = None,
               user_msg: str | None = None, fmt: str = "wav") -> bytes:
    """Call MiMo TTS API and return raw audio bytes."""
    assistant_content = text
    if style:
        assistant_content = f"<style>{style}</style>{text}"

    messages = []
    if user_msg:
        messages.append({"role": "user", "content": user_msg})
    messages.append({"role": "assistant", "content": assistant_content})

    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "audio": {"format": fmt, "voice": voice},
    }).encode()

    req = urllib.request.Request(
        f"{API_BASE}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode(errors="replace")
        print(f"API error {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)

    audio_b64 = body["choices"][0]["message"]["audio"]["data"]
    return base64.b64decode(audio_b64)


def main():
    parser = argparse.ArgumentParser(description="Generate speech via MiMo TTS")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("-o", "--output", default="output.wav",
                        help="Output file path (default: output.wav)")
    parser.add_argument("-v", "--voice", default="mimo_default", choices=VOICES,
                        help="Voice preset (default: mimo_default)")
    parser.add_argument("-s", "--style", default=None,
                        help="Style tag, e.g. '开心', '东北话', '悄悄话'")
    parser.add_argument("-f", "--format", default="wav", choices=["wav"],
                        help="Audio format (default: wav)")
    parser.add_argument("--user-msg", default=None,
                        help="Optional user-role context message")
    parser.add_argument("--api-key", default=None,
                        help="API key (or set MIMO_API_KEY env var)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("Error: provide --api-key or set MIMO_API_KEY env var", file=sys.stderr)
        sys.exit(1)

    audio = synthesize(
        text=args.text,
        voice=args.voice,
        api_key=api_key,
        style=args.style,
        user_msg=args.user_msg,
        fmt=args.format,
    )

    with open(args.output, "wb") as f:
        f.write(audio)

    print(f"Saved {len(audio)} bytes → {args.output}")


if __name__ == "__main__":
    main()
