#!/usr/bin/env python3

"""
image_to_video.py — 图片转视频

用法:
  python <SKILL_DIR>/scripts/image_to_video.py '<json_args>'
  python <SKILL_DIR>/scripts/image_to_video.py @params.json

json_args 字段见 references/05-image-to-video.md
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_common import init_and_parse, fmt_src, out, bail

def main():
    client, sp, args = init_and_parse()

    images = args.get("images")
    if not images:
        bail("image_to_video: images 不能为空")
    formatted = []
    for img in images:
        it   = img.get("type", "vid")
        isrc = img.get("source", "")
        item = {"type": it, "source": fmt_src(it, isrc) if it in ("vid", "directurl") else isrc}
        for k in ("duration", "animation_type", "animation_in", "animation_out"):
            if k in img:
                item[k] = img[k]
        formatted.append(item)

    param_obj = {
        "space_name":  sp,
        "images":      formatted,
        "transitions": args.get("transitions") or [],
    }
    out(client.submit_vcreative("loki://167979998", param_obj, sp))

if __name__ == "__main__":
    main()
