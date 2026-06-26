#!/usr/bin/env python3

"""
interlacing.py — 智能补帧

用法:
  python <SKILL_DIR>/scripts/interlacing.py '<json_args>'
  python <SKILL_DIR>/scripts/interlacing.py @params.json

json_args 字段见 references/14-interlacing.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, build_media_input, out, bail

def main():
    client, sp, args = init_and_parse()

    t     = args.get("type", "Vid")
    video = args.get("video")
    if not video:
        bail("interlacing: video 不能为空")
    fps   = args.get("Fps")
    if fps is None:
        bail("interlacing: Fps 为必填参数")
    fps = float(fps)
    if not (0 < fps <= 120):
        bail("interlacing: Fps 必须在 (0, 120] 范围内")

    params = {
        "Input": build_media_input(t, video, sp),
        "Operation": {
            "Type": "Task",
            "Task": {
                "Type":    "Enhance",
                "Enhance": {
                    "Type": "Moe",
                    "MoeEnhance": {
                        "Config":        "common",
                        "Target":        {"Fps": fps},
                        "VideoStrategy": {"RepairStyle": 1, "RepairStrength": 0},
                    },
                },
            },
        },
    }
    out(client.submit_media(params, "videoInterlacing", sp))

if __name__ == "__main__":
    main()
