#!/usr/bin/env python3

"""
portrait_matting.py — 人像抠图

用法:
  python <SKILL_DIR>/scripts/portrait_matting.py '<json_args>'
  python <SKILL_DIR>/scripts/portrait_matting.py @params.json

json_args 字段见 references/20-portrait-matting.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, build_media_input, out, bail

def main():
    client, sp, args = init_and_parse()

    t     = args.get("type", "Vid")
    video = args.get("video")
    if not video:
        bail("portrait_matting: video 不能为空")

    fmt = args.get("output_format", "WEBM").upper()
    if fmt not in ("MOV", "WEBM"):
        bail(f"portrait_matting: output_format 必须为 MOV 或 WEBM，得到：{fmt}")

    params = {
        "Input": build_media_input(t, video, sp),
        "Operation": {
            "Type": "Task",
            "Task": {
                "Type": "VideoMatting",
                "VideoMatting": {
                    "Model":       "Human",
                    "VideoOption": {"Format": fmt},
                    "NewVid":      True,
                },
            },
        },
    }
    out(client.submit_media(params, "portraitImageRetouching", sp))

if __name__ == "__main__":
    main()
