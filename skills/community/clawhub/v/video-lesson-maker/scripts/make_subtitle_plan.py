#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 narration_plan.json 生成 build_subtitles.py 所需的 subtitle_plan.json。

build_subtitles.py 要求 --plan 为 [{idx, start, file}]，file 是 narration 工作
目录下的一段 wav 文件名（默认 segXX.wav）。

用法：
  python make_subtitle_plan.py --plan narration_plan.json \
      [--out narration/subtitle_plan.json]
"""
import argparse
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True, help="prepare_narration.py 产出的 narration_plan.json")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    plan = json.load(open(a.plan, encoding="utf-8"))
    out = []
    for seg in plan["segments"]:
        idx = int(seg["idx"])
        out.append({"idx": idx, "start": seg["start"], "file": f"seg{idx:02d}.wav"})

    out_path = a.out or os.path.join(plan.get("work", "."), "subtitle_plan.json")
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"已写出 subtitle_plan.json ({len(out)} 段) -> {out_path}")


if __name__ == "__main__":
    main()
