#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI runner for TopMediai TTS skill.
"""
import argparse
import json
from topmediai_tts_api import (
    get_api_key_info,
    get_all_voices,
    text_to_speech,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--action", required=True, choices=["info", "voices", "tts"])
    ap.add_argument("--text", default="")
    ap.add_argument("--speaker", default="")
    ap.add_argument("--emotion", default="")
    args = ap.parse_args()

    if args.action == "info":
        res = get_api_key_info()
        print(json.dumps(res, ensure_ascii=False))
        return

    if args.action == "voices":
        res = get_all_voices()
        print(json.dumps(res, ensure_ascii=False))
        return

    if args.action == "tts":
        if not args.text:
            raise RuntimeError("--text is required when --action tts")
        if not args.speaker:
            raise RuntimeError("--speaker is required when --action tts")
        res = text_to_speech(text=args.text, speaker=args.speaker, emotion=args.emotion or None)
        print(json.dumps(res, ensure_ascii=False))
        return


if __name__ == "__main__":
    main()
