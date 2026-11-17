#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cad_beam_benchmark.py - 把 CAD 自动梁中心线结果与广联达模型汇总做对照。

用途：内测时不对外宣称精度；每次改动后用同一组 auto JSON 看趋势。

  cad_beam_benchmark.py \
      --model-summary 1#楼各层混凝土方量汇总.csv \
      --auto-json dir/*beam_auto.json -o 梁自动与模型对照
"""



from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
import cad_quantity  # noqa: E402


def _cn_to_no(text: str) -> int | None:
    return cad_quantity._cn_to_no(text)


def _parse_floor_name(text: str) -> int | None:
    t = str(text or "").replace(" ", "")
    if t == "首层":
        return 1
    if t == "基础层":
        return -1
    if t.startswith("第"):
        t = t[1:]
    if t.endswith("层"):
        t = t[:-1]
    return _cn_to_no(t)


def load_model_summary(path: Path) -> dict[str, dict[str, float]]:
    """按 楼层 -> (构件,等级) -> m3 建索引。"""
    out: dict[str, dict[str, float]] = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = csv.DictReader(f)
        for row in rows:
            floor = str(row.get("楼层") or "").strip()
            component = str(row.get("构件类别") or "").strip()
            grade = str(row.get("混凝土强度等级") or "").strip()
            try:
                value = float(row.get("方量合计(m3)") or 0)
            except ValueError:
                continue
            key = f"{component}|{grade}"
            out.setdefault(floor, {}).setdefault(key, 0.0)
            out[floor][key] += value
    return out


def floor_range(label: str) -> tuple[int | None, int | None]:
    return cad_quantity.floor_label_kind(label)[:2]


def render_md(items: list[dict[str, Any]]) -> str:
    o = ["# CAD 梁自动粗算 vs 广联达模型对照", ""]
    o.append("| 图纸 | 自动梁 m3 | 模型梁 m3 | 模型连梁 m3 | 差异 % | 自动对象 |")
    o.append("|---|---:|---:|---:|---:|---:|")
    for it in items:
        model = it["model_beam_m3"]
        auto = it["auto_m3"]
        diff = (auto - model) / model * 100 if model else None
        o.append(f"| {it['floor_label']} | {auto:.3f} | {model:.3f} | "
                 f"{it['model_ll_m3']:.3f} | "
                 f"{'-' if diff is None else round(diff, 1)}% | "
                 f"{it['resolved_count']} |")
    o += [
        "",
        "口径：模型梁取 C30/梁，模型连梁另列；自动结果只统计梁平法集中标注中心线，",
        "尚未含 LL/TL 等墙柱/楼梯梁，也未做支座净跨。",
        "",
    ]
    return "\n".join(o)


def csv_lines(items: list[dict[str, Any]]) -> list[list[str]]:
    out = [["图纸", "自动梁m3", "模型梁m3", "模型连梁m3", "差异%", "自动对象", "覆盖楼层"]]
    for it in items:
        model = it["model_beam_m3"]
        diff = (it["auto_m3"] - model) / model * 100 if model else ""
        out.append([it["floor_label"], f"{it['auto_m3']:.3f}", f"{model:.3f}",
                    f"{it['model_ll_m3']:.3f}", f"{diff:.1f}" if diff != "" else "",
                    str(it["resolved_count"]), it["floor_numbers"]])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-summary", required=True)
    ap.add_argument("--auto-json", nargs="+", required=True)
    ap.add_argument("-o", "--out", default="beam_benchmark")
    args = ap.parse_args()
    model = load_model_summary(Path(args.model_summary))
    items = []
    for p in args.auto_json:
        data = json.loads(Path(p).read_text(encoding="utf-8"))
        label = str(data.get("floor_label") or "")
        lo, hi = floor_range(label)
        floor_names = []
        model_beam = 0.0
        model_ll = 0.0
        if lo is not None and hi is not None:
            for floor_name, comps in model.items():
                fn = _parse_floor_name(floor_name)
                if fn is None:
                    continue
                if lo <= fn <= hi:
                    floor_names.append(floor_name)
                    model_beam += comps.get("梁|C30", 0.0)
                    model_ll += comps.get("连梁|C30", 0.0)
        count = len(floor_names) or 1
        items.append({
            "floor_label": label,
            "auto_m3": float(data.get("total_beam_concrete_m3") or 0),
            "model_beam_m3": round(model_beam / count, 3),
            "model_ll_m3": round(model_ll / count, 3),
            "resolved_count": int(data.get("resolved_count") or 0),
            "floor_numbers": ",".join(floor_names) or "-",
        })
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".md").write_text(render_md(items), encoding="utf-8")
    with out.with_suffix(".csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_lines(items))
    print(f"已写出 {out.with_suffix('.md')} / {out.with_suffix('.csv')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
