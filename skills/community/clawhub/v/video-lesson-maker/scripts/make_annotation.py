#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""白板动画揭示编排生成器：按区域顺序自动产出 annotation.json。

把"手写标注"这一步标准化。输入一个 spec（JSON），描述画布尺寸与若干揭示区域
（按绘制顺序），脚本按累计时间自动算出每个区域的 startMs / durationMs，并给出
sceneDurationMs。

⚠️ 关键约定（本项目 V05 重大教训）：
  startMs 必须是「幕内相对时间」，绝非成片绝对时间！写成绝对时间会把每幕
  拉长到几十秒。本脚本默认就产幕内相对时间。

spec JSON 字段：
  {
    "canvas": {"width": 1536, "height": 864},
    "regions": [
      {"x":100,"y":80,"width":600,"height":120},            # 标题区
      {"x":100,"y":240,"width":500,"height":200,"dur":4000},# 主体1（可覆盖默认时长）
      {"x":700,"y":240,"width":500,"height":200,
       "protectedRegions":[{"x":120,"y":260,"width":200,"height":40}]}
    ],
    "durationMs": 3000,   # 每个区域默认揭示时长(ms)
    "leadMs": 0,          # 每个区域开始前的留白(ms)
    "gazeMs": 1500        # 结尾凝视(ms)，计入 sceneDurationMs
  }

输出：annotation.json（可直接喂给 render_stream_whiteboard.py）

用法：
  python make_annotation.py --spec spec.json --out annotation.json
"""
import argparse
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="区域编排 spec JSON")
    ap.add_argument("--out", required=True, help="输出 annotation.json 路径")
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    canvas = spec["canvas"]
    regions = spec["regions"]
    duration_ms = int(spec.get("durationMs", 3000))
    lead_ms = int(spec.get("leadMs", 0))
    gaze_ms = int(spec.get("gazeMs", 1500))

    elements = []
    cursor = 0
    for reg in regions:
        dur = int(reg.get("dur", duration_ms))
        start = cursor + lead_ms
        el = {
            "region": {
                "x": reg["x"], "y": reg["y"],
                "width": reg["width"], "height": reg["height"],
            },
            "reveal": {
                "startMs": start,
                "durationMs": dur,
                "protectedRegions": reg.get("protectedRegions", []),
            },
        }
        elements.append(el)
        cursor = start + dur

    scene_duration = cursor + gaze_ms
    ann = {
        "canvas": {"width": canvas["width"], "height": canvas["height"]},
        "sceneDurationMs": scene_duration,
        "elements": elements,
    }
    json.dump(ann, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    last_end = cursor
    print(f"区域数: {len(elements)}  末元素结束: {last_end}ms  sceneDurationMs: {scene_duration}ms")
    print(f"自检: {'通过' if last_end < scene_duration else '失败(末元素超出 sceneDuration)'}")
    print(f"已写出 -> {a.out}")


if __name__ == "__main__":
    main()
