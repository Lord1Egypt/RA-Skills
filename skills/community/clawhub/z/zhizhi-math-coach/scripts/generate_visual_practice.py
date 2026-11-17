#!/usr/bin/env python3
"""Generate varied visual practice specs with answers derived from diagram data."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
from pathlib import Path

from geometry_primitives import validate_geometry


KINDS = ("shape_collection", "clock", "number_line", "grid")
KNOWLEDGE_KINDS = {"geometry.shape-recognition": "shape_collection", "time.clock-reading": "clock",
                   "number.number-line": "number_line", "geometry.grid-counting": "grid"}


def question_from_geometry(geometry: dict) -> dict:
    validate_geometry(geometry)
    kind = geometry["type"]
    if kind == "shape_collection":
        names = {"circle": "圆形", "triangle": "三角形", "square": "正方形", "rectangle": "长方形"}
        present = sorted({shape["kind"] for shape in geometry["shapes"]})
        prompt = "数一数图中各种图形分别有几个。"
        detail = "；".join(f"{names[name]}{sum(shape['kind'] == name for shape in geometry['shapes'])}个" for name in present) + "。按种类逐个标记，避免重复计数。"
    elif kind == "clock":
        prompt = "看钟面，写出现在的时间。"
        detail = f"{geometry['hour'] % 12 or 12}时{geometry.get('minute', 0):02d}分。短针表示小时，长针表示分钟。"
    elif kind == "number_line":
        prompt = "按从左到右的顺序，填写数轴上方框中的数。"
        hidden = sorted(geometry.get("hidden_values", []))
        if not hidden:
            raise ValueError("number-line practice needs at least one hidden value")
        detail = "依次填：" + "、".join(map(str, hidden)) + f"。相邻刻度相差{geometry.get('step', 1)}。"
    elif kind == "grid":
        prompt = "数一数，图中涂色的小方格一共有多少个？"
        detail = f"共有{len(geometry.get('shaded_cells', []))}个涂色小方格。可逐行计数，再把各行数量相加。"
    else:
        raise ValueError("template_verified supports only the four built-in visual templates")
    return {"prompt": prompt, "answer_prompt": "答：", "answer_detail": detail}


def make_item(kind: str, rng: random.Random) -> dict:
    if kind == "shape_collection":
        count = rng.randint(6, 12)
        shapes = []
        for index in range(count):
            shape = rng.choice(["circle", "triangle", "square", "rectangle"])
            shapes.append({"kind": shape, "x": 15 + index % 4 * 75, "y": 15 + index // 4 * 55,
                           "width": 48 if shape == "rectangle" else 30, "height": 30})
        geometry = {"type": kind, "shapes": shapes, "canvas_width": 320, "canvas_height": 180}
    elif kind == "clock":
        geometry = {"type": kind, "hour": rng.randint(1, 12), "minute": rng.choice([0, 30]),
                    "canvas_width": 220, "canvas_height": 220}
    elif kind == "number_line":
        start = rng.randint(0, 10)
        geometry = {"type": kind, "start": start, "end": start + 10, "step": 1,
                    "hidden_values": sorted(rng.sample(list(range(start + 1, start + 10)), 3)),
                    "canvas_width": 400, "canvas_height": 100}
    else:
        count = rng.randint(4, 12)
        cells = rng.sample([[r, c] for r in range(4) for c in range(5)], count)
        geometry = {"type": kind, "rows": 4, "cols": 5, "shaded_cells": sorted(cells),
                    "canvas_width": 260, "canvas_height": 200}
    return {"type": "geometry_problem", "geometry_spec": geometry, "work_lines": 1,
            "review_status": "template_verified", **question_from_geometry(geometry)}


def make_spec(kind: str, count: int, seed: int, date: str) -> dict:
    rng = random.Random(seed)
    kinds = list(KINDS) if kind == "mixed" else [kind]
    items = [make_item(kinds[index % len(kinds)], rng) for index in range(count)]
    return {"version": 1, "title": "看图数学小练习", "date": date, "topic": kind,
            "strategy": "geometry_drill", "review_status": "template_verified", "seed": seed,
            "target": "看清图形信息，独立作答并解释方法。",
            "sections": [{"title": "看图作答", "layout": "problem-grid-2", "items": items}]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=[*KINDS, "mixed", "auto"], default="mixed")
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument("--count", type=int, default=4)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.count <= 12:
        parser.error("--count must be between 1 and 12")
    dt.date.fromisoformat(args.date)
    kind = args.kind
    selected = None
    if kind == "auto":
        state = json.loads((args.workspace / "records/knowledge-state.json").read_text(encoding="utf-8"))
        priorities = {"需要巩固": 0, "待确认": 1, "待观察": 2, "初步掌握": 3, "稳定掌握": 4}
        candidates = [(key, value) for key, value in state.get("concepts", {}).items() if key in KNOWLEDGE_KINDS]
        if not candidates:
            parser.error("no supported visual knowledge points in the learning record; choose --kind explicitly")
        selected, _ = min(candidates, key=lambda pair: (priorities.get(pair[1]["status"], 5), pair[1]["next_review_date"]))
        kind = KNOWLEDGE_KINDS[selected]
    spec = make_spec(kind, args.count, args.seed, args.date)
    if selected:
        spec["based_on_knowledge_point"] = selected
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
