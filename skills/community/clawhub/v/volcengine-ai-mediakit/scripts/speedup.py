#!/usr/bin/env python3

"""
speedup.py — 视频/音频变速

用法:
  python <SKILL_DIR>/scripts/speedup.py video '<json_args>'
  python <SKILL_DIR>/scripts/speedup.py audio '<json_args>'
  python <SKILL_DIR>/scripts/speedup.py video @params.json

json_args 字段见 references/04-speedup.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, fmt_src, out, bail

WORKFLOW = {
    "video": "loki://165223469",
    "audio": "loki://174663067",
}

def main():
    if len(sys.argv) < 3:
        bail("用法: python <SKILL_DIR>/scripts/speedup.py <video|audio> '<json_args>'")
    media_type = sys.argv[1]
    if media_type not in WORKFLOW:
        bail(f"第一个参数必须为 video 或 audio，得到：{media_type!r}")

    # speedup 的 JSON 在 argv[2]，space_name 在 argv[3]
    client, sp, args = init_and_parse(argv_pos=2, sp_pos=3)

    t      = args.get("type", "vid")
    source = args.get("source")
    if not source:
        bail("speedup: source 不能为空")
    speed  = float(args.get("speed", 1.0))
    if not (0.1 <= speed <= 4):
        bail("speedup: speed 必须在 0.1～4 之间")

    param_obj = {
        "space_name": sp,
        "source": fmt_src(t, source),
        "speed":  speed,
    }
    out(client.submit_vcreative(WORKFLOW[media_type], param_obj, sp))

if __name__ == "__main__":
    main()
