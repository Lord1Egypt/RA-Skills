#!/usr/bin/env python3

"""
extract_audio.py — 从视频中提取音轨

用法:
  python <SKILL_DIR>/scripts/extract_audio.py '<json_args>'
  python <SKILL_DIR>/scripts/extract_audio.py @params.json

json_args 字段见 references/07-extract-audio.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, fmt_src, out, bail

def main():
    client, sp, args = init_and_parse()

    t      = args.get("type", "vid")
    source = args.get("source")
    if not source:
        bail("extract_audio: source 不能为空")
    fmt    = args.get("format", "m4a")
    if fmt not in ("mp3", "m4a"):
        bail("extract_audio: format 必须为 mp3 或 m4a")

    param_obj = {
        "space_name": sp,
        "source": fmt_src(t, source),
        "format": fmt,
    }
    out(client.submit_vcreative("loki://167986559", param_obj, sp))

if __name__ == "__main__":
    main()
