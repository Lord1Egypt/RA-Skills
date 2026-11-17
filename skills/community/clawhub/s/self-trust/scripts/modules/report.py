# -*- coding: utf-8 -*-
"""报表模块（§6.1 双可视化：双轨进度条 + 近6月 ASCII 趋势图 + 月度快照）。

- 进度条：达成进度（实填）vs 时间进度（虚线基线），绿/黄/红（F4 口径）；
- 趋势图：近 6 月 攒钱/生活/冲动 三层 + 安全垫红线提示（monthly_history 快照）；
- 月度快照：当月无快照时追加一条到 audit monthly_history（仅追加，§10.1）；
- conversational 模式标注「估算数据，精度有限」；安全垫逼近红色预警（§10.2）。

LLM 铁律：禁止心算，数字必须原样引用本模块输出。
"""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

from core import audit as audit_io
from core import contract as contract_io
from core import formulas as F
from core.models import living_baseline_value, monthly_basis, monthly_net_effective, ObjectiveStatus
from modules import streaks

BAR_WIDTH = 16
LAG_YELLOW = 0.0    # lag > 0 → 落后（黄）
LAG_RED = 0.10      # lag ≥ 10pct → 严重落后（红，§6.2 校准缓冲阈值口径）
CUSHION_WARN_MONTHS = 1.0   # 垫上余量 < 1 个月生活费 → 红色预警（§10.2）


def _parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    return date.fromisoformat(str(s)[:10])


def _bar(ratio: float, width: int = BAR_WIDTH) -> str:
    ratio = max(min(float(ratio), 1.0), 0.0)
    filled = round(ratio * width)
    return "█" * filled + "░" * (width - filled)


def _mini_bar(value: float, scale_max: float, width: int = 5) -> str:
    if scale_max <= 0:
        return "░" * width
    filled = round(min(value / scale_max, 1.0) * width)
    return "█" * filled + "░" * (width - filled)


def _objective_view(o: dict[str, Any], today: date) -> dict[str, Any]:
    name = o.get("name", "?")
    target = o.get("target_amount")
    current = float(o.get("current_amount", 0) or 0)
    status = o.get("status") or ObjectiveStatus.ACTIVE.value
    info = F.f4_lag(current, target, _parse_date(o.get("start_date")),
                    _parse_date(o.get("deadline")), today)
    view: dict[str, Any] = {
        "name": name, "status": status,
        "current_amount": current, "target_amount": target,
        "achieved_ratio": (current / float(target)) if target else None,
        "lag": None, "time_progress": None, "color": None,
    }
    # M6：achieved_ratio 已是 current/target（与 F6 的 achieve_ratio 同值，仅名字差一字母），
    # 不再重复挂 achieve_ratio 字段，避免 LLM 渲染引用错字段名。
    view["reward_quota"] = float(o.get("reward_quota", 0) or 0)
    if info is None:
        # 无 deadline 目标：仅展示攒钱占比（F4 守卫）
        ratio = view["achieved_ratio"] or 0.0
        view["ascii"] = f"{name}\t攒钱占比 {ratio:.0%}" if target else \
            f"{name}\t累计 ¥{current:,.0f}（无目标额，仅展示）"
        return view
    lag = info["lag"]
    color = ("红" if lag >= LAG_RED else "黄") if lag > LAG_YELLOW else "绿"
    view.update({"lag": lag, "time_progress": info["time_progress"],
                 "overdue": info["overdue"], "color": color})
    marks = []
    if info["overdue"]:
        marks.append("⚠️超期")
    if view["reward_quota"] > 0:
        marks.append(f"🏆已解锁奖励 ¥{view['reward_quota']:,.0f}")
    elif view["achieved_ratio"] and view["achieved_ratio"] >= 1.0:
        marks.append("🎉已达成")
    suffix = (" " + " ".join(marks)) if marks else ""
    view["ascii"] = (
        f"{name}\t{_bar(info['achieved_progress'])}  "
        f"{info['achieved_progress']:.0%}  "
        f"(时间轴应达 {info['time_progress']:.0%} · {color}){suffix}")
    return view


def _trend_ascii(history: list[dict[str, Any]]) -> str:
    """近 6 月资金流向三层 ASCII 趋势（攒钱/生活/冲动 + 安全垫红线）。"""
    recent = history[-6:]
    if not recent:
        return "（暂无月度快照，趋势图待累计）"
    invests = [float(r.get("invest", 0) or 0) for r in recent]
    livings = [float(r.get("living", 0) or 0) for r in recent]
    impulses = [float(r.get("impulse", 0) or 0) for r in recent]
    scale = max(invests + livings + impulses + [1.0])
    months = [str(r.get("month", "?"))[-2:].lstrip("0") + "月" for r in recent]
    rows = [
        "攒钱 " + " ".join(_mini_bar(v, scale) for v in invests) + "   ← 投资攒钱",
        "生活 " + " ".join(_mini_bar(v, scale) for v in livings) + "   ← 计划内生活",
        "冲动 " + " ".join(_mini_bar(v, scale) for v in impulses) + "   ← 非计划冲动",
        "月份  " + "  ".join(f"{m:<4}" for m in months),
        "── 安全垫红线 ──────────────────────",
    ]
    return "\n".join(rows)


def render_report(
    contract: dict[str, Any],
    history: list[dict[str, Any]] | None = None,
    *,
    today: date | None = None,
) -> dict[str, Any]:
    """报表入口（纯函数，不落盘）。输出结构化 JSON（进度/缺口/趋势/里程碑/预警）。"""
    today = today or date.today()
    history = history or []

    f0 = F.f0_net_position(contract.get("corpus", 0), contract.get("liabilities"),
                           contract.get("rigid_annual_expenses"),
                           contract.get("monthly_contribution", 0))
    baseline = living_baseline_value(contract)
    sc = contract.get("safety_cushion", {})
    cushion = F.f1_effective_cushion(
        sc.get("mode", "months"), baseline,
        months=sc.get("months", 6), fixed=sc.get("fixed", 0),
        ratio=sc.get("ratio", 0.2), net_assets=f0["net_assets"])
    margin = f0["corpus"] - cushion
    cushion_alert = margin < baseline * CUSHION_WARN_MONTHS

    objectives = [_objective_view(o, today) for o in contract.get("objectives", [])]
    progress_lines = [v["ascii"] for v in objectives]
    trend = _trend_ascii(history)

    # 层 B：毛/净口径展示（仅展示，不改判定；effective 不进 F0/F1/F2）
    basis = monthly_basis(contract)
    eff = monthly_net_effective(contract)

    notes: list[str] = []
    if contract.get("mode") == "conversational":
        notes.append("估算数据，精度有限（conversational 模式无持久台账）")
    # 毛口径待校准：report 常驻⚠️（把 init 一次性警告变成持久状态，分叉2）
    if basis == "gross_estimate":
        notes.append(
            "⚠️ 月净流入为「毛口径」估算（未录入负债/刚性），"
            "生活费基线 / 安全垫据此偏高；"
            "说「记账自定义·补负债」或「补刚性」即净口径化")
    if cushion_alert:
        notes.append(f"🔴 安全垫预警：垫上余量 ¥{margin:,.0f} 不足 1 个月生活费"
                     f"（¥{baseline:,.0f}），非计划消费已临时收紧（§10.2）")
    ro = contract.get("rebalance_override")
    if ro:
        notes.append(f"[临时校准] 生效中（{ro.get('month')}·{ro.get('reason')}），"
                     "仅本月有效，次月自动回滚，原始权重不变")

    return {
        "ok": True,
        "stub": False,
        "date": today.isoformat(),
        "mode": contract.get("mode"),
        "corpus": f0["corpus"],
        "net_assets": f0["net_assets"],
        "monthly_net": f0["monthly_net"],
        "monthly_basis": basis,
        "monthly_net_effective": eff,
        "living_baseline": baseline,
        "effective_cushion": cushion,
        "cushion_margin": margin,
        "cushion_alert": cushion_alert,
        "objectives": objectives,
        "rebalance_override": ro,
        "pending_cooling": [
            r for r in contract.get("pending_requests", [])
            if r.get("status") == "cooling"],
        "notes": notes,
        "ascii": "\n".join(progress_lines) + "\n\n" + trend,
        "formulas_used": ["F0", "F1", "F4", "F6"],
        "ref": "§6.1",
    }


def run_report(data_dir: Path, *, today: date | None = None) -> dict[str, Any]:
    """报表编排：读契约 + 历史 → 渲染 → 当月首报追加 monthly_history 快照（仅追加）。"""
    today = today or date.today()
    contract = contract_io.read_contract(data_dir)
    history = audit_io.read_all(data_dir, "monthly_history")
    result = render_report(contract, history, today=today)

    this_month = today.strftime("%Y-%m")
    already = any(str(r.get("month")) == this_month for r in history)
    if not already:
        snapshot = {
            "time": audit_io.now_iso(today),   # M1：审计时间对齐逻辑 today
            "month": this_month,
            "income": None,   # 实际注入实绩由对账/上报补录（§6.2 口径），不虚构
            "invest": None,
            "living": None,
            "impulse": None,
            "corpus": result["corpus"],
            "cushion_left": result["cushion_margin"],
        }
        audit_io.append(data_dir, "monthly_history", snapshot)
        result["snapshot_appended"] = snapshot
    else:
        result["snapshot_appended"] = None

    # 运行态：§3.1 平滑过渡计数器（先观察缺报天数再记上报，缺报提示不被归零吞掉）
    last = contract.get("last_report_date")
    observed_gap = ((today - date.fromisoformat(str(last)[:10])).days
                    if last else 0)
    streaks.record_report(contract, today)
    contract_io.write_contract(data_dir, contract, actor="engine")
    result["report_streak"] = contract["report_streak"]
    result["gap_streak_observed"] = observed_gap
    hint = streaks.transition_hint(contract, observed_gap=observed_gap)
    result["mode_transition_hint"] = hint
    if hint:
        result["notes"].append(hint["message"])
    return result
