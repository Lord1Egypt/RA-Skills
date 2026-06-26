#!/usr/bin/env python3

"""
mix_audios.py — 多轨混音

用法:
  python <SKILL_DIR>/scripts/mix_audios.py '<json_args>'
  python <SKILL_DIR>/scripts/mix_audios.py @params.json

json_args 字段见 references/08-mix-audios.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, fmt_src, out, bail

def main():
    client, sp, args = init_and_parse()

    audios = args.get("audios")
    if not audios:
        bail("mix_audios: audios 不能为空")
    formatted = []
    for a in audios:
        at  = a.get("type", "vid")
        as_ = a.get("source", "")
        formatted.append(fmt_src(at, as_) if at in ("vid", "directurl") else as_)

    param_obj = {"space_name": sp, "audios": formatted}
    out(client.submit_vcreative("loki://167987532", param_obj, sp))

if __name__ == "__main__":
    main()
