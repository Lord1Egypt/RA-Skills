#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""钢结构吨位估算：截面标注 × 米重公式 × 图面长度。

输入是 cad-file-reader `cad_steel_geometry` 的产物 `*.steel.json`
（schema cad-steel-geometry/v1）。识图层只给证据（截面标注、构件标注、
钢构件图层线段），重量在此按以下口径估算：

  米重   = 截面几何公式近似（ρ=7.85，面积 mm² × 0.00785 kg/m）
           不含圆角/公差，H 型约偏低 1~2%，冷弯 C/Z 型偏低 2~5%
  长度   两档——
           ① 显式长度：文本里 L=12345 / 长度 12345（置信高，直接用）
           ② 图面线段：钢构件图层 geometry 段长合计（图面口径，不含
              节点板/加劲肋/下料余量，系统偏低，只作下限证据）
  不足   槽钢（[16 / 槽钢16）等号数型截面无公式，只计数待查表，不进吨位；
         2 段式 H 型（H400x200）缺腹板/翼缘厚度，同样只计数。
         钢板无宽度时只计数。

输出为估算带（±15%），final_quantity=false，不替代深化设计、翻样或结算。

用法
  python3 steel_tonnage.py --steel 钢结构识图/xxx.steel.json --out-prefix 钢结构吨位
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
from collections import defaultdict
from io import StringIO
from pathlib import Path

SCHEMA = "cad-steel-tonnage/v0.1"
RHO = 0.00785  # mm² → kg/m


# ---------------------------------------------------------------- 米重引擎

def _num(values: list[str]) -> list[float]:
    out = []
    for v in values:
        try:
            out.append(float(v))
        except (TypeError, ValueError):
            pass
    return out


def unit_weight_h(text: str, nums: list[float]) -> tuple[float, str]:
    """H 型钢：HN400x200x8x13 → h,b,t1,t2；H400x200 缺厚度 → 不进吨位。"""
    if len(nums) >= 4:
        h, b, t1, t2 = nums[0], nums[1], nums[2], nums[3]
        area = 2 * b * t2 + max(h - 2 * t2, 0) * t1  # 两翼缘 + 腹板
        return area * RHO, "公式（不含圆角，约偏低1~2%）"
    return 0.0, "2 段式 H 型缺腹板/翼缘厚度，仅计数"


def unit_weight_tube(text: str, nums: list[float]) -> tuple[float, str]:
    """圆管 Φ180x6 / D180x6；只有 Φd 一个数字时按实心圆钢。"""
    if len(nums) >= 2 and nums[0] > nums[1]:
        d, t = nums[0], nums[1]
        return (d - t) * 3.14159265 * t * RHO, "公式"
    if len(nums) == 1:
        d = nums[0]
        return 3.14159265 / 4 * d * d * RHO, "无壁厚按实心圆钢公式（若为管需给壁厚）"
    return 0.0, "圆管格式无法解析，仅计数"


def unit_weight_rect(text: str, nums: list[float]) -> tuple[float, str]:
    """方/矩管 □100x100x4 / 200x100x6。"""
    if len(nums) >= 3:
        a, b, t = nums[0], nums[1], nums[2]
        return (2 * (a + b) - 4 * t) * t * RHO, "公式（直角近似）"
    return 0.0, "方矩管缺壁厚，仅计数"


def unit_weight_angle(text: str, nums: list[float]) -> tuple[float, str]:
    """角钢 L100x8（等边）/ L100x63x8（不等边）。"""
    if len(nums) >= 3:
        a, b, t = nums[0], nums[1], nums[2]
        return (a + b - t) * t * RHO, "公式（不含内圆弧）"
    if len(nums) == 2:
        a, t = nums[0], nums[1]
        return (2 * a - t) * t * RHO, "等边公式（不含内圆弧）"
    return 0.0, "角钢格式无法解析，仅计数"


def unit_weight_purlin(text: str, nums: list[float]) -> tuple[float, str]:
    """C/Z 檩条 C200x70x20x2.5 → 展开宽 × 厚。"""
    if len(nums) >= 4:
        h, b = nums[0], nums[1]
        t = nums[3] if nums[3] < nums[2] else nums[2]
        return (h + 2 * b) * t * RHO, "展开宽公式（不含卷边，偏低2~5%）"
    if len(nums) == 3:
        h, b, t = nums[0], nums[1], nums[2]
        return (h + 2 * b) * t * RHO, "展开宽公式（无卷边尺寸）"
    return 0.0, "檩条截面无法解析，仅计数"


def unit_weight_plate(text: str, nums: list[float]) -> tuple[float, str]:
    """钢板 PL8x200（厚x宽，按每米长 kg）；只有厚度时仅计数。"""
    if len(nums) >= 2:
        t, w = nums[0], nums[1]
        return t * w * RHO, "厚×宽（每米长 kg；宽度为标称宽）"
    return 0.0, "钢板缺宽度，仅计数"


_WEIGHTERS = {
    "h_section": unit_weight_h,
    "tube": unit_weight_tube,
    "rect_tube": unit_weight_rect,
    "angle": unit_weight_angle,
    "purlin_section": unit_weight_purlin,
    "plate": unit_weight_plate,
}

_CHANNEL_NO_WEIGHT = {"槽钢", "[", "C"}  # 号数型槽钢无公式


def parse_section(row: dict) -> dict:
    """section 候选 → 解析结果：米重（0=不进吨位）+ 备注。"""
    text = str(row.get("text") or "").strip()
    stype = str(row.get("section_type") or "")
    norm = text.replace("×", "x").replace("X", "x").replace(" ", "")
    nums = _num(re.findall(r"\d+(?:\.\d+)?", norm))
    # 槽钢号数型（[16 / 槽钢16 / 16a）：无公式
    if stype == "channel" or (stype != "purlin_section" and re.match(r"^(\[|槽钢)\d", norm)):
        return {"text": text, "section_type": stype, "kg_m": 0.0,
                "note": "号数型槽钢需查表，仅计数"}
    fn = _WEIGHTERS.get(stype)
    if fn is None:
        if re.match(r"^[A-Za-z]?\d+$", norm):  # 裸数字，无截面类型
            return {"text": text, "section_type": stype, "kg_m": 0.0,
                    "note": "截面类型不明，仅计数"}
        return {"text": text, "section_type": stype, "kg_m": 0.0,
                "note": "截面类型未映射，仅计数"}
    kg_m, note = fn(norm, nums)
    return {"text": text, "section_type": stype, "kg_m": round(kg_m, 2),
            "note": note if kg_m else note}


# ---------------------------------------------------------------- 长度证据

LEN_RE = re.compile(r"(?:L\s*[=＝:]|长度)\s*(\d{3,6})", re.I)


def explicit_lengths(members: list[dict]) -> dict[str, float]:
    """构件标注文本里的显式长度（L=6000 / 长度6000，mm→m）。"""
    out: dict[str, float] = {}
    for m in members:
        for ev in m.get("evidence") or []:
            text = str(ev.get("text") or "")
            hit = LEN_RE.search(text)
            if hit:
                mm = float(hit.group(1))
                if 200 <= mm <= 60000:
                    code = str(m.get("code") or m.get("name") or "?")
                    out.setdefault(code, mm / 1000.0)
    return out


def drawn_length(steel: dict) -> dict[str, float]:
    """钢构件图层 geometry 段长合计（图面口径，按图层分组，mm→m）。"""
    per_layer: dict[str, float] = defaultdict(float)
    for item in steel.get("steel_geometry") or []:
        if not isinstance(item, dict):
            continue
        layer = str(item.get("layer") or "?")
        geom = item.get("geometry")
        vals: list[float] = []
        if isinstance(geom, dict):
            vals = [_f(geom.get(k)) for k in ("length", "length_mm")]
        elif isinstance(geom, (list, tuple)) and len(geom) >= 4:
            x0, y0, x1, y1 = (_f(geom[0]), _f(geom[1]), _f(geom[2]), _f(geom[3]))
            vals = [((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5]
        for v in vals:
            if v > 0:
                per_layer[layer] += v / 1000.0
    return dict(per_layer)


def _f(v) -> float:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.0
    return x


# ---------------------------------------------------------------- 汇总

def build(steel_path: str, out_prefix: str) -> Path:
    steel = json.load(open(steel_path, encoding="utf-8"))
    sections = steel.get("sections") or []
    members = steel.get("members") or []
    if not sections and not members:
        raise SystemExit("❌ steel.json 里没有截面/构件候选"
                         "（确认输入是 cad_steel_geometry 的 *.steel.json）")

    parsed = [parse_section(r) for r in sections]
    usable = [p for p in parsed if p["kg_m"] > 0]
    only_count = [p for p in parsed if p["kg_m"] <= 0]

    expl = explicit_lengths(members)
    layer_len = drawn_length(steel)
    drawn_total = sum(layer_len.values())

    # 长度策略：显式长度有则用其合计；否则用图面线段长度（并标注口径）
    expl_total = sum(expl.values())
    if expl_total > 0:
        length_basis = "explicit"
        length_used, length_note = expl_total, "构件表显式长度 L= 合计"
    elif drawn_total > 0:
        length_basis = "drawn"
        length_used, length_note = drawn_total, "钢构件图层线段长度合计（图面口径，系统偏低）"
    else:
        length_basis = "none"
        length_used, length_note = 0.0, "无长度证据，只出截面谱不出吨位"

    # 截面谱：按（类型,文本,米重）聚合标注次数
    spec: dict[tuple, dict] = {}
    for p in parsed:
        key = (p["section_type"], p["text"], p["kg_m"])
        rec = spec.setdefault(key, {"count": 0, "note": p["note"]})
        rec["count"] += 1
    spec_rows = [
        {"section_type": k[0], "text": k[1], "kg_m": k[2],
         "count": v["count"], "note": v["note"]}
        for k, v in sorted(spec.items(), key=lambda kv: (-kv[0][2], kv[0][1]))
    ]

    # 吨位：把总长度按「截面米重加权」分摊到有米重的截面（权重=米重×次数），
    # 这在缺「每根构件↔截面」映射时是对总量最不坏的分摊假设。
    rows: list[dict] = []
    total_lo = total_hi = 0.0
    weight_sum = sum(r["kg_m"] * r["count"] for r in spec_rows if r["kg_m"] > 0)
    if length_used > 0 and weight_sum > 0:
        for r in spec_rows:
            if r["kg_m"] <= 0:
                continue
            share = (r["kg_m"] * r["count"]) / weight_sum
            length_m = length_used * share
            t_lo = r["kg_m"] * length_m * 0.85 / 1000.0   # -15%
            t_hi = r["kg_m"] * length_m * 1.15 / 1000.0   # +15%
            total_lo += t_lo
            total_hi += t_hi
            rows.append({
                "截面类型": r["section_type"], "截面": r["text"],
                "标注次数": r["count"], "米重kg/m": r["kg_m"],
                "分摊长度m": round(length_m, 1),
                "吨位带t": [round(t_lo, 2), round(t_hi, 2)],
            })
        total_lo, total_hi = round(total_lo, 2), round(total_hi, 2)

    out = {
        "schema": SCHEMA,
        "final_quantity": False,
        "length_basis": length_basis,
        "length_note": length_note,
        "length_used_m": round(length_used, 1),
        "drawn_length_by_layer": {k: round(v, 1) for k, v in
                                  sorted(layer_len.items(), key=lambda kv: -kv[1])},
        "explicit_lengths_m": expl,
        "rows": rows,
        "spec_rows": spec_rows,
        "only_count": [p["text"] for p in only_count],
        "total_t": [total_lo, total_hi] if rows else [],
        "summary": {
            "截面标注数": len(parsed),
            "可计米重截面数": len(usable),
            "仅计数截面数": len(only_count),
            "构件标注数": len(members),
            "总吨位带t": [total_lo, total_hi] if rows else [],
        },
    }
    _render(out, Path(steel_path).stem, out_prefix)
    return Path(str(out_prefix) + ".csv")


def _render(out: dict, title: str, out_prefix: str) -> None:
    out_base = Path(out_prefix)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    Path(str(out_base) + ".json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    md = StringIO()
    s = out["summary"]
    md.write(f"# {title}（钢结构吨位估算）\n\n")
    md.write("> **口径声明**：估算带（±15%），final_quantity=false；米重为截面几何公式近似"
             "（不含圆角，H 型偏低 1~2%、冷弯 C/Z 偏低 2~5%）；不替代深化设计、翻样、下料与结算。\n")
    md.write(f"> 长度口径：**{out['length_note']}**\n\n")
    md.write(f"- 截面标注 {s['截面标注数']} 条（可计米重 {s['可计米重截面数']}、"
             f"仅计数 {s['仅计数截面数']}）；构件标注 {s['构件标注数']} 条\n")
    if out["total_t"]:
        md.write(f"- **总吨位带：{out['total_t'][0]}~{out['total_t'][1]} t**"
                 f"（长度 {out['length_used_m']} m 按米重×次数加权分摊）\n\n")
        md.write("## 分截面吨位\n\n| 截面类型 | 截面 | 标注次数 | 米重kg/m | 分摊长度m | 吨位t带 |\n|---|---|---|---|---|---|\n")
        for r in out["rows"]:
            md.write(f"| {r['截面类型']} | {r['截面']} | {r['标注次数']} | {r['米重kg/m']} "
                     f"| {r['分摊长度m']} | {r['吨位带t'][0]}~{r['吨位带t'][1]} |\n")
        md.write("\n")
    else:
        md.write("- ⚠️ 无长度证据或无可计米重截面：只出截面谱，不出吨位\n\n")
    if out["drawn_length_by_layer"]:
        md.write("## 图面线段长度（钢构件图层）\n\n| 图层 | 长度m |\n|---|---|\n")
        for k, v in out["drawn_length_by_layer"].items():
            md.write(f"| {k} | {v} |\n")
        md.write("\n")
    md.write("## 截面谱（全部标注）\n\n| 截面类型 | 截面原文 | 次数 | 米重kg/m | 备注 |\n|---|---|---|---|---|\n")
    for r in out["spec_rows"]:
        md.write(f"| {r['section_type']} | {r['text']} | {r['count']} | "
                 f"{r['kg_m'] or '-'} | {r['note']} |\n")
    if out["only_count"]:
        md.write(f"\n（以下 {len(out['only_count'])} 条标注未进吨位：{'、'.join(out['only_count'][:20])}"
                 f"{'…' if len(out['only_count']) > 20 else ''}）\n")
    Path(str(out_base) + ".md").write_text(md.getvalue(), encoding="utf-8")

    with Path(str(out_base) + ".csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["口径", "数值", "说明"])
        if out["total_t"]:
            w.writerow(["总吨位带t", f"{out['total_t'][0]}~{out['total_t'][1]}",
                        f"长度口径：{out['length_note']}"])
            for r in out["rows"]:
                w.writerow([f"吨位-{r['截面']}", f"{r['吨位带t'][0]}~{r['吨位带t'][1]}",
                            f"{r['米重kg/m']} kg/m × {r['分摊长度m']} m × {r['标注次数']} 次标注分摊"])
        else:
            w.writerow(["总吨位", "", "无长度证据或无可计米重截面，只出截面谱"])
        for r in out["spec_rows"]:
            w.writerow([f"截面谱-{r['text']}", r["count"], f"{r['section_type']}；{r['note']}"])


def main() -> None:
    raw = sys.argv[1:]
    ap = argparse.ArgumentParser(
        description="Steel tonnage estimate from cad_steel_geometry output")
    ap.add_argument("--steel", required=True,
                    help="cad_steel_geometry 产物 *.steel.json")
    ap.add_argument("--out-prefix", required=True)
    a = ap.parse_args(raw)
    build(a.steel, a.out_prefix)


if __name__ == "__main__":
    main()
