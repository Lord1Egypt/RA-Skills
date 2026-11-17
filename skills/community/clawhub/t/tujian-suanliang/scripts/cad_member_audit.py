#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构件级三级校对：图面标注 × 模型几何 自洽性审计。

对同一批构件，把两份独立产物的数据按编号互对：

  L1 图面标注（优先 beam_objects.json：目标图框内的梁标注解析——
     code/section/length_mm/volume_m3；未提供时退回 component_schedule：
     scan.members 的全文件标注索引，此时覆盖缺口会混入其他图框的标注，
     审计结论需谨慎）
  L2 模型几何（quantity_report.beam_schedule，source=model.members.beams
     或 beam_objects.rows 回退）
     —— 模型展开出的：截面、中心线长、毛/净体积、支座数

输出五态（按 base_code 归并）：
  一致        两侧都有，截面可比且一致
  截面冲突    两侧都有，截面不一致（审计核心发现）
  图面有模型无  L1 有该编号、L2 没有（漏建/漏识别）
  模型有图面无  L2 有该编号、L1 没有（无图面标注依据）
  规格残缺    两侧都有但截面一侧为空，无法比

再加两条总量守恒线：编号数（L1 vs L2）、体积合计（L1 体积行 vs L2
gross/clear_volume_m3）。
结果为研发自检口径（self_check=true），不作为结算或对量依据。

输入
  --quantity-report  s5 流水线 cad_quantity_report 出的 quantity_report.json
  --beam-objects     可选，beam_objects.json（目标图框梁标注，推荐给）
  --out-prefix       输出前缀（.md/.csv/.json）

用法
  python3 cad_member_audit.py --quantity-report quantity_report.json \
      --beam-objects beam_objects.json --out-prefix 构件校对
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

SCHEMA = "cad-member-audit/v0.1"

BEAM_CATS = {"梁", "beam"}


def norm_code(value) -> str:
    """构件编号归一：去空格、统一大写。"""
    return re.sub(r"\s+", "", str(value or "")).upper()


def base_code(normed: str) -> str:
    """去掉跨数/悬挑括号段与尾缀的构件主名：KL1(3A)→KL1。"""
    return re.sub(r"[(（].*?[)）]", "", normed)


def norm_section(value) -> str:
    """截面归一：250x600 / 250X600 / 250×600 → 250x600；数字统一去小数尾。"""
    text = str(value or "").strip().replace("×", "x").replace("X", "x").replace(" ", "")
    m = re.fullmatch(r"(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)", text)
    if m:
        b = float(m.group(1))
        h = float(m.group(2))
        return f"{b:g}x{h:g}"
    return text


def _f(value) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return 0.0
    return v if v > 0 else 0.0


def collect_beam_objects(bo: dict) -> dict[str, dict]:
    """beam_objects.json → L1 图面标注行（目标图框口径）。

    rows 是实例行（同编号可多根）：按 norm_code 聚合，记实例数、
    截面集合、中心线长集合、体积合计、标注来源集合。
    """
    l1: dict[str, dict] = {}
    for r in bo.get("rows") or []:
        code = norm_code(r.get("code"))
        if not code:
            continue
        rec = l1.setdefault(code, {
            "codes": set(), "sections": set(), "stirrups": set(),
            "observed": 0, "vol_m3": 0.0, "vol_rows": 0,
            "length_mm": set(), "spans": set(), "sources": set(),
        })
        rec["codes"].add(str(r.get("code") or ""))
        if r.get("section"):
            rec["sections"].add(norm_section(r.get("section")))
        rec["observed"] += 1  # 每行是一根实例
        vol = _f(r.get("volume_m3"))
        if vol:
            rec["vol_m3"] += vol
            rec["vol_rows"] += 1
        if r.get("length_mm"):
            rec["length_mm"].add(round(_f(r.get("length_mm"))))
        if r.get("annotation_source"):
            rec["sources"].add(str(r.get("annotation_source")))
    return l1


def collect_rows(report: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    """从 quantity_report 取 L1 图面索引行、L2 模型几何行（梁类）。

    返回 ({norm_code: 行聚合}, {norm_code: 行聚合})。同编号多行聚合：
    L1 记标注根数合计与截面集合，L2 记实例数与体积合计。
    """
    l1: dict[str, dict] = {}
    for r in report.get("component_schedule") or []:
        if (r.get("category") or "") not in BEAM_CATS:
            continue
        code = norm_code(r.get("code"))
        if not code:
            continue
        rec = l1.setdefault(code, {
            "codes": set(), "sections": set(), "stirrups": set(),
            "observed": 0, "vol_m3": 0.0, "vol_rows": 0,
            "length_mm": set(), "spans": set(),
        })
        rec["codes"].add(str(r.get("code") or ""))
        if r.get("section"):
            rec["sections"].add(norm_section(r.get("section")))
        if r.get("stirrup"):
            rec["stirrups"].add(str(r.get("stirrup")))
        rec["observed"] += int(_f(r.get("observed_count")) or 0)
        vol = _f(r.get("concrete_candidate_m3"))
        if vol:
            rec["vol_m3"] += vol
            rec["vol_rows"] += 1
        if r.get("length_mm"):
            rec["length_mm"].add(round(_f(r.get("length_mm"))))
        if r.get("span_count"):
            rec["spans"].add(str(r.get("span_count")))

    l2: dict[str, dict] = {}
    for r in report.get("beam_schedule") or []:
        code = norm_code(r.get("code") or r.get("base_code"))
        if not code:
            continue
        rec = l2.setdefault(code, {
            "codes": set(), "sections": set(), "instances": 0,
            "gross_m3": 0.0, "clear_m3": 0.0,
            "centerline_mm": set(), "support_counts": set(),
        })
        rec["codes"].add(str(r.get("code") or ""))
        if r.get("section"):
            rec["sections"].add(norm_section(r.get("section")))
        rec["instances"] += 1
        rec["gross_m3"] += _f(r.get("gross_volume_m3"))
        rec["clear_m3"] += _f(r.get("clear_volume_m3"))
        if r.get("centerline_length_mm"):
            rec["centerline_mm"].add(round(_f(r.get("centerline_length_mm"))))
        rec["support_counts"].add(int(_f(r.get("support_count")) or 0))
    return l1, l2


def audit(l1: dict[str, dict], l2: dict[str, dict]) -> dict:
    """五态判定 + 总量守恒。返回审计 dict（可 json 序列化的行先转字符串）。"""
    rows: list[dict] = []
    matched_codes = set(l1) & set(l2)

    # 先按精确编号比对，再对未匹中的按 base_code 兜底归并
    l1_by_base: dict[str, list[str]] = defaultdict(list)
    for code in l1:
        if code not in matched_codes:
            l1_by_base[base_code(code)].append(code)
    l2_by_base: dict[str, list[str]] = defaultdict(list)
    for code in l2:
        if code not in matched_codes:
            l2_by_base[base_code(code)].append(code)

    pairs: list[tuple[str | None, str | None]] = [(c, c) for c in matched_codes]
    used_l2: set[str] = set()
    for b, l1_codes in l1_by_base.items():
        hit = l2_by_base.get(b)
        if hit:
            for c1 in l1_codes:
                c2 = hit[0]
                used_l2.add(c2)
                pairs.append((c1, c2))
    unmatched_l1 = [c for cs in l1_by_base.values() for c in cs
                    if not l2_by_base.get(base_code(c))]
    unmatched_l2 = [c for c in l2 if c not in matched_codes and c not in used_l2]

    for c1, c2 in pairs:
        a, b = l1[c1], l2[c2]
        sec_a = sorted(a["sections"])
        sec_b = sorted(b["sections"])
        if sec_a and sec_b:
            if set(sec_a) & set(sec_b):
                state = "一致"
            else:
                state = "截面冲突"
        else:
            state = "规格残缺"
        rows.append({
            "state": state,
            "L1_code": "、".join(sorted(a["codes"])),
            "L2_code": "、".join(sorted(b["codes"])),
            "L1_截面": "、".join(sec_a) or "-",
            "L2_截面": "、".join(sec_b) or "-",
            "L1_标注根数": a["observed"],
            "L2_实例数": b["instances"],
            "L1_箍筋": "；".join(sorted(a["stirrups"])) or "-",
            "L1_候选体积m3": round(a["vol_m3"], 2) or None,
            "L2_毛体积m3": round(b["gross_m3"], 2),
            "L2_净体积m3": round(b["clear_m3"], 2),
            "L2_支座数": "、".join(str(x) for x in sorted(b["support_counts"])),
        })
    for c in unmatched_l1:
        a = l1[c]
        rows.append({
            "state": "图面有模型无",
            "L1_code": "、".join(sorted(a["codes"])), "L2_code": "",
            "L1_截面": "、".join(sorted(a["sections"])) or "-",
            "L2_截面": "-",
            "L1_标注根数": a["observed"], "L2_实例数": 0,
            "L1_箍筋": "；".join(sorted(a["stirrups"])) or "-",
            "L1_候选体积m3": round(a["vol_m3"], 2) or None,
            "L2_毛体积m3": None, "L2_净体积m3": None, "L2_支座数": "",
        })
    for c in unmatched_l2:
        b = l2[c]
        rows.append({
            "state": "模型有图面无",
            "L1_code": "", "L2_code": "、".join(sorted(b["codes"])),
            "L1_截面": "-", "L2_截面": "、".join(sorted(b["sections"])) or "-",
            "L1_标注根数": 0, "L2_实例数": b["instances"],
            "L1_箍筋": "-",
            "L1_候选体积m3": None,
            "L2_毛体积m3": round(b["gross_m3"], 2),
            "L2_净体积m3": round(b["clear_m3"], 2),
            "L2_支座数": "、".join(str(x) for x in sorted(b["support_counts"])),
        })

    order = {"截面冲突": 0, "规格残缺": 1, "图面有模型无": 2, "模型有图面无": 3, "一致": 4}
    rows.sort(key=lambda r: (order.get(r["state"], 9),
                             str(r["L1_code"] or r["L2_code"])))

    counts = defaultdict(int)
    for r in rows:
        counts[r["state"]] += 1
    l1_vol = round(sum(r["L1_候选体积m3"] or 0 for r in rows), 2)
    l2_vol = round(sum(r["L2_毛体积m3"] or 0 for r in rows), 2)
    return {
        "schema": SCHEMA,
        "self_check": True,
        "rows": rows,
        "summary": {
            "L1_图面索引编号数": len(l1),
            "L2_模型几何编号数": len(l2),
            "五态计数": dict(counts),
            "L1_候选体积合计m3": l1_vol,
            "L2_毛体积合计m3": l2_vol,
            "体积差m3": round(l2_vol - l1_vol, 2),
        },
    }


def render_md(audit_out: dict, title: str) -> str:
    md = StringIO()
    s = audit_out["summary"]
    l1_note = ("L1=图面标注（beam_objects.rows，目标图框内）"
               if s.get("L1_source") == "beam_objects"
               else "L1=图面索引（component_schedule，**全文件标注**，"
                    "覆盖缺口会混入其他图框的标注，建议补 --beam-objects 换目标图框口径）")
    md.write(f"# {title}（构件级三级校对）\n\n")
    md.write("> **口径声明**：self_check=true 的研发自检，不作为结算或对量口径。\n")
    md.write(f"> {l1_note}；L2=模型几何（beam_schedule，模型展开）。"
             "五态：一致 / 截面冲突 / 规格残缺 / 图面有模型无 / 模型有图面无。\n\n")
    md.write(f"- L1 图面标注编号：**{s['L1_图面索引编号数']}**；L2 模型几何编号：**{s['L2_模型几何编号数']}**\n")
    md.write(f"- 五态：{s['五态计数']}\n")
    md.write(f"- 体积守恒：L1 候选 {s['L1_候选体积合计m3']} m³ vs L2 毛 {s['L2_毛体积合计m3']} m³"
             f"（差 {s['体积差m3']} m³；L1 只有 index 行带候选体积，多为部分覆盖）\n\n")
    if s["五态计数"].get("截面冲突"):
        md.write("## ⚠️ 截面冲突明细\n\n")
        md.write("| L1编号 | L1截面 | L2编号 | L2截面 | L1根数 | L2实例 |\n|---|---|---|---|---|---|\n")
        for r in audit_out["rows"]:
            if r["state"] == "截面冲突":
                md.write(f"| {r['L1_code']} | {r['L1_截面']} | {r['L2_code']} | {r['L2_截面']} "
                         f"| {r['L1_标注根数']} | {r['L2_实例数']} |\n")
        md.write("\n")
    if s["五态计数"].get("图面有模型无") or s["五态计数"].get("模型有图面无"):
        md.write("## 覆盖缺口明细\n\n")
        md.write("| 状态 | 编号 | 截面 | L1根数 | L2实例 |\n|---|---|---|---|---|\n")
        for r in audit_out["rows"]:
            if r["state"] in ("图面有模型无", "模型有图面无"):
                code = r["L1_code"] or r["L2_code"]
                md.write(f"| {r['state']} | {code} | {r['L1_截面'] if r['L1_code'] else r['L2_截面']} "
                         f"| {r['L1_标注根数']} | {r['L2_实例数']} |\n")
        md.write("\n")
    md.write("## 全量对照表\n\n| 状态 | L1编号 | L1截面 | L1箍筋 | L2编号 | L2截面 | L2支座 | L1根数 | L2实例 | L1候选m³ | L2毛m³ | L2净m³ |\n"
             "|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in audit_out["rows"]:
        md.write(f"| {r['state']} | {r['L1_code']} | {r['L1_截面']} | {r['L1_箍筋']} "
                 f"| {r['L2_code']} | {r['L2_截面']} | {r['L2_支座数']} "
                 f"| {r['L1_标注根数']} | {r['L2_实例数']} "
                 f"| {r['L1_候选体积m3'] if r['L1_候选体积m3'] else '-'} "
                 f"| {r['L2_毛体积m3'] if r['L2_毛体积m3'] else '-'} "
                 f"| {r['L2_净体积m3'] if r['L2_净体积m3'] else '-'} |\n")
    return md.getvalue()


def build(report_path: str, out_prefix: str,
          beam_objects_path: str | None = None) -> Path:
    report = json.load(open(report_path, encoding="utf-8"))
    l1: dict[str, dict] = {}
    l1_source = "component_schedule"
    if beam_objects_path:
        bo = json.load(open(beam_objects_path, encoding="utf-8"))
        l1 = collect_beam_objects(bo)
        if l1:
            l1_source = "beam_objects"
    if not l1:
        # 未提供 beam_objects 或其为空 → 退回全文件标注索引（component_schedule）
        l1, l2 = collect_rows(report)
        if not l1 and not l2:
            raise SystemExit("❌ quantity_report.json 里没有梁构件行"
                             "（component_schedule.category=梁 或 beam_schedule 均为空）")
    else:
        _, l2 = collect_rows(report)
        if not l2:
            raise SystemExit("❌ quantity_report.json 的 beam_schedule 为空，没有模型几何行可对照")
    out = audit(l1, l2)
    out["summary"]["L1_source"] = l1_source
    out_base = Path(out_prefix)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    Path(str(out_base) + ".json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(str(out_base) + ".md").write_text(
        render_md(out, Path(report_path).stem), encoding="utf-8")
    csv_path = Path(str(out_base) + ".csv")
    cols = ["state", "L1_code", "L1_截面", "L1_箍筋", "L2_code", "L2_截面",
            "L2_支座数", "L1_标注根数", "L2_实例数", "L1_候选体积m3",
            "L2_毛体积m3", "L2_净体积m3"]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["状态"] + cols[1:])
        for r in out["rows"]:
            w.writerow([r.get(c) if r.get(c) is not None else "" for c in cols])
    print(f"[构件校对] L1源={l1_source} L1={out['summary']['L1_图面索引编号数']} "
          f"L2={out['summary']['L2_模型几何编号数']} 五态={out['summary']['五态计数']}")
    return csv_path


def main() -> None:
    raw = sys.argv[1:]
    ap = argparse.ArgumentParser(
        description="Member-level cross audit: drawn annotations vs model geometry")
    ap.add_argument("--quantity-report", required=True,
                    help="s5 cad_quantity_report 出的 quantity_report.json")
    ap.add_argument("--beam-objects", default=None,
                    help="beam_objects.json（目标图框梁标注，推荐的 L1 口径）")
    ap.add_argument("--out-prefix", required=True)
    a = ap.parse_args(raw)
    build(a.quantity_report, a.out_prefix, beam_objects_path=a.beam_objects)


if __name__ == "__main__":
    main()
