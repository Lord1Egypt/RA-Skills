#!/usr/bin/env python3

"""
clipping.py — 视频/音频裁剪

用法:
  python <SKILL_DIR>/scripts/clipping.py '<json_args>'
  python <SKILL_DIR>/scripts/clipping.py @params.json

json_args 字段见 references/02-clipping.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, fmt_src, out, bail

def main():
    client, sp, args = init_and_parse()

    t      = args.get("type", "video")
    source = args.get("source")
    if not source:
        bail("clipping: source 不能为空")
    start  = float(args.get("start_time", 0))
    end    = float(args.get("end_time", start + 1))
    if end <= start:
        bail("clipping: end_time 必须大于 start_time")

    param_obj = {
        "space_name": sp,
        "source":     fmt_src(t, source),
        "start_time": start,
        "end_time":   end,
    }
    wf = "loki://158666752" if t == "audio" else "loki://154419276"
    out(client.submit_vcreative(wf, param_obj, sp))

if __name__ == "__main__":
    main()
