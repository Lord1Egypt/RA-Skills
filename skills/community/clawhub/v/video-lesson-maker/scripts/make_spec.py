#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由绘制结果生成 annotation spec —— 让 region 坐标不可能再与画面漂移。

问题：spec 的 region 是手写的，enhance_scenes.py 的绘制坐标是另一处手写的。
只要改了其中一处（比如把便签上移 40px 避开字幕带），两者就漂移，成片里的
表现是「那块文字永远不出现」——项目3 就这样在 13 幕里丢掉过整块内容。

做法：enhance_scenes.py 里对每个场景调用

    from enhance_toolkit import LAYOUT
    LAYOUT.begin(im)
    ...绘制（draw_title / draw_label_card / draw_note 会自动登记）...
    LAYOUT.save(f"layout-{idx}.json")

再用本脚本把 layout × 时长参数转成 spec：

    python make_spec.py --layout layout-01.json --out spec-01.json \
        --dur 4000 --title-dur 3000 --gaze 1200 --pad 8

region 顺序 = 绘制顺序（先标题、后主体），这与白板揭示的讲授节奏一致。
"""
from __future__ import annotations

import argparse
import json
import sys


def main():
    ap = argparse.ArgumentParser(description="layout.json → spec-0N.json")
    ap.add_argument("--layout", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dur", type=int, default=4000, help="普通块揭示时长 ms")
    ap.add_argument("--title-dur", type=int, default=3000, help="标题块揭示时长 ms")
    ap.add_argument("--gaze", type=int, default=1200, help="结尾凝视 ms")
    ap.add_argument("--pad", type=int, default=8, help="region 外扩 px（覆盖手绘抖动）")
    ap.add_argument("--margin", type=int, default=0,
                    help="强制内缩到画布留白内（默认 0 = 不内缩，只裁到画布内）")
    a = ap.parse_args()

    d = json.load(open(a.layout, encoding="utf-8"))
    cw = d["canvas"]["width"]
    ch = d["canvas"]["height"]
    els = d["elements"]
    if not els:
        print("layout 里没有元素，先确认 enhance_scenes.py 调用了 LAYOUT.begin(im)")
        return 2

    regions = []
    for e in els:
        x0 = max(0, e["x"] - a.pad)
        y0 = max(0, e["y"] - a.pad)
        x1 = min(cw, e["x"] + e["width"] + a.pad)
        y1 = min(ch, e["y"] + e["height"] + a.pad)
        if a.margin:
            x0, y0 = max(x0, a.margin), max(y0, a.margin)
            x1, y1 = min(x1, cw - a.margin), min(y1, ch - a.margin)
        dur = a.title_dur if str(e["tag"]).startswith("title") else a.dur
        regions.append({"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0,
                        "dur": dur, "tag": e["tag"]})

    total = sum(r["dur"] for r in regions) + a.gaze
    spec = {"canvas": {"width": cw, "height": ch},
            "regions": regions,
            "durationMs": a.dur,
            "leadMs": 0,
            "gazeMs": a.gaze}
    json.dump(spec, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{len(regions)} 块 → {a.out}｜无声时长合计 {total / 1000:.1f}s")
    for r in regions:
        print(f"  ({r['x']:>4},{r['y']:>4},{r['width']:>4},{r['height']:>3})  "
              f"{r['dur']:>5}ms  {r['tag']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
