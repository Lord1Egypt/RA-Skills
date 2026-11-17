#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""钢筋吨位汇总：含筋率带 × 图面配筋构成 交叉核对。

两个口径、一张表：
  口径A（含筋率带）：土建算量（qty_core）出的 *-计划.csv，钢筋吨 = 混凝土净量 × 含筋率区间。
  口径B（图面配筋构成）：cad-file-reader 聚合 JSON 里的配筋标注，按直径×米重算「强度构成」，
    加权平均直径落在带内哪个位置 → 把 A 的带宽收窄成「建议区间」。

两带取交集作推荐区间；交集为空时明确说偏差方向，不硬凑一个数。
全部是估算带（final_quantity=false），不替代翻样、对量与结算。

输入
  --plan             qty_core 出的 *-计划.csv（构件类别,标号,混凝土m3,钢筋估算kg带低,钢筋估算kg带高）可多张
  --quantity-report  s5 流水线出的 quantity_report.json（cad_quantity_report.py 产物），与 --plan 二选一
  --aggregate        project_aggregate JSON（cad-project-aggregate/v1，含 rebars / rebar_by_floor）
  --rules            口径.json（默认 ../rules/口径.json）

用法
  python3 rebar_tonnage.py --plan 三层-计划.csv --aggregate aggregate.json --out-prefix 钢筋吨位
  python3 rebar_tonnage.py --quantity-report quantity_report.json --out-prefix 钢筋吨位
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i18n  # noqa: E402

# 米重公式与 rules/口径.json「钢筋.米重公式」一致：0.00617*d^2 kg/m
def unit_weight(dia_mm: float) -> float:
    return 0.00617 * dia_mm * dia_mm


def load_plan(paths: list[str]) -> list[dict]:
    """qty_core 的 *-计划.csv：构件类别,标号,混凝土m3,型数,钢筋估算kg带低,钢筋估算kg带高,订货量m3,钢筋估算t"""
    rows: list[dict] = []
    for p in paths:
        with open(p, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                try:
                    vol = float(r.get("混凝土m3") or 0)
                    lo = float(r.get("钢筋估算kg带低") or 0)
                    hi = float(r.get("钢筋估算kg带高") or 0)
                except (TypeError, ValueError):
                    continue
                if vol <= 0 and lo <= 0 and hi <= 0:
                    continue
                rows.append({"来源": Path(p).name, "构件类别": (r.get("构件类别") or "").strip(),
                             "标号": (r.get("标号") or "").strip(), "混凝土m3": vol,
                             "kg低": lo, "kg高": hi})
    return rows


def load_quantity_report(path: str) -> list[dict]:
    """s5 cad_quantity_report 出的 quantity_report.json → 计划行。

    口径（防重复计数）：component_schedule（scan.members）里某类别有
    concrete_candidate_m3 的行就只算它；该类别一行体积都没有时才走
    模型兜底——梁用 beam_schedule 的 gross/clear_volume_m3（模型几何展开），
    板用 slab_schedule 的 volume_m3。column_schedule 是 component_schedule
    的柱子集，永不重复计入。
    """
    data = json.load(open(path, encoding="utf-8"))
    rows: list[dict] = []
    seen: set[tuple[str, str]] = set()
    cats_with_volume: set[str] = set()

    def add(cat: str, code: str, vol, src_note: str) -> None:
        try:
            vol = float(vol or 0)
        except (TypeError, ValueError):
            vol = 0.0
        key = (cat, code)
        if key in seen or vol <= 0:
            return
        seen.add(key)
        cats_with_volume.add(cat)
        rows.append({"来源": f"{Path(path).name}:{src_note}", "构件类别": cat,
                     "标号": code, "混凝土m3": vol, "kg低": 0.0, "kg高": 0.0})

    for r in data.get("component_schedule") or []:
        add((r.get("category") or "?").strip(), (r.get("code") or "?").strip(),
            r.get("concrete_candidate_m3"), "component_schedule")
    if "梁" not in cats_with_volume:
        for r in data.get("beam_schedule") or []:
            add("梁", (r.get("code") or r.get("id") or "?").strip(),
                r.get("clear_volume_m3") or r.get("gross_volume_m3"),
                "beam_schedule")
    if "板" not in cats_with_volume:
        for r in data.get("slab_schedule") or []:
            add("板", (r.get("id") or r.get("code") or "?").strip(),
                r.get("volume_m3"), "slab_schedule")
    return rows


# 下料增值系数带（锚固+搭接+弯钩摊销；参照 22G101 平法构造量级的计划口径估计，
# 不是翻样）。真实下料需构件级配筋解析（锚固长度 laE、定尺接头、弯钩 11.9d 等），
# 属另一类专业软件；这里只给「吨位 → 下料重量」的系数带。
CUT_FACTORS = {
    "梁": (1.06, 1.12),   # 纵筋锚固 15d×2 + 定尺搭接摊销
    "板": (1.03, 1.08),   # 板筋锚固少、搭接为主
    "柱": (1.05, 1.11),   # 纵筋接头多（层间搭接/机械连接摊销）
    "墙": (1.04, 1.10),
    "基础": (1.03, 1.07),
    "楼梯": (1.05, 1.12),
}
CUT_DEFAULT = (1.05, 1.12)


def cutting_estimate(a_rows: list[dict]) -> dict:
    """口径A 分类别吨位带 × 下料系数带 → 下料重量带（计划口径，final_quantity=false）。"""
    rows = []
    tot_lo = tot_hi = 0.0
    for r in a_rows:
        cat = r.get("构件类别") or "未分类"
        t_lo, t_hi = r.get("钢筋t带") or (0.0, 0.0)
        if not (t_lo or t_hi):
            continue
        f_lo, f_hi = CUT_FACTORS.get(cat, CUT_DEFAULT)
        c_lo, c_hi = round(t_lo * f_lo, 3), round(t_hi * f_hi, 3)
        rows.append({"构件类别": cat, "吨位带t": [t_lo, t_hi],
                     "下料系数带": [f_lo, f_hi], "下料重量带t": [c_lo, c_hi]})
        tot_lo += c_lo
        tot_hi += c_hi
    return {"rows": rows, "total": [round(tot_lo, 3), round(tot_hi, 3)],
            "final_quantity": False}


def band_a(plan_rows: list[dict], rules: dict) -> tuple[dict, list[dict]]:
    """口径A：按构件类别汇总混凝土量 × 含筋率区间。返回 (总带, 分类别行)。"""
    ratios = (rules.get("构件") or {})
    per_cat: dict[str, dict] = defaultdict(lambda: {"混凝土m3": 0.0, "kg低": 0.0, "kg高": 0.0,
                                                    "来源": set()})
    missing_ratio: set[str] = set()
    for r in plan_rows:
        cat = r["构件类别"] or "未分类"
        band = (ratios.get(cat) or {}).get("含筋率区间kg_per_m3")
        rec = per_cat[cat]
        rec["混凝土m3"] += r["混凝土m3"]
        rec["来源"].add(r["来源"])
        if band:
            rec["kg低"] += r["混凝土m3"] * band[0]
            rec["kg高"] += r["混凝土m3"] * band[1]
        else:
            # 计划 CSV 自带带（qty_core 已算过）就用它，再提示规则里没有该类别
            missing_ratio.add(cat)
            rec["kg低"] += r["kg低"]
            rec["kg高"] += r["kg高"]
    rows = []
    for cat, rec in per_cat.items():
        rows.append({"构件类别": cat, "混凝土m3": round(rec["混凝土m3"], 2),
                     "钢筋kg带": [round(rec["kg低"]), round(rec["kg高"])],
                     "钢筋t带": [round(rec["kg低"] / 1000, 2), round(rec["kg高"] / 1000, 2)],
                     "来源": "；".join(sorted(rec["来源"]))})
    rows.sort(key=lambda x: -x["混凝土m3"])
    total_lo = round(sum(r["钢筋kg带"][0] for r in rows) / 1000, 2)
    total_hi = round(sum(r["钢筋kg带"][1] for r in rows) / 1000, 2)
    return {"t低": total_lo, "t高": total_hi, "缺含筋率类别": sorted(missing_ratio)}, rows


def _dia_from_spec(spec: str) -> int | None:
    """从配筋型号原文解直径：6@100/200(2)→6；3Ⅲ25/3C25/3Φ25→25。"""
    text = str(spec or "").strip()
    if not text:
        return None
    # 先取「符号后跟数字」形态（3Ⅲ25 / C12 / Φ8），否则取 @ 前的数字（6@100）
    m = re.search(r"[ⅢΦ℃A-Ga-g](\d{1,2})(?!\d)", text)
    if not m:
        m = re.search(r"(\d{1,2})\s*@", text)
    if not m:
        return None
    try:
        dia = int(m.group(1))
    except ValueError:
        return None
    return dia if 4 <= dia <= 50 else None


def aggregate_from_scan(scan: dict) -> dict:
    """cad_scan 的 rebar_summary（箍筋/纵筋型号表）→ 口径B 的 aggregate 形态。

    每个型号按直径归并，count=构件型数（标注次数口径，与 project_aggregate 的
    rebars.count 同义）；grade 从符号猜：Ⅲ/C→HRB400，B→HRB335，A/Φ→HPB300，
    其余 unknown。适合 s5 产物直接喂口径B，无需回识图/聚合入口。
    """
    grades_map = [("Ⅲ", "HRB400"), ("C", "HRB400"), ("B", "HRB335"),
                  ("A", "HPB300"), ("Φ", "HPB300")]
    agg: dict[tuple[int, str], int] = defaultdict(int)
    for rows in (scan.get("rebar_summary") or {}).values():
        for r in rows or []:
            spec = str(r.get("型号") or "")
            dia = _dia_from_spec(spec)
            if dia is None:
                continue
            grade = "unknown"
            for sym, g in grades_map:
                if sym in spec:
                    grade = g
                    break
            n = int(r.get("构件型数") or 0) or 1
            agg[(dia, grade)] += n
    return {"rebars": [
        {"diameter": dia, "grade": grade, "count": count,
         "drawings": ["cad_scan.rebar_summary"], "source": "cad_scan.rebar_summary"}
        for (dia, grade), count in sorted(agg.items(), key=lambda kv: (-kv[1], kv[0][0]))
    ]}


def _floor_rows(aggregate: dict, floor: str) -> list[dict] | None:
    """从 rebar_by_floor 取指定层的配筋行；宽松匹配（精确→双向包含），找不到返回 None。"""
    rows = aggregate.get("rebar_by_floor") or []
    if not rows or not floor:
        return None
    exact = [r for r in rows if (r.get("floor") or "") == floor]
    if exact:
        return exact
    loose = [r for r in rows
             if floor in (r.get("floor") or "") or (r.get("floor") or "") in floor]
    return loose or None


def rebar_profile(aggregate: dict, floor: str | None = None) -> dict:
    """口径B 输入：各直径的标注次数、强度指数（次数×米重）、加权平均直径。

    强度指数不是吨位——标注次数既不是根数也没有长度——但比「出现次数」更接近
    吨位构成：Φ25 一条标注顶 Φ8 一条的 9.8 倍米重。加权平均直径决定 A 带内位置。

    floor 给定时优先用 rebar_by_floor 里该层的行（单层口径B，不再借用全图构成）；
    该层无配筋行则回退全图 rebars 并在 profile.floor_source 标注。
    """
    out = {"rows": [], "weighted_dia": None, "total_count": 0,
           "floor": floor, "floor_source": None}
    floor_rows = _floor_rows(aggregate, floor) if floor else None
    if floor_rows is not None:
        out["floor_source"] = "rebar_by_floor"
        agg = {}
        for r in floor_rows:
            dia = r.get("diameter")
            try:
                dia = int(dia)
            except (TypeError, ValueError):
                continue
            if not (4 <= dia <= 50):
                continue
            n = int(r.get("count") or 0)
            agg.setdefault(dia, {"n": 0, "grades": defaultdict(int)})
            agg[dia]["n"] += n
            for g, c in (r.get("grades") or {}).items():
                agg[dia]["grades"][g] += int(c or 0)
        entries = [{"diameter": d, "count": v["n"],
                    "grade": "；".join(f"{k}×{c}" for k, c in
                                      sorted(v["grades"].items(), key=lambda kv: -kv[1]))
                        or "unknown"}
                   for d, v in agg.items() if v["n"] > 0]
        src_rows = entries
    else:
        if floor:
            out["floor_source"] = "global_fallback"
        src_rows = aggregate.get("rebars") or []
    if not src_rows:
        return out
    tot_w = 0.0
    tot_wd = 0.0
    for r in src_rows:
        dia = r.get("diameter")
        try:
            dia = int(dia)
        except (TypeError, ValueError):
            continue
        if not (4 <= dia <= 50):
            continue
        n = int(r.get("count") or 0)
        uw = unit_weight(dia)
        w = n * uw
        out["rows"].append({"直径": f"Φ{dia}", "牌号": r.get("grade") or "unknown",
                            "标注次数": n, "米重kg/m": round(uw, 3),
                            "强度指数": round(w, 1),
                            "涉及图纸数": len(r.get("drawings") or [])})
        out["total_count"] += n
        tot_w += w
        tot_wd += w * dia
    out["rows"].sort(key=lambda x: -x["强度指数"])
    out["weighted_dia"] = round(tot_wd / tot_w, 1) if tot_w > 0 else None
    return out


def band_position(weighted_dia: float) -> float:
    """加权平均直径 → 含筋率带内位置 [0,1]。

    经验锚点（文档级假设，非规范）：板筋以 Φ8~Φ12 为主 → 带下段；
    梁柱纵筋 Φ16~Φ25 占主导 → 带中上段。线性映射 d=10 → 0.0，d=22 → 1.0。
    """
    if weighted_dia is None:
        return None
    p = (weighted_dia - 10.0) / (22.0 - 10.0)
    return round(min(max(p, 0.0), 1.0), 3)


def band_b(band_a_t: tuple[float, float], p: float | None) -> tuple[float, float] | None:
    """口径B：把 A 带按位置 p 收窄成 ±1/6 带宽的建议区间（约 ±1/3 带宽）。"""
    if p is None:
        return None
    lo, hi = band_a_t
    width = hi - lo
    if width <= 0:
        return (lo, hi)
    c = lo + p * width
    half = width / 6.0
    return (round(max(lo, c - half), 2), round(min(hi, c + half), 2))


def overlap(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float] | None:
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    return (round(lo, 2), round(hi, 2)) if hi >= lo else None


def build(plan_paths: list[str], aggregate_path: str | None, rules_path: str | None,
          out_prefix: str, fmt: str = "all",
          quantity_report_path: str | None = None,
          floor: str | None = None,
          scan_rebar_path: str | None = None) -> Path:
    rules = {}
    if rules_path:
        rules = json.load(open(rules_path, encoding="utf-8"))
    source_kind = "plan"
    plan_rows = load_plan(plan_paths) if plan_paths else []
    if quantity_report_path:
        qr_rows = load_quantity_report(quantity_report_path)
        if not qr_rows:
            raise SystemExit("❌ quantity_report.json 里没有可用体积行"
                             "（需 component_schedule.concrete_candidate_m3 或 slab_schedule.volume_m3）")
        plan_rows += qr_rows
        source_kind = "quantity_report"
    if not plan_rows:
        raise SystemExit("❌ 没有输入或没有可用行：--plan（qty_core *-计划.csv）"
                         " 或 --quantity-report（s5 quantity_report.json）二选一")
    aggregate = {}
    if aggregate_path:
        aggregate = json.load(open(aggregate_path, encoding="utf-8"))
    elif scan_rebar_path:
        # s5 cad_scan.json 的 rebar_summary → 口径B（无 project_aggregate 时的轻量路线）
        aggregate = aggregate_from_scan(json.load(open(scan_rebar_path, encoding="utf-8")))

    a_total, a_rows = band_a(plan_rows, rules)
    a_band = (a_total["t低"], a_total["t高"])
    profile = rebar_profile(aggregate, floor=floor)
    p = band_position(profile.get("weighted_dia"))
    b_band = band_b(a_band, p)
    inter = overlap(a_band, b_band) if b_band else None

    from io import StringIO
    md = StringIO()
    md.write("# 钢筋吨位汇总（估算带）\n\n")
    md.write("> **口径声明**：估算带口径（±20~30%），final_quantity=false；不替代翻样、下料、对量与结算。\n")
    md.write("> 口径A＝混凝土净量×含筋率区间（rules/口径.json）；口径B＝图面配筋构成把 A 带收窄的建议区间；推荐区间取两带交集。\n\n")
    if b_band:
        src_note = ""
        if profile.get("floor"):
            if profile.get("floor_source") == "rebar_by_floor":
                src_note = f"（口径B 取 **{profile['floor']}** 层配筋行，非全图构成）"
            else:
                src_note = f"（⚠️ rebar_by_floor 无「{profile['floor']}」层配筋行，口径B 回退全图构成）"
        md.write(f"- 口径A 总带：**{a_band[0]}~{a_band[1]} t**\n")
        md.write(f"- 图面配筋加权平均直径：**Φ{profile['weighted_dia']}**（强度构成加权）→ 带内位置 {p}{src_note}\n")
        md.write(f"- 口径B 建议区间：**{b_band[0]}~{b_band[1]} t**\n")
        if inter:
            md.write(f"- **推荐区间（两带交集）：{inter[0]}~{inter[1]} t**\n")
        else:
            md.write(f"- ⚠️ 两带无交集：口径B 在 A 带{'上方' if b_band[0] > a_band[1] else '下方'}，"
                     f"说明图面配筋直径构成偏{'大' if b_band[0] > a_band[1] else '小'}，"
                     f"先核对含筋率取值与配筋标注归属，再人工定值\n")
    else:
        md.write("- 口径B：未提供聚合 JSON 或无有效配筋标注，只有口径A\n")
    if a_total["缺含筋率类别"]:
        zero_cats = [r["构件类别"] for r in a_rows
                     if r["构件类别"] in a_total["缺含筋率类别"]
                     and r["钢筋kg带"] == [0, 0] and r["混凝土m3"] > 0]
        if zero_cats and source_kind == "quantity_report":
            md.write(f"- ⚠️ 规则里没有含筋率区间的类别：{'、'.join(a_total['缺含筋率类别'])}"
                     f"；其中 **{'、'.join(zero_cats)} 有混凝土量但钢筋贡献为 0**"
                     f"（quantity_report 路径没有自带带，需先补 rules/口径.json 或改走 --plan）\n")
        else:
            md.write(f"- ⚠️ 规则里没有含筋率区间的类别：{'、'.join(a_total['缺含筋率类别'])}（已沿用计划 CSV 自带带）\n")
    md.write("\n## 按构件类别（口径A）\n\n| 构件类别 | 混凝土m3 | 钢筋kg带 | 钢筋t带 | 来源 |\n|---|---|---|---|---|\n")
    for r in a_rows:
        md.write(f"| {r['构件类别']} | {r['混凝土m3']} | {r['钢筋kg带'][0]}~{r['钢筋kg带'][1]} "
                 f"| {r['钢筋t带'][0]}~{r['钢筋t带'][1]} | {r['来源']} |\n")
    if profile["rows"]:
        md.write("\n## 图面配筋构成（口径B 依据）\n\n| 直径 | 牌号 | 标注次数 | 米重kg/m | 强度指数 | 占比% | 涉及图纸数 |\n|---|---|---|---|---|---|---|\n")
        tot_i = sum(r["强度指数"] for r in profile["rows"]) or 1.0
        for r in profile["rows"][:15]:
            md.write(f"| {r['直径']} | {r['牌号']} | {r['标注次数']} | {r['米重kg/m']} "
                     f"| {r['强度指数']} | {round(r['强度指数']/tot_i*100,1)} | {r['涉及图纸数']} |\n")
        md.write(f"\n（强度指数＝标注次数×米重，是构成指标不是吨位；共 {profile['total_count']} 条标注）\n")
    floor_rows = aggregate.get("rebar_by_floor") or []
    if floor_rows:
        md.write("\n## 每层直径分布\n\n| 楼层 | 直径 | 牌号构成 | 出现次数 |\n|---|---|---|---|\n")
        for r in floor_rows[:40]:
            grades = r.get("grades") or {}
            gtxt = "；".join(f"{k}×{v}" for k, v in sorted(grades.items(), key=lambda kv: -kv[1])[:3]) or "?"
            dia = r.get("diameter")
            md.write(f"| {r.get('floor', '?')} | Φ{dia if dia is not None else '?'} | {gtxt} | {r.get('count', 0)} |\n")
        if len(floor_rows) > 40:
            md.write(f"\n（其余 {len(floor_rows) - 40} 行见聚合 JSON 的 rebar_by_floor）\n")

    cut = cutting_estimate(a_rows)
    if cut["rows"]:
        md.write("\n## 下料重量估算带（计划口径）\n\n")
        md.write("> 下料带＝口径A 吨位带 × 下料系数带（锚固/搭接/弯钩摊销，22G101 量级估计）。"
                 "**不是翻样**；若采用推荐区间，可同比例缩放。final_quantity=false。\n\n")
        md.write("| 构件类别 | 吨位带t | 下料系数带 | 下料重量带t |\n|---|---|---|---|\n")
        for r in cut["rows"]:
            md.write(f"| {r['构件类别']} | {r['吨位带t'][0]}~{r['吨位带t'][1]} "
                     f"| {r['下料系数带'][0]}~{r['下料系数带'][1]} "
                     f"| {r['下料重量带t'][0]}~{r['下料重量带t'][1]} |\n")
        md.write(f"\n- **下料重量总带：{cut['total'][0]}~{cut['total'][1]} t**\n")

    out_base = Path(out_prefix)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    Path(str(out_base) + ".md").write_text(md.getvalue(), encoding="utf-8")

    csv_path = Path(str(out_base) + ".csv")
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["口径", "t低", "t高", "说明"])
        w.writerow(["口径A 含筋率带", a_band[0], a_band[1], "混凝土净量×含筋率区间"])
        if b_band:
            w.writerow(["口径B 图面构成建议", b_band[0], b_band[1],
                        f"加权平均直径 Φ{profile['weighted_dia']} → 带内位置 {p}"])
            if inter:
                w.writerow(["推荐区间(交集)", inter[0], inter[1], "两口径重叠"])
            else:
                w.writerow(["推荐区间", "", "", "两带无交集，需人工核对"])
        for r in a_rows:
            w.writerow([f"口径A-{r['构件类别']}", r["钢筋t带"][0], r["钢筋t带"][1],
                        f"{r['混凝土m3']} m3"])
        for r in cut.get("rows", []):
            w.writerow([f"下料-{r['构件类别']}", r["下料重量带t"][0], r["下料重量带t"][1],
                        f"系数 {r['下料系数带'][0]}~{r['下料系数带'][1]}（计划口径非翻样）"])
        w.writerow(["下料重量总带", cut["total"][0], cut["total"][1],
                    "口径A×下料系数带；final_quantity=false"])
        for r in profile["rows"][:15]:
            w.writerow([f"构成-{r['直径']}", r["标注次数"], r["强度指数"],
                        f"牌号 {r['牌号']}；强度指数=次数×米重，非吨位"])

    xlsx_path = Path(str(out_base) + ".xlsx")
    if fmt in ("all", "xlsx"):
        try:
            from openpyxl import Workbook
        except ImportError:
            print("[输出] 无 openpyxl，已给 CSV/MD")
            return csv_path
        wb = Workbook()
        ws = wb.active
        ws.title = "钢筋吨位"
        ws.append(["口径", "t低", "t高", "说明"])
        ws.append(["口径A 含筋率带", a_band[0], a_band[1], "混凝土净量×含筋率区间（估算带）"])
        if b_band:
            ws.append(["口径B 图面构成建议", b_band[0], b_band[1],
                       f"加权平均直径 Φ{profile['weighted_dia']} → 带内位置 {p}"])
            ws.append(["推荐区间(交集)", *(inter or ("", "")),
                       "两带无交集，需人工核对" if not inter else "两口径重叠"])
        for r in a_rows:
            ws.append([f"口径A-{r['构件类别']}", r["钢筋t带"][0], r["钢筋t带"][1],
                       f"{r['混凝土m3']} m3｜{r['来源']}"])
        ws.append([])
        ws.append(["直径", "牌号", "标注次数", "米重kg/m", "强度指数", "涉及图纸数"])
        for r in profile["rows"]:
            ws.append([r["直径"], r["牌号"], r["标注次数"], r["米重kg/m"],
                       r["强度指数"], r["涉及图纸数"]])
        ws.append([])
        ws.append(["口径声明", "估算带（±20~30%），final_quantity=false，不替代翻样/对量/结算"])
        wb.save(xlsx_path)
        print(f"已写入: {xlsx_path}")
    return csv_path


def main() -> None:
    raw = sys.argv[1:]
    lang = i18n.argv_lang(raw)
    desc = ("Rebar tonnage band: ratio band x drawn-rebar composition cross-check"
            if lang == "en" else "钢筋吨位汇总：含筋率带 × 图面配筋构成 交叉核对")
    ap = argparse.ArgumentParser(description=desc)
    i18n.add_lang_arg(ap, default=lang)
    ap.add_argument("--plan", nargs="+", default=None,
                    help="qty_core 出的 *-计划.csv（可多张）；与 --quantity-report 二选一"
                    if lang == "zh" else "qty_core plan CSV(s)")
    ap.add_argument("--quantity-report", default=None,
                    help="s5 流水线 quantity_report.json（cad_quantity_report.py 产物）"
                    if lang == "zh" else "s5 quantity_report.json")
    ap.add_argument("--aggregate", default=None,
                    help="project_aggregate JSON（cad-project-aggregate/v1）" if lang == "zh"
                    else "project_aggregate JSON")
    ap.add_argument("--floor", default=None,
                    help="单层口径B：按该楼层过滤 rebar_by_floor 的配筋行（找不到回退全图并提示）"
                    if lang == "zh" else "filter rebar_by_floor by floor name")
    ap.add_argument("--scan-rebar", default=None,
                    help="s5 cad_scan.json：用 rebar_summary 的型号表喂口径B"
                    "（与 --aggregate 二选一）" if lang == "zh"
                    else "s5 cad_scan.json rebar_summary for profile B")
    ap.add_argument("--rules", default=str(Path(__file__).resolve().parent.parent / "rules/口径.json"))
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--fmt", choices=("all", "csv", "xlsx"), default="all")
    a = ap.parse_args(raw)
    if not a.plan and not a.quantity_report:
        ap.error("--plan 与 --quantity-report 至少给一个")
    build(a.plan or [], a.aggregate, a.rules, a.out_prefix, a.fmt,
          quantity_report_path=a.quantity_report, floor=a.floor,
          scan_rebar_path=a.scan_rebar)


if __name__ == "__main__":
    main()
