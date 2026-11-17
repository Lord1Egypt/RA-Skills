#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 cad_scan detail JSON 提取人防结构计量前的专项复核清单。

只做人防构件/口部/专业接口的文字与图层证据归类，不计算人防结构量，
不推断门框墙尺寸、钢筋规格或混凝土等级。
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

SCHEMA = "cad-civil-defense-checklist/v1"

RULES = [
    {
        "id": "protection_zone",
        "name": "防护单元/抗力等级",
        "patterns": ["防护单元", "抗暴单元", "核6级", "核5级", "常6级", "常5级", "人防分区"],
        "why": "先确认防护单元边界和抗力等级，后续门框墙、临空墙、封堵不能跨单元错算。",
    },
    {
        "id": "door_frame_wall",
        "name": "人防门/门框墙/封堵",
        "patterns": ["防护密闭门", "密闭门", "门框墙", "封堵墙", "封堵板", "临战封堵"],
        "why": "人防门框墙和封堵构件通常不能按普通墙柱梁直接套用，必须单列复核。",
    },
    {
        "id": "shell_wall",
        "name": "临空墙/防护墙",
        "patterns": ["临空墙", "防护外墙", "防护密闭墙", "人防墙", "防护墙体", "人防防护墙"],
        "why": "防护墙体可能兼作平时剪力墙，需要按平时/战时取大值并核对边缘构件归属。",
    },
    {
        "id": "opening",
        "name": "口部/密闭通道",
        "patterns": ["口部", "进风口", "排风口", "滤毒", "防毒通道", "密闭通道", "洗消间"],
        "why": "口部房间、通道和孔洞是钢筋、模板、预留预埋的集中部位，需独立列复核清单。",
    },
    {
        "id": "slab_structure",
        "name": "人防顶板/底板",
        "patterns": ["人防顶板", "人防底板", "顶板", "底板", "防护顶板"],
        "why": "顶底板厚度和标高变化会影响梁墙柱交接、洞口和混凝土分账。",
    },
    {
        "id": "beam_column_wall",
        "name": "顶梁/墙柱/基础",
        "patterns": ["人防顶梁", "墙、柱", "墙柱", "基础平面", "基础平法", "基础底板"],
        "why": "需要把结构平面、详图和基础说明串起来，避免只看单张平面漏构件。",
    },
    {
        "id": "mep_interfaces",
        "name": "给排水/电气/暖通接口",
        "patterns": ["战时给排水", "人防给排水", "洗消", "战时通风", "人防通风", "防爆波电缆井", "人防电气", "战时照明"],
        "why": "人防专业接口多，结构计量前应把预留洞、套管、设备基础和封堵接口交给各专业核对。",
    },
]


def _records(data: dict[str, Any]) -> list[dict[str, Any]]:
    raw = data.get("text_records") or data.get("texts") or []
    out: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        text = " ".join(str(item.get("text") or "").split())
        if text:
            out.append({
                "text": text,
                "layer": str(item.get("layer") or ""),
                "file": item.get("file"),
                "sheet": item.get("sheet"),
                "x": item.get("x"),
                "y": item.get("y"),
            })
    return out


def _evidence(rec: dict[str, Any], pattern: str) -> dict[str, Any]:
    out = {"pattern": pattern, "text": rec["text"][:240]}
    for key in ("layer", "file", "sheet", "x", "y"):
        if rec.get(key) not in (None, ""):
            out[key] = rec[key]
    return out


def build(data: dict[str, Any]) -> dict[str, Any]:
    records = _records(data)
    checklist = []
    for rule in RULES:
        hits: list[dict[str, Any]] = []
        for rec in records:
            for pattern in rule["patterns"]:
                if pattern.lower() in rec["text"].lower():
                    hits.append(_evidence(rec, pattern))
                    break
        checklist.append({
            "id": rule["id"],
            "name": rule["name"],
            "status": "evidence_found" if hits else "missing_evidence",
            "hit_count": len(hits),
            "evidence": hits[:20],
            "action": rule["why"],
        })
    layer_counts = Counter(rec.get("layer") or "<空图层>" for rec in records)
    roles = {
        "civil_defense_terms": sum(1 for rec in records if any(
            term in rec["text"] for term in ("人防", "防护密闭", "临空墙", "门框墙", "防护单元")
        )),
        "opening_terms": sum(1 for rec in records if any(
            term in rec["text"] for term in ("口部", "进风口", "排风口", "密闭通道", "防毒通道")
        )),
        "mep_terms": sum(1 for rec in records if any(
            term in rec["text"] for term in ("战时给排水", "人防给排水", "战时通风", "人防通风", "防爆波电缆井", "人防电气")
        )),
    }
    return {
        "schema": SCHEMA,
        "source": data.get("source_file") or (data.get("files") or [{}])[0].get("name") or "",
        "summary": {
            "text_records": len(records),
            "checklist_total": len(checklist),
            "evidence_found": sum(1 for row in checklist if row["status"] == "evidence_found"),
            "missing_evidence": sum(1 for row in checklist if row["status"] == "missing_evidence"),
            **roles,
        },
        "checklist": checklist,
        "top_layers": [{"layer": layer, "text_count": count} for layer, count in layer_counts.most_common(30)],
        "formal_ready": False,
        "boundary": "只输出人防结构算量前的专项复核清单和文字证据，不输出人防结构工程量、钢筋量、材料量、造价或结算量。",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="人防结构算量前专项复核清单")
    parser.add_argument("detail", help="cad_scan detail.json（含 text_records）")
    parser.add_argument("--out", required=True, help="输出 JSON")
    args = parser.parse_args()
    src = Path(args.detail).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"输入不存在：{src}")
    result = build(json.loads(src.read_text(encoding="utf-8")))
    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
