#!/usr/bin/env python3

"""
voice_separation.py — 人声分离

用法:
  python <SKILL_DIR>/scripts/voice_separation.py '<json_args>'
  python <SKILL_DIR>/scripts/voice_separation.py @params.json

json_args 字段见 references/10-voice-separation.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, build_media_input, out, bail

def main():
    client, sp, args = init_and_parse()

    t     = args.get("type", "Vid")
    video = args.get("video")
    if not video:
        bail("voice_separation: video 不能为空")

    params = {
        "Input": build_media_input(t, video, sp),
        "Operation": {
            "Type": "Task",
            "Task": {
                "Type":         "AudioExtract",
                "AudioExtract": {"Voice": True},
            },
        },
    }
    out(client.submit_media(params, "voiceSeparation", sp))

if __name__ == "__main__":
    main()
