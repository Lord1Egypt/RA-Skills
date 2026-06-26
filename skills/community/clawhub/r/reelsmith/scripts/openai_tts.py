#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from openai import OpenAI

VOICE_PRESETS = {
    'default': 'alloy',
    'calm': 'alloy',
    'professional': 'verse',
    'energetic': 'ash',
    'confident': 'sage',
    'broadcast': 'ash',
}


def main():
    ap = argparse.ArgumentParser(description='Generate narration audio with OpenAI TTS')
    ap.add_argument('--text', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--voice', default=None)
    ap.add_argument('--style', default='default', choices=list(VOICE_PRESETS.keys()))
    ap.add_argument('--model', default='gpt-4o-mini-tts')
    args = ap.parse_args()

    chosen_voice = args.voice or VOICE_PRESETS.get(args.style, 'alloy')
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    speech = client.audio.speech.create(
        model=args.model,
        voice=chosen_voice,
        input=args.text,
    )
    out = Path(args.output)
    out.write_bytes(speech.read())
    print(str(out))


if __name__ == '__main__':
    main()
