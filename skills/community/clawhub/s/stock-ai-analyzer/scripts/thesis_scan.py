#!/usr/bin/env python3
"""Deterministic thesis & anomaly scanner over an a-stock-analyzer evidence pack.

This script ONLY surfaces — it computes growth/valuation/quality metrics against
fixed thresholds and emits (1) candidate investment-thesis archetypes (including
the 预期差 sub-types A1/A2/B) and (2) anomaly flags, each with a suggested probe
(which原文/dataset to pull next). It makes NO buy/sell or "cheap/expensive"
judgement — confirming a thesis, attributing a cause and all wording are the
model's job, per references/deep_mode.md.

Usage:
    python scripts/thesis_scan.py --evidence reports/evidence_688213.json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# --- thresholds (deterministic surfacing knobs; not judgements) -------------- #
T = {
    "growth_cagr_strong": 15.0,        # %: revenue/profit CAGR worth a growth thesis
    "yoy_surge": 50.0,                 # %: |YoY| beyond this = 暴增/暴跌 flag
    "pe_pct_low": 30.0,                # valuation percentile considered low
    "pe_abs_cheap": 25.0,              # absolute PE-TTM considered low
    "pe_abs_elevated": 30.0,           # absolute PE-TTM considered elevated
    "ocf_ni_weak": 0.5,                # OCF/净利 below this = 利润含金量弱
    "margin_swing_pct": 3.0,           # pct-point gross/net margin change to flag
    "recv_vs_rev_gap": 15.0,           # pct: 应收增速 - 营收增速 gap to flag
    "inv_vs_rev_gap": 15.0,            # pct: 存货增速 - 营收增速 gap to flag
    "inv_to_rev_high": 35.0,           # %: inventory/annual revenue high watermark
    "goodwill_to_eqt": 30.0,           # %: 商誉/净资产 impairment-risk watermark
    "debt_to_assets_high": 70.0,      # %: 资产负债率 (非金融) watermark
    "dedt_divergence": 0.7,            # 扣非/归母 below this = 利润质量存疑
    "rd_intensity_rise": 1.0,          # pct-point rise in 研发/营收 = option signal
}


def to_num(value: Any) -> Optional[float]:
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return f if not math.isnan(f) else None


def dataset(evidence: dict, name: str) -> Any:
    entry = (evidence.get("datasets") or {}).get(name)
    if isinstance(entry, dict):
        if entry.get("ok") is False:
            return None
        return entry.get("data", entry)
    return entry


def annual_rows(rows: List[dict]) -> List[dict]:
    # Dedup by end_date (Tushare returns restated/duplicate rows); last wins.
    by_end: Dict[str, dict] = {}
    for r in rows:
        if isinstance(r, dict) and str(r.get("end_date", "")).endswith("1231"):
            by_end[str(r.get("end_date"))] = r
    return [by_end[k] for k in sorted(by_end)]


def cagr(first: Optional[float], last: Optional[float], periods: int) -> Optional[float]:
    if first is None or last is None or first <= 0 or last <= 0 or periods < 1:
        return None
    return (pow(last / first, 1.0 / periods) - 1.0) * 100.0


def latest_window(band: dict, metric: str) -> Dict[str, Any]:
    """Return the longest available percentile window for a metric."""
    m = (band or {}).get(metric) or {}
    windows = m.get("windows") or {}
    for key in ("5y", "3y", "1y"):
        if windows.get(key) and windows[key].get("sample_size"):
            return {"window": key, **windows[key], "current": m.get("current")}
    return {"current": m.get("current")}


# --- people & governance surfacing (facts only; NO judgement) ---------------- #
# Core roles whose turnover is worth surfacing to the model (it decides meaning).
CORE_TITLES = ("董事长", "总经理", "总裁", "财务总监", "董事会秘书", "CEO", "首席")
# holder_type substrings that mark an institutional holder (vs natural person / 一般企业).
INSTITUTIONAL_TYPES = ("基金", "社保", "保险", "QFII", "信托", "资管", "养老", "证券公司")


def _year(value: Any) -> Optional[int]:
    s = str(value or "")
    return int(s[:4]) if len(s) >= 4 and s[:4].isdigit() else None


def _is_core_title(title: Any) -> bool:
    t = str(title or "")
    return any(c in t for c in CORE_TITLES)


def build_people_governance(evidence: dict, ts_code: Optional[str]) -> Dict[str, Any]:
    """Surface deterministic people/governance facts from managers / rewards /
    top10-holders / holder-trade. This makes NO good/bad call — it only摆事实
    and suggests which公告/联网 to pull next (probes). All judgement is the
    model's job per references/growth_success_rate.md."""
    ds = lambda n: dataset(evidence, n)  # noqa: E731
    managers = ds("managers") if isinstance(ds("managers"), list) else []
    rewards = ds("rewards") if isinstance(ds("rewards"), list) else []
    top10 = ds("top10-holders") if isinstance(ds("top10-holders"), list) else []
    htrade = ds("holder-trade") if isinstance(ds("holder-trade"), list) else []
    company = ds("company") if isinstance(ds("company"), dict) else {}
    income = ds("income") if isinstance(ds("income"), list) else []

    # ---- management stability (from managers begin/end) ----
    seen = set()
    mrows: List[dict] = []
    for r in managers:
        if not isinstance(r, dict):
            continue
        key = (r.get("name"), r.get("title"), r.get("begin_date"), r.get("end_date"))
        if key in seen:
            continue
        seen.add(key)
        mrows.append(r)
    in_office = [r for r in mrows if not r.get("end_date")]
    departed = [r for r in mrows if r.get("end_date")]
    core_departures = [
        {"name": r.get("name"), "title": r.get("title"), "end_date": r.get("end_date")}
        for r in departed if _is_core_title(r.get("title"))
    ]
    birth_years = [y for r in mrows if (y := _year(r.get("birthday"))) is not None]
    management = {
        "rows_available": len(mrows),
        "in_office_count": len(in_office),
        "departed_in_sample": len(departed),
        "core_role_departures": core_departures,
        "birth_year_range": [min(birth_years), max(birth_years)] if birth_years else None,
        "missing_birthday": sum(1 for r in mrows if _year(r.get("birthday")) is None),
    }

    # ---- interest alignment (chairman/manager holdings & pay from rewards) ----
    chairman = (company.get("chairman") or "").strip()
    manager = (company.get("manager") or "").strip()
    rw_by_name: Dict[str, dict] = {}
    for r in rewards:
        if not isinstance(r, dict) or r.get("name") is None:
            continue
        nm = r.get("name")
        prev = rw_by_name.get(nm)
        if prev is None or str(r.get("ann_date", "")) >= str(prev.get("ann_date", "")):
            rw_by_name[nm] = r

    def reward_of(name: str) -> Optional[dict]:
        r = rw_by_name.get(name)
        if not r:
            return None
        return {"title": r.get("title"), "reward": to_num(r.get("reward")),
                "hold_vol": to_num(r.get("hold_vol"))}

    key_execs = []
    for nm, r in rw_by_name.items():
        if _is_core_title(r.get("title")):
            key_execs.append({"name": nm, "title": r.get("title"),
                              "reward": to_num(r.get("reward")),
                              "hold_vol": to_num(r.get("hold_vol"))})
    alignment = {
        "chairman": chairman or None,
        "chairman_eq_manager": bool(chairman and chairman == manager),
        "chairman_reward_hold": reward_of(chairman) if chairman else None,
        "key_execs": key_execs[:8],
    }

    # ---- ownership concentration & balance (latest top10 snapshot) ----
    by_end: Dict[str, List[dict]] = {}
    for r in top10:
        if isinstance(r, dict) and r.get("end_date"):
            by_end.setdefault(str(r.get("end_date")), []).append(r)
    ends = sorted(by_end)
    latest = by_end[ends[-1]] if ends else []
    prior = by_end[ends[-2]] if len(ends) >= 2 else []

    def inst_ratio(holders: List[dict]) -> Optional[float]:
        if not holders:
            return None
        s = 0.0
        for h in holders:
            t = str(h.get("holder_type") or "")
            if any(k in t for k in INSTITUTIONAL_TYPES):
                s += to_num(h.get("hold_ratio")) or 0.0
        return round(s, 2)

    ranked = sorted(latest, key=lambda h: to_num(h.get("hold_ratio")) or 0.0, reverse=True)
    top1 = ranked[0] if ranked else {}
    top2 = ranked[1] if len(ranked) > 1 else {}
    r1 = to_num(top1.get("hold_ratio")) if top1 else None
    r2 = to_num(top2.get("hold_ratio")) if top2 else None
    ownership = {
        "as_of": ends[-1] if ends else None,
        "top1": {"name": top1.get("holder_name"), "ratio": r1, "type": top1.get("holder_type")} if top1 else None,
        "top2_ratio": r2,
        "top1_top2_gap": round(r1 - r2, 2) if (r1 is not None and r2 is not None) else None,
        "chairman_in_top_holders": bool(chairman and any(chairman == h.get("holder_name") for h in latest)),
        "institutional_ratio": inst_ratio(latest),
        "institutional_ratio_prior": inst_ratio(prior),
    }

    # ---- important-shareholder trades (holder-trade) ----
    def _dir(r: dict) -> str:
        return str(r.get("in_de") or "").upper()
    ins = [r for r in htrade if isinstance(r, dict) and _dir(r) == "IN"]
    outs = [r for r in htrade if isinstance(r, dict) and _dir(r) in ("DE", "OUT")]

    def vol_sum(rows: List[dict]) -> float:
        return round(sum(to_num(r.get("change_vol")) or 0.0 for r in rows), 0)

    shareholder_actions = {
        "records": len([r for r in htrade if isinstance(r, dict)]),
        "increase_count": len(ins), "increase_vol": vol_sum(ins),
        "decrease_count": len(outs), "decrease_vol": vol_sum(outs),
    }

    # ---- organization & talent density (D 子框架的可算部分；事实，非判断) ----
    ann_inc_pg = annual_rows(income)
    latest_inc = ann_inc_pg[-1] if ann_inc_pg else {}
    employees = to_num(company.get("employees"))
    rev = to_num(latest_inc.get("revenue"))
    rd = to_num(latest_inc.get("rd_exp"))
    organization = {
        "employees": int(employees) if employees else None,
        "latest_annual": latest_inc.get("end_date") if latest_inc else None,
        "revenue_per_capita_wan": round(rev / employees / 1e4, 1) if (rev and employees) else None,
        "rd_to_revenue_pct": round(rd / rev * 100, 2) if (rev and rd is not None) else None,
    }

    # ---- probes: what公告/联网 to pull to do the real人/治理尽调 (Deep 方向三) ----
    probes = [
        {"why": "核对历史承诺兑现：激励考核目标 / 业绩承诺是否达成（最硬的 track record）",
         "cmd": f"fetch announcements {ts_code} --searchkey 股权激励",
         "and": "对照后续定期报告的实际达成情况"},
        {"why": "治理合规历史：监管函 / 问询 / 处罚 / 会计差错更正",
         "cmd": f"fetch announcements {ts_code} --searchkey 监管函",
         "and": f"fetch announcements {ts_code} --searchkey 问询"},
        {"why": "控股股东股权质押 / 资金占用风险",
         "cmd": f"fetch announcements {ts_code} --searchkey 质押"},
        {"why": "重要股东减持节奏与主体",
         "cmd": f"fetch announcements {ts_code} --searchkey 减持"},
        {"why": "创始人 / 实控人产业背景、连续创业战绩、行业声誉、言行一致性",
         "cmd": "联网检索创始人 / 实控人履历（本 skill 无此数据，归 Deep 方向三）"},
        {"why": "组织执行力：研发人员结构 / 核心技术人员变动 / 股权激励覆盖广度与考核进取性",
         "cmd": f"fetch report-text {ts_code} --report-type annual --section 研发",
         "and": f"fetch announcements {ts_code} --searchkey 股权激励（看覆盖人数与考核目标）"},
    ]

    notes: List[str] = []
    if not mrows:
        notes.append("缺 managers：无法看高管结构 / 稳定性。")
    elif len(in_office) < 5:
        notes.append(
            f"managers 疑为部分快照（在任仅 {len(in_office)} 行，通常董监高 9–15 人）："
            "高管稳定性为 best-effort，完整名册与跨年变动需读历年公告或联网补全。"
        )
    if not rw_by_name:
        notes.append("缺 rewards：无法看管理层持股 / 薪酬绑定。")
    if not ends:
        notes.append("缺 top10-holders：无法看集中度 / 制衡。")

    return {
        "management": management,
        "alignment": alignment,
        "ownership": ownership,
        "organization": organization,
        "shareholder_actions": shareholder_actions,
        "probes": probes,
        "notes": notes,
        "surfacing_only": (
            "以上仅为人/治理事实的确定性摆放，无评级、无好坏判断。"
            "创始人素质、团队 track record（承诺兑现）、治理诚信的判断与档位，"
            "全部由模型按 references/growth_success_rate.md 完成（骨架轻量 / Deep 方向三全量）。"
        ),
    }


def build_scan(evidence: dict) -> Dict[str, Any]:
    ds = lambda n: dataset(evidence, n)  # noqa: E731
    income = ds("income") if isinstance(ds("income"), list) else []
    financial = ds("financial") if isinstance(ds("financial"), list) else []
    balance = ds("balance") if isinstance(ds("balance"), list) else []
    cashflow = ds("cashflow") if isinstance(ds("cashflow"), list) else []
    band = ds("valuation-band") if isinstance(ds("valuation-band"), dict) else {}
    bands = band.get("bands") or {}

    fin_by_end = {str(r.get("end_date")): r for r in financial if isinstance(r, dict) and r.get("end_date")}
    bal_by_end = {str(r.get("end_date")): r for r in balance if isinstance(r, dict) and r.get("end_date")}
    cf_by_end = {str(r.get("end_date")): r for r in cashflow if isinstance(r, dict) and r.get("end_date")}

    ann_inc = annual_rows(income)
    ts_code = band.get("ts_code") or (income[0].get("ts_code") if income else None)

    # ---- growth trajectory (annual) ----
    growth: Dict[str, Any] = {"annual_periods": [r.get("end_date") for r in ann_inc]}
    if len(ann_inc) >= 2:
        n = len(ann_inc) - 1
        rev0, rev1 = to_num(ann_inc[0].get("revenue")), to_num(ann_inc[-1].get("revenue"))
        ni0, ni1 = to_num(ann_inc[0].get("n_income_attr_p")), to_num(ann_inc[-1].get("n_income_attr_p"))
        growth["revenue_cagr_pct"] = round(cagr(rev0, rev1, n), 2) if cagr(rev0, rev1, n) is not None else None
        growth["netprofit_cagr_pct"] = round(cagr(ni0, ni1, n), 2) if cagr(ni0, ni1, n) is not None else None
        growth["years_span"] = n
    rev_yoy = [to_num((fin_by_end.get(str(r.get("end_date"))) or {}).get("tr_yoy")) for r in ann_inc]
    rev_yoy = [v for v in rev_yoy if v is not None]
    growth["revenue_yoy_series"] = rev_yoy
    growth["all_positive_yoy"] = bool(rev_yoy) and all(v > 0 for v in rev_yoy)
    growth["yoy_volatility"] = round(max(rev_yoy) - min(rev_yoy), 2) if len(rev_yoy) >= 2 else None

    # ---- valuation snapshot ----
    pe = latest_window(bands, "pe_ttm")
    pb = latest_window(bands, "pb")
    ps = latest_window(bands, "ps_ttm")
    valuation = {
        "pe_ttm": pe.get("current"),
        "pe_pct": pe.get("current_percentile"),
        "pe_window": pe.get("window"),
        "pb": pb.get("current"),
        "pb_pct": pb.get("current_percentile"),
        "ps_ttm": ps.get("current"),
        "ps_pct": ps.get("current_percentile"),
    }

    flags: List[Dict[str, Any]] = []

    def flag(category, period, metric, value, threshold, direction, severity, probe):
        flags.append({
            "category": category, "period": period, "metric": metric,
            "value": value, "threshold": threshold, "direction": direction,
            "severity": severity, "probe": probe,
        })

    # ---- anomaly flags ----
    # 业绩 YoY surge / collapse (annual + latest quarter)
    for r in (ann_inc[-2:] + ([income[0]] if income else [])):
        ed = str(r.get("end_date"))
        f = fin_by_end.get(ed) or {}
        for key, label in (("tr_yoy", "营收YoY"), ("netprofit_yoy", "归母YoY")):
            v = to_num(f.get(key))
            if v is not None and abs(v) >= T["yoy_surge"]:
                flag("业绩异常", ed, label, round(v, 2), T["yoy_surge"],
                     "暴增" if v > 0 else "暴跌", "high",
                     {"why": "增速极端，需查驱动/可持续性/基数",
                      "cmd": f"fetch report-text {ts_code} --report-type annual --section mda",
                      "and": "联网检索行业景气与新闻"})
        # 扣非 vs 归母 divergence
        dedt, ni = to_num(f.get("profit_dedt")), to_num(r.get("n_income_attr_p"))
        if dedt is not None and ni and ni > 0 and (dedt / ni) < T["dedt_divergence"]:
            flag("利润质量", ed, "扣非/归母", round(dedt / ni, 2), T["dedt_divergence"],
                 "扣非显著低于归母", "med",
                 {"why": "非经常性损益占比高", "cmd": f"fetch income {ts_code} --limit 8",
                  "and": f"fetch report-text {ts_code} --report-type annual --section 财务报告"})

    # margin swings (latest two annuals)
    if len(ann_inc) >= 2:
        for key, label in (("grossprofit_margin", "毛利率"), ("netprofit_margin", "净利率")):
            a = to_num((fin_by_end.get(str(ann_inc[-2].get("end_date"))) or {}).get(key))
            b = to_num((fin_by_end.get(str(ann_inc[-1].get("end_date"))) or {}).get(key))
            if a is not None and b is not None and abs(b - a) >= T["margin_swing_pct"]:
                flag("利润质量", ann_inc[-1].get("end_date"), label, round(b - a, 2),
                     T["margin_swing_pct"], "上行" if b > a else "下行",
                     "med" if b < a else "low",
                     {"why": "利润率拐点", "cmd": f"fetch report-text {ts_code} --report-type annual --section mda"})

    # OCF / 净利 (latest annual)
    if ann_inc:
        ed = str(ann_inc[-1].get("end_date"))
        ocf = to_num((cf_by_end.get(ed) or {}).get("n_cashflow_act"))
        ni = to_num(ann_inc[-1].get("n_income_attr_p"))
        if ocf is not None and ni and ni > 0:
            ratio = ocf / ni
            if ratio < T["ocf_ni_weak"]:
                flag("利润质量", ed, "经营现金流/净利", round(ratio, 2), T["ocf_ni_weak"],
                     "利润未转现金", "high",
                     {"why": "利润含金量弱，查营运资本占用",
                      "cmd": f"fetch report-text {ts_code} --report-type annual --section 财务报告",
                      "and": "看应收/存货附注与信用政策"})

    # 应收 / 存货 vs 营收 growth (latest annual vs prior)
    if len(ann_inc) >= 2:
        ed, ped = str(ann_inc[-1].get("end_date")), str(ann_inc[-2].get("end_date"))
        rev_g = to_num((fin_by_end.get(ed) or {}).get("tr_yoy"))
        def grow(by_end, field):
            a = to_num((by_end.get(ped) or {}).get(field)); b = to_num((by_end.get(ed) or {}).get(field))
            return ((b - a) / a * 100.0) if (a and a > 0 and b is not None) else None
        recv_g = grow(bal_by_end, "accounts_receiv")
        inv_g = grow(bal_by_end, "inventories")
        if rev_g is not None and recv_g is not None and (recv_g - rev_g) >= T["recv_vs_rev_gap"]:
            flag("营运资本", ed, "应收增速-营收增速", round(recv_g - rev_g, 1), T["recv_vs_rev_gap"],
                 "应收扩张快于收入", "med",
                 {"why": "可能放宽信用确认收入", "cmd": f"fetch report-text {ts_code} --report-type annual --section 财务报告"})
        if rev_g is not None and inv_g is not None and (inv_g - rev_g) >= T["inv_vs_rev_gap"]:
            flag("营运资本", ed, "存货增速-营收增速", round(inv_g - rev_g, 1), T["inv_vs_rev_gap"],
                 "存货扩张快于收入", "med",
                 {"why": "去库存/跌价风险", "cmd": f"fetch report-text {ts_code} --report-type annual --section mda"})
        # inventory / revenue ratio
        inv = to_num((bal_by_end.get(ed) or {}).get("inventories"))
        rev = to_num(ann_inc[-1].get("revenue"))
        if inv is not None and rev and rev > 0 and (inv / rev * 100.0) >= T["inv_to_rev_high"]:
            flag("营运资本", ed, "存货/营收", round(inv / rev * 100.0, 1), T["inv_to_rev_high"],
                 "存货占营收高", "low",
                 {"why": "备货高，关注周转与跌价", "cmd": f"fetch balance {ts_code} --limit 8"})

    # 商誉 / 净资产, 资产负债率 (latest annual)
    if ann_inc:
        ed = str(ann_inc[-1].get("end_date"))
        gw = to_num((bal_by_end.get(ed) or {}).get("goodwill"))
        eqt = to_num((bal_by_end.get(ed) or {}).get("total_hldr_eqy_inc_min_int"))
        if gw is not None and eqt and eqt > 0 and (gw / eqt * 100.0) >= T["goodwill_to_eqt"]:
            flag("减值风险", ed, "商誉/净资产", round(gw / eqt * 100.0, 1), T["goodwill_to_eqt"],
                 "商誉占比高", "high",
                 {"why": "并购减值风险", "cmd": f"fetch report-text {ts_code} --report-type annual --section 财务报告",
                  "and": f"fetch announcements {ts_code} --searchkey 收购"})
        dta = to_num((fin_by_end.get(ed) or {}).get("debt_to_assets"))
        if dta is not None and dta >= T["debt_to_assets_high"]:
            flag("资本结构", ed, "资产负债率", round(dta, 1), T["debt_to_assets_high"],
                 "杠杆偏高", "med",
                 {"why": "偿债与财务费用压力", "cmd": f"fetch balance {ts_code} --limit 8"})

    # ---- thesis archetypes ----
    theses: List[Dict[str, Any]] = []
    rev_cagr = growth.get("revenue_cagr_pct")
    ni_cagr = growth.get("netprofit_cagr_pct")
    best_cagr = max([c for c in (rev_cagr, ni_cagr) if c is not None], default=None)
    pe_abs, pe_pct = valuation["pe_ttm"], valuation["pe_pct"]
    stable_grow = growth.get("all_positive_yoy")

    def add_thesis(archetype, subtype, rationale, probes, confidence_hint="待证实"):
        theses.append({"archetype": archetype, "subtype": subtype, "rationale": rationale,
                       "confidence_hint": confidence_hint, "probes": probes})

    if best_cagr is not None and best_cagr >= T["growth_cagr_strong"] and stable_grow:
        # 预期差: growth not (fully) priced — split A1/A2 by absolute PE + percentile
        de_rated = (pe_pct is not None and pe_pct <= T["pe_pct_low"])
        cheap_abs = (pe_abs is not None and pe_abs <= T["pe_abs_cheap"])
        if cheap_abs and de_rated:
            add_thesis("预期差", "A2 低估值+成长",
                       f"营收/利润 CAGR≈{best_cagr}% 且逐年正增长，PE_ttm={pe_abs}（{valuation['pe_window']}分位{pe_pct}%）绝对与分位双低",
                       [{"why": "确认增长未被定价、是否真便宜",
                         "cmd": "长周期日线确认月线横盘 + 主线归属", "and": f"fetch valuation-band {ts_code} --years 5"}],
                       "重点：最干净的预期差")
        elif de_rated and pe_abs is not None and pe_abs >= T["pe_abs_elevated"]:
            add_thesis("预期差", "A1 高估值消化",
                       f"CAGR≈{best_cagr}%，PE_ttm={pe_abs} 仍偏高但已 de-rate 到{valuation['pe_window']}分位{pe_pct}%（盈利追赶估值）",
                       [{"why": "判断消化是否到位、增速能否延续",
                         "cmd": f"fetch report-text {ts_code} --report-type annual --section mda"}],
                       "估值消化型")
        else:
            add_thesis("稳健/高增长", "增长已部分定价",
                       f"CAGR≈{best_cagr}%，PE_ttm={pe_abs}（分位{pe_pct}%）",
                       [{"why": "增速可持续性与透支判断", "cmd": f"fetch report-text {ts_code} --report-type annual --section mda"}])

    # B 期权型: rising R&D intensity / new-business — confirm via filings (always)
    rd_series = []
    for r in ann_inc:
        rev = to_num(r.get("revenue")); rd = to_num(r.get("rd_exp"))
        if rev and rev > 0 and rd is not None:
            rd_series.append(rd / rev * 100.0)
    rd_rising = len(rd_series) >= 2 and (rd_series[-1] - rd_series[0]) >= T["rd_intensity_rise"]
    add_thesis("预期差", "B 未定价期权",
               (f"研发/营收由 {round(rd_series[0],1)}% 升至 {round(rd_series[-1],1)}%，可能有未被定价的新业务/远期技术期权"
                if rd_rising else "需读年报/季报确认是否存在未被定价的新业务/远期技术期权（机器人/AI 等）"),
               [{"why": "捞公司自述的新布局/在研/募投，判断材料性与主线连接",
                 "cmd": f"fetch report-text {ts_code} --report-type q1 --section AI",
                 "and": f"fetch report-text {ts_code} --report-type annual --section mda + 联网检索当前主线"}],
               "必须靠方向二年报挖掘确认")

    people_governance = build_people_governance(evidence, ts_code)

    notes = []
    if not band:
        notes.append("缺 valuation-band：无法判断估值分位，预期差 A1/A2 分型不可靠。")
    if len(ann_inc) < 3:
        notes.append(f"年度样本仅 {len(ann_inc)} 期：CAGR/稳定性代表性弱，建议 income/financial 提高 --limit。")
    notes.append("月线横盘需长周期日线确认（pack 默认 daily 仅 60 日）。")
    notes.extend(people_governance.get("notes", []))

    return {
        "ts_code": ts_code,
        "as_of": band.get("latest_trade_date"),
        "growth": growth,
        "valuation": valuation,
        "thesis_candidates": theses,
        "anomaly_flags": flags,
        "people_governance": people_governance,
        "notes": notes,
        "model_responsibility": (
            "脚本只做阈值 surfacing：命题原型、异常旗标、人/治理事实都是线索，不是结论。"
            "命题证实/证伪、归因、贵贱与买卖判断、成长成功率档位与措辞，全部由模型按 "
            "references/deep_mode.md 与 references/growth_success_rate.md 完成。"
        ),
    }


def _stderr_summary(scan: dict) -> str:
    """One-line human-readable summary printed to stderr so a Deep run is visible
    in the terminal even when stdout is captured to JSON."""
    code = scan.get("ts_code", "?")
    theses = scan.get("thesis_candidates") or []
    subtypes = [t.get("subtype") or t.get("archetype") or "?" for t in theses]
    thesis_str = "+".join(subtypes) if subtypes else "none"

    flags = scan.get("anomaly_flags") or []
    sev_counts: Dict[str, int] = {}
    for f in flags:
        s = str(f.get("severity") or "?")
        sev_counts[s] = sev_counts.get(s, 0) + 1
    flag_str = " ".join(f"{k}:{v}" for k, v in sorted(sev_counts.items())) or "0"

    probe_count = sum(len(t.get("probes") or []) for t in theses) + sum(
        1 for f in flags if f.get("probe")
    )
    high_priority = sev_counts.get("high", 0) + sum(
        1 for t in theses if "预期差" in (t.get("archetype") or "")
    )
    pdf_budget = max(3, min(10, high_priority + 2))
    web_budget = max(3, min(10, len(theses) * 2 + 1))

    pg = scan.get("people_governance") or {}
    mgmt = pg.get("management") or {}
    own = pg.get("ownership") or {}
    sa = pg.get("shareholder_actions") or {}
    pg_str = (
        f"core_exits={len(mgmt.get('core_role_departures') or [])} "
        f"top1={(own.get('top1') or {}).get('ratio')} "
        f"减持记录={sa.get('decrease_count', 0)}"
    )

    return (
        f"[thesis_scan] {code} thesis={thesis_str} | flags={flag_str} | "
        f"probes={probe_count} | people/gov: {pg_str} | "
        f"budget hint: ≤{pdf_budget} PDF / ≤{web_budget} web"
    )


def build_plan(scan: dict) -> str:
    """Consolidate scan probes (thesis + anomaly flags + people_governance) into a
    numbered research work-order (markdown). Deterministic reformat / dedup — it
    assigns NO priority judgement of its own; the model refines order & landing
    spots per references/orchestration.md §2."""
    code = scan.get("ts_code", "?")
    # (rank, 归属, cmd, why, 落点) — lower rank = surfaced earlier (high-severity / 预期差 first)
    items: List[tuple] = []
    for t in scan.get("thesis_candidates") or []:
        tag = f"命题·{t.get('subtype') or t.get('archetype') or '?'}"
        rank = 1 if "预期差" in (t.get("archetype") or "") else 2
        for p in t.get("probes") or []:
            items.append((rank, tag, p.get("cmd"), p.get("why"), "核心看点 / 主线归属"))
    sev_rank = {"high": 0, "med": 2, "low": 3}
    for f in scan.get("anomaly_flags") or []:
        pr = f.get("probe") or {}
        tag = f"旗标·{f.get('category')}/{f.get('metric')}({f.get('severity')})"
        items.append((sev_rank.get(str(f.get("severity")), 2), tag, pr.get("cmd"),
                      pr.get("why"), "成长诊断 / 风险 / 估值置信度"))
    for p in (scan.get("people_governance") or {}).get("probes") or []:
        items.append((2, "成长成功率·人/治理", p.get("cmd"), p.get("why"), "成长成功率子节"))

    # dedup by cmd, keep the lowest rank (earliest) occurrence
    best: Dict[str, tuple] = {}
    for rank, tag, cmd, why, land in items:
        if not cmd:
            continue
        if cmd not in best or rank < best[cmd][0]:
            best[cmd] = (rank, tag, why, land)
    rows = sorted(best.items(), key=lambda kv: kv[1][0])

    highs = sum(1 for f in scan.get("anomaly_flags") or [] if f.get("severity") == "high")
    pdf_b = max(3, min(10, highs + 2))
    web_b = max(3, min(10, len(scan.get("thesis_candidates") or []) * 2 + 1))

    lines = [
        f"# 调研工单 · {code}",
        f"> 预算建议：读 ≤{pdf_b} 篇 PDF / 联网 ≤{web_b} 次。逐项核销（⬜→✅/⚠️数据缺/✗超预算）。"
        f"编排见 references/orchestration.md。",
        "",
        "| 编号 | 归属 | 动作 | 落点 | 状态 |",
        "|---|---|---|---|---|",
    ]
    for i, (cmd, (_rank, tag, why, land)) in enumerate(rows, 1):
        why_s = f"（{why}）" if why else ""
        lines.append(f"| W{i} | {tag} | `{cmd}`{why_s} | {land} | ⬜ |")
    lines += [
        "",
        "> 确定性骨架：主 agent 据此增删项、定优先级、补落点，再开始派子代理。脚本不下判断。",
    ]
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic thesis & anomaly scan over an evidence pack.")
    parser.add_argument("--evidence", "-e", required=True, help="Path to evidence_<code>.json from data_fetcher pack.")
    parser.add_argument("--out", "-o", default=None, help="Optional path to write the scan JSON.")
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Emit a consolidated research work-order (markdown) instead of the scan JSON.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress the human-readable stderr summary (kept for scripted callers).",
    )
    args = parser.parse_args(argv)

    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    scan = build_scan(evidence)
    if args.plan:
        print(build_plan(scan))
        return 0
    text = json.dumps(scan, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    if not args.quiet:
        print(_stderr_summary(scan), file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
