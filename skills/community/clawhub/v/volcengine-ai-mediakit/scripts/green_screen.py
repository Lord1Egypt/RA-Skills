#!/usr/bin/env python3

"""
green_screen.py — 绿幕抠图

用法:
  python <SKILL_DIR>/scripts/green_screen.py '<json_args>'
  python <SKILL_DIR>/scripts/green_screen.py @params.json

json_args 字段见 references/21-green-screen.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, build_media_input, out, bail

def main():
    client, sp, args = init_and_parse()

    t     = args.get("type", "Vid")
    video = args.get("video")
    if not video:
        bail("green_screen: video 不能为空")

    fmt = args.get("output_format", "WEBM").upper()
    if fmt not in ("MOV", "WEBM"):
        bail(f"green_screen: output_format 必须为 MOV 或 WEBM，得到：{fmt}")

    params = {
        "Input": build_media_input(t, video, sp),
        "Operation": {
            "Type": "Task",
            "Task": {
                "Type": "VideoMatting",
                "VideoMatting": {
                    "Model":       "GreenScreen",
                    "VideoOption": {"Format": fmt},
                    "NewVid":      True,
                },
            },
        },
    }
    out(client.submit_media(params, "greenScreen", sp))

if __name__ == "__main__":
    main()
