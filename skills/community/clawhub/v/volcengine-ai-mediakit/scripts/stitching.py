#!/usr/bin/env python3

"""
stitching.py — 视频/音频拼接

用法:
  python <SKILL_DIR>/scripts/stitching.py '<json_args>'
  python <SKILL_DIR>/scripts/stitching.py @params.json

json_args 字段见 references/01-stitching.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, fmt_src, out, bail

def main():
    client, sp, args = init_and_parse()

    t = args.get("type", "video")
    if t == "audio":
        audios = args.get("audios")
        if not audios:
            bail("stitching(audio): audios 不能为空")
        param_obj = {
            "space_name": sp,
            "audios": [a if a.startswith(("vid://","directurl://","http://","https://")) else fmt_src("vid", a) for a in audios],
        }
        out(client.submit_vcreative("loki://158487089", param_obj, sp))
    else:
        videos = args.get("videos")
        if not videos:
            bail("stitching(video): videos 不能为空")
        param_obj = {
            "space_name": sp,
            "videos": [v if v.startswith(("vid://","directurl://","http://","https://")) else fmt_src("vid", v) for v in videos],
            "transitions": args.get("transitions") or [],
        }
        out(client.submit_vcreative("loki://154775772", param_obj, sp))

if __name__ == "__main__":
    main()
