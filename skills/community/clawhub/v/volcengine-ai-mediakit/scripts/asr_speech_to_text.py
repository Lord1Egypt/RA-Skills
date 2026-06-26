#!/usr/bin/env python3

"""
asr_speech_to_text.py — 语音转字幕 (ASR)

用法:
  python <SKILL_DIR>/scripts/asr_speech_to_text.py '<json_args>'
  python <SKILL_DIR>/scripts/asr_speech_to_text.py @params.json

json_args 字段见 references/15-asr-speech-to-text.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, build_media_input, out, bail

def main():
    client, sp, args = init_and_parse()

    t     = args.get("type", "Vid")
    video = args.get("video")
    if not video:
        bail("asr_speech_to_text: video 不能为空")

    asr_config = {"WithSpeakerInfo": True}
    language = args.get("language")
    if language:
        asr_config["Language"] = language

    params = {
        "Input": build_media_input(t, video, sp),
        "Operation": {
            "Type": "Task",
            "Task": {
                "Type": "Asr",
                "Asr":  asr_config,
            },
        },
    }
    out(client.submit_media(params, "asr", sp))

if __name__ == "__main__":
    main()
