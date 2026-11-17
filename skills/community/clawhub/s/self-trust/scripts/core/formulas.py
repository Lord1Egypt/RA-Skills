# -*- coding: utf-8 -*-
"""F0~F8 通用计算公式（设计文档 §2.0，纯函数，无副作用）。

设计原则（§11）：判定公正性靠确定性代码，不靠 AI。本模块只做数值计算：
- 除零保护：分母为 0 / None 时返回 None（含义为「不适用」），并由调用方标注
  「数据不全，测算存在偏差」，绝不输出虚假精确值。
- 无 deadline 目标：禁用 F4 / F7（返回 None）。
- 所有 doctest 使用设计文档示例数字，防文档与代码漂移。

公式编号与设计文档一一对应：F0 净资产/净流入、F1 有效安全垫、F2 冷静期阈值、
F3 月度可投增量（名义）、F3.5 通胀回撤修正、F4 目标落后度 lag、F5 消费影响（简化）、
F6 里程碑奖励、F7 真实节奏测算、F8 审批审计快照。
"""
from __future__ import annotations

from datetime import date
from typing import Any, Optional


# ---------------------------------------------------------------- F0
def f0_net_position(
    corpus: float,
    liabilities: list[dict[str, Any]] | None,
    rigid_annual_expenses: list[dict[str, Any]] | None,
    monthly_contribution: float,
) -> dict[str, float]:
    """公式 0：净资产与月度净流入。

    monthly_contribution 已是「税后收入 - 负债月供 - 刚性月摊」后的净口径
    （§2.0 说明），此处不重复扣减，仅单列负债/刚性中间变量供审计快照（F8）。

    >>> r = f0_net_position(200000, [{"name": "房贷", "balance": 800000,
    ...     "monthly_payment": 5000, "annual_rate": 0.04}],
    ...     [{"name": "保费", "amount": 12000, "due_month": 3}], 8000)
    >>> r["liabilities_sum"], r["rigid_monthly"], r["monthly_payment_sum"]
    (800000.0, 1000.0, 5000.0)
    >>> r["net_assets"], r["monthly_net"]
    (-600000.0, 8000.0)
    """
    liabilities = liabilities or []
    rigid = rigid_annual_expenses or []
    liabilities_sum = float(sum(x.get("balance", 0) or 0 for x in liabilities))
    monthly_payment_sum = float(sum(x.get("monthly_payment", 0) or 0 for x in liabilities))
    rigid_monthly = float(sum(x.get("amount", 0) or 0 for x in rigid)) / 12.0
    return {
        "corpus": float(corpus),
        "liabilities_sum": liabilities_sum,
        "monthly_payment_sum": monthly_payment_sum,
        "rigid_monthly": rigid_monthly,
        "net_assets": float(corpus) - liabilities_sum,
        "monthly_net": float(monthly_contribution),
    }


# ---------------------------------------------------------------- F1
def f1_effective_cushion(
    mode: str,
    living_baseline: float,
    months: float = 6,
    fixed: float = 0,
    ratio: float = 0.2,
    net_assets: float = 0,
) -> float:
    """公式 1：有效安全垫（三模式，ratio 基于净资产且负值收敛到 0）。

    >>> f1_effective_cushion("months", living_baseline=5000, months=6)
    30000.0
    >>> f1_effective_cushion("fixed", living_baseline=5000, fixed=100000)
    100000.0
    >>> f1_effective_cushion("ratio", living_baseline=5000, ratio=0.2, net_assets=500000)
    100000.0
    >>> f1_effective_cushion("ratio", living_baseline=5000, ratio=0.2, net_assets=-600000)
    0.0
    """
    mode = (mode or "").strip().lower()  # L5：模式名大小写不敏感（Months→months）
    if mode == "months":
        return float(living_baseline) * float(months)
    if mode == "fixed":
        return float(fixed)
    if mode == "ratio":
        return max(float(net_assets), 0.0) * float(ratio)
    # 未知模式：兜底为 0（无缓冲）而非抛错，避免 bogus 模式（如 customize 误设）
    # 让全部 judge/report 调用崩溃。非法模式由 customize 预览/落盘在边界处拒绝。
    return 0.0


# ---------------------------------------------------------------- F2
def f2_cooldown_threshold(
    effective_cushion: float,
    cooldown_days: float,
    living_baseline: float,
) -> float:
    """公式 2：冷静期自动阈值，clamp 到 [baseline×0.2, baseline×3]。

    >>> f2_cooldown_threshold(30000, 3, 5000)
    3000.0
    >>> f2_cooldown_threshold(1000000, 3, 5000)   # 垫极大 → clamp 上限
    15000.0
    >>> f2_cooldown_threshold(0, 3, 5000)         # 垫极小 → clamp 下限
    1000.0
    """
    raw = (float(effective_cushion) / 30.0) * float(cooldown_days)
    lo, hi = float(living_baseline) * 0.2, float(living_baseline) * 3.0
    return min(max(raw, lo), hi)


# ---------------------------------------------------------------- F3
def f3_monthly_invest_nominal(monthly_net: float, invest_ratio: float) -> float:
    """公式 3：月度可投增量（名义口径，乐观上限）。净流入 ≤ 0 时为 0。

    >>> f3_monthly_invest_nominal(8000, 0.5)
    4000.0
    >>> f3_monthly_invest_nominal(-2000, 0.5)
    0.0
    """
    if monthly_net is None or monthly_net <= 0:
        return 0.0
    return float(monthly_net) * float(invest_ratio)


# ---------------------------------------------------------------- F3.5
def f3_5_monthly_invest_real(
    monthly_invest_nominal: float,
    inflation: float = 0.025,
    drawdown_factor: float = 0.10,
    r_gross: float = 0.05,
) -> float:
    """公式 3.5：通胀回撤修正后的「实际月进展」（保守真实口径）。

    实际月进展 = 名义 × (1 - drawdown) × (1 + (r_gross - inflation) / 12)

    >>> round(f3_5_monthly_invest_real(4000), 2)
    3607.5
    >>> f3_5_monthly_invest_real(0)
    0.0
    """
    if monthly_invest_nominal is None or monthly_invest_nominal <= 0:
        return 0.0
    return (
        float(monthly_invest_nominal)
        * (1.0 - float(drawdown_factor))
        * (1.0 + (float(r_gross) - float(inflation)) / 12.0)
    )


# ---------------------------------------------------------------- F4
def f4_lag(
    current_amount: float,
    target_amount: Optional[float],
    start_date: Optional[date],
    deadline: Optional[date],
    today: date,
) -> Optional[dict[str, float | bool]]:
    """公式 4：目标落后度 lag（时间进度 - 达成进度，含超期 clamp）。

    deadline / start_date / target_amount 缺省 → 禁用（返回 None，仅展示攒钱占比）。

    >>> from datetime import date
    >>> r = f4_lag(42, 100, date(2026, 1, 1), date(2026, 1, 11), date(2026, 1, 6))
    >>> round(r["time_progress"], 2), round(r["lag"], 2), r["overdue"]
    (0.5, 0.08, False)
    >>> r = f4_lag(80, 100, date(2026, 1, 1), date(2026, 1, 11), date(2027, 1, 1))
    >>> r["time_progress"], round(r["lag"], 2), r["overdue"]   # 超期 clamp 到 1
    (1.0, 0.2, True)
    >>> f4_lag(42, None, None, None, date(2026, 1, 6)) is None
    True
    """
    if not deadline or not start_date or not target_amount:
        return None
    total_days = (deadline - start_date).days
    if total_days <= 0:
        return None  # 负/零周期契约（init 已校验，双保险）
    time_progress = min((today - start_date).days / total_days, 1.0)
    achieved = float(current_amount) / float(target_amount)
    return {
        "time_progress": time_progress,
        "achieved_progress": achieved,
        "lag": time_progress - achieved,
        "overdue": today > deadline,
    }


# ---------------------------------------------------------------- F5
def f5_impact_simple(amount: float, monthly_invest_nominal: float) -> Optional[float]:
    """公式 5：消费/撤回对目标影响（简化线性口径，误差 ±20%~50%，调用方须标注）。

    月度可投增量为 0 → 返回 None（「当前无自由现金流覆盖」，不除零）。

    >>> f5_impact_simple(10000, 5000)   # 文档示例：1 万 ÷ 5 千 = 延后约 2 个月
    2.0
    >>> f5_impact_simple(10000, 0) is None
    True
    """
    if not monthly_invest_nominal or monthly_invest_nominal <= 0:
        return None
    return float(amount) / float(monthly_invest_nominal)


# ---------------------------------------------------------------- F6
def f6_reward(
    current_amount: float,
    target_amount: Optional[float],
    reward_unlocked: bool,
) -> dict[str, Any]:
    """公式 6：里程碑奖励额度（达成率 ≥ 120% 且未解锁 → 超额 × 20%）。

    >>> r = f6_reward(360000, 300000, False)
    >>> r["unlockable"], r["reward_max"]
    (True, 12000.0)
    >>> f6_reward(330000, 300000, False)["unlockable"]   # 110% 不够
    False
    >>> f6_reward(360000, 300000, True)["unlockable"]    # 已解锁不重复
    False
    >>> f6_reward(360000, None, False)["unlockable"]     # 无目标额不适用
    False
    """
    if not target_amount or target_amount <= 0:
        return {"unlockable": False, "achieve_ratio": None, "reward_max": 0.0}
    ratio = float(current_amount) / float(target_amount)
    unlockable = ratio >= 1.2 and not reward_unlocked
    excess = max(float(current_amount) - float(target_amount), 0.0)
    return {
        "unlockable": unlockable,
        "achieve_ratio": ratio,
        "reward_max": excess * 0.2 if unlockable else 0.0,
    }


# ---------------------------------------------------------------- F7
def f7_real_pace(
    amount: float,
    current_amount: float,
    target_amount: Optional[float],
    deadline: Optional[date],
    today: date,
    monthly_invest_real: float,
    inflation: float = 0.025,
) -> Optional[dict[str, Optional[float]]]:
    """公式 7：真实节奏测算（复利 + 通胀动态折算目标额 + 回撤，落地默认口径）。

    deadline=None 禁用（同 F4 守卫）；净月增为 0 → 各月数返回 None（不除零）。

    >>> from datetime import date
    >>> r = f7_real_pace(10000, 100000, 300000, date(2036, 1, 1),
    ...                  date(2026, 1, 1), 3607.5, inflation=0.0)
    >>> round(r["gap_nominal"], 0), round(r["real_delay_months"], 2)
    (200000.0, 2.77)
    >>> r = f7_real_pace(10000, 100000, 300000, date(2036, 1, 1),
    ...                  date(2026, 1, 1), 0) # 无净月增
    >>> r["real_delay_months"] is None, round(r["gap_nominal"], 0) > 200000
    (True, True)
    """
    if not deadline or not target_amount:
        return None
    remaining_years = max((deadline - today).days / 365.0, 0.0)
    target_adj = float(target_amount) * (1.0 + float(inflation)) ** remaining_years
    gap_nominal = target_adj - float(current_amount)
    net_monthly = float(monthly_invest_real or 0)
    if net_monthly <= 0:
        return {
            "remaining_years": remaining_years,
            "target_amount_adj": target_adj,
            "gap_nominal": gap_nominal,
            "net_monthly": 0.0,
            "coverage_months": None,
            "real_delay_months": None,
        }
    return {
        "remaining_years": remaining_years,
        "target_amount_adj": target_adj,
        "gap_nominal": gap_nominal,
        "net_monthly": net_monthly,
        "coverage_months": gap_nominal / net_monthly if gap_nominal > 0 else 0.0,
        "real_delay_months": float(amount) / net_monthly,
    }


# ---------------------------------------------------------------- F8
def f8_audit_snapshot(
    *,
    time: str,
    amount: float,
    category: str,
    scene: str,
    inputs: dict[str, Any],
    formulas_used: list[str],
    decision: dict[str, Any],
    alt_plan: str = "",
) -> dict[str, Any]:
    """公式 8：审批审计快照（完整中间变量落盘结构，§10.1 复盘验算）。

    仅做结构组装校验（必备键缺失即报错，不吞错），落盘由 core.audit 负责。

    >>> snap = f8_audit_snapshot(time="2026-07-27T12:00:00", amount=10000,
    ...     category="合理享受", scene="C",
    ...     inputs={"corpus": 200000, "net_assets": -600000},
    ...     formulas_used=["F0", "F1", "F3", "F5"],
    ...     decision={"scene": "C", "result": "驳回", "summary": "击穿安全垫"},
    ...     alt_plan="分 3 个月从合理享受额度支取")
    >>> snap["decision"]["result"], snap["scene"]
    ('驳回', 'C')
    >>> f8_audit_snapshot(time="t", amount=1, category="c", scene="A",
    ...     inputs={}, formulas_used=[], decision={"scene": "A"})
    Traceback (most recent call last):
        ...
    ValueError: decision 缺少必备键: ['result', 'summary']
    """
    missing = [k for k in ("scene", "result", "summary") if k not in decision]
    if missing:
        raise ValueError(f"decision 缺少必备键: {missing}")
    return {
        "time": time,
        "amount": float(amount),
        "category": category,
        "scene": scene,
        "inputs": dict(inputs),
        "formulas_used": list(formulas_used),
        "decision": dict(decision),
        "alt_plan": alt_plan,
    }


if __name__ == "__main__":
    import doctest

    failed, _ = doctest.testmod()
    raise SystemExit(1 if failed else 0)
