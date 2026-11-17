# -*- coding: utf-8 -*-
"""月度校准模块（§6.2 rebalance 缓冲/柔性/收入放松/回滚 + §6.4 目标生命周期）。

确定性规则（公正性靠代码不靠 AI；LLM 铁律：禁止心算，数字原样引用引擎输出）：
- 缓冲期：目标连续 2 个月 lag>0（F4 口径，lag_streak≥2）才触发调整（§6.2）；
- 柔性优先：净月增（F3.5/F7 口径）>0 时给 target_amount 下调 / deadline 顺延建议，
  写入 rebalance_override 临时层，不改原始 objectives（§10.3）；
- 刚性兜底：净月增≤0（柔性不可行）时 boost 投资占比（≤+15pct）+ 收紧非计划审批；
- 收入下跌自动放松：monthly_history 实绩连续 2 月 ≤ 基线×0.8 → 宽松态
  （invest_ratio_adj −10pct，暂停收紧），优先于 lag 收紧（不挤压生存消费）；
- 次月自动回滚：跨月即清空上月 rebalance_override，重新评估；
- §6.4 生命周期：active→overdue 由引擎确定性翻转（超期是客观事实）；
  completed / archived 须用户显式确认（transition_objective，过 §5.4 闸门）。

约束：校准只写运行态区（rebalance_override / lag_streak / last_calibrate /
objectives 内嵌运行态子字段），绝不改配置区 objectives.weight（test_contract_guard 强制）。
"""
from __future__ import annotations

import math
from datetime import date
from pathlib import Path
from typing import Any, Optional

from core import audit as audit_io
from core import contract as contract_io
from core import formulas as F
from core.models import living_baseline_value, ObjectiveStatus
from core.i18n import OBJECTIVE_STATUS_ZH, zh

# §6.2 确定性阈值（集中定义）
LAG_STREAK_TRIGGER = 2          # 连续落后月数触发线
INCOME_DROP_RATIO = 0.8         # 收入 ≤ 基线×0.8 视为下跌
INCOME_RECOVER_BAND = 0.1       # 恢复 = 基线 ±10% 内
BOOST_PCT_CAP = 15              # 刚性 boost 上限 +15pct
BOOST_PCT_DEFAULT = 10          # balanced 默认 boost
RELAX_INVEST_ADJ = -0.10        # 宽松态 invest_ratio 临时下调
APPROVAL_ADJ_FLOOR = -0.5       # 非计划审批通过率收紧下限


def _parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    return date.fromisoformat(str(s)[:10])


def _income_series(history: list[dict[str, Any]]) -> list[tuple[str, float]]:
    """月度收入实绩序列：按 month 去重（后写覆盖），仅保留 income 非 None 的月份。"""
    by_month: dict[str, float] = {}
    for rec in history or []:
        m = rec.get("month")
        if m and rec.get("income") is not None:
            by_month[str(m)] = float(rec["income"])
    return sorted(by_month.items())


def _net_monthly(contract: dict[str, Any]) -> float:
    """F3 → F3.5 链：真实口径净月增（校准柔性方案可行性判据）。"""
    dr = contract.get("distribution_rules", {})
    cp = dr.get("calc_params", {})
    f0 = F.f0_net_position(contract.get("corpus", 0), contract.get("liabilities"),
                           contract.get("rigid_annual_expenses"),
                           contract.get("monthly_contribution", 0))
    nominal = F.f3_monthly_invest_nominal(f0["monthly_net"], dr.get("invest_ratio", 0.5))
    return F.f3_5_monthly_invest_real(
        nominal, inflation=cp.get("inflation", 0.025),
        drawdown_factor=cp.get("drawdown_factor", 0.10),
        r_gross=cp.get("r_gross", 0.05))


def calibrate(
    contract: dict[str, Any],
    history: list[dict[str, Any]] | None = None,
    *,
    today: date | None = None,
    force: bool = False,
) -> dict[str, Any]:
    """月度校准入口（原地修改 contract 的运行态字段，不落盘；落盘走 run_calibrate）。

    返回 {ok, changes:[...], rebalance_override, skipped}。
    """
    today = today or date.today()
    this_month = today.strftime("%Y-%m")
    changes: list[dict[str, Any]] = []

    # 跨月守卫：同月已校准且非强制 → 跳过（幂等）
    last = contract.get("last_calibrate")
    if last and str(last)[:7] == this_month and not force:
        return {"ok": True, "skipped": True, "changes": [],
                "rebalance_override": contract.get("rebalance_override"),
                "message": "本月已校准（同月幂等，force=True 可重跑）"}

    # 1) 次月自动回滚：上月临时层过期清空（原始权重从未被改，§6.2 约束）
    ro = contract.get("rebalance_override")
    if ro and ro.get("month") != this_month:
        contract["rebalance_override"] = None
        changes.append({"type": "override_rollback", "expired": ro,
                        "note": "次月自动回滚，重新评估，原始权重不变"})

    net_monthly = _net_monthly(contract)
    inflation = (contract.get("distribution_rules", {})
                 .get("calc_params", {}).get("inflation", 0.025))

    # 2) §6.4 生命周期 + F6 奖励解锁（引擎仅翻转 active→overdue；completed 只建议）
    for o in contract.get("objectives", []):
        status = o.get("status") or ObjectiveStatus.ACTIVE.value
        if status != ObjectiveStatus.ACTIVE.value:
            continue
        target = o.get("target_amount")
        deadline = _parse_date(o.get("deadline"))
        current = float(o.get("current_amount", 0) or 0)
        achieved = (current / float(target)) if target else None
        if deadline and today > deadline and (achieved is None or achieved < 1.0):
            o["status"] = ObjectiveStatus.OVERDUE.value
            changes.append({
                "type": "lifecycle", "objective": o.get("name"),
                "from": ObjectiveStatus.ACTIVE.value, "to": ObjectiveStatus.OVERDUE.value,
                "note": "超期未达成，退出常规校准（F4 超期守卫）；"
                        "请三选一：延期 / 降额收尾 / 确认放弃（均过 §5.4 闸门）"})
            continue
        if achieved is not None and achieved >= 1.0:
            changes.append({
                "type": "lifecycle_suggestion", "objective": o.get("name"),
                "suggest": ObjectiveStatus.COMPLETED.value,
                "note": "已达成 100%，请用户确认收尾（标记已完成）；"
                        "确认后权重释放，提示重分配（引擎不自动改其它目标权重）"})
        # F6 里程碑奖励解锁（≥120% 且未解锁 → 写 reward_quota，运行态子字段）
        r6 = F.f6_reward(current, target, bool(o.get("reward_unlocked")))
        if r6["unlockable"]:
            o["reward_unlocked"] = True
            o["reward_quota"] = r6["reward_max"]
            changes.append({"type": "reward_unlocked", "objective": o.get("name"),
                            "achieve_ratio": r6["achieve_ratio"],
                            "reward_quota": r6["reward_max"]})

    # 3) lag_streak 缓冲计数（仅 active + 有 deadline；达标月归零）
    lagging: list[dict[str, Any]] = []
    for o in contract.get("objectives", []):
        if (o.get("status") or ObjectiveStatus.ACTIVE.value) != ObjectiveStatus.ACTIVE.value:
            continue
        info = F.f4_lag(o.get("current_amount", 0), o.get("target_amount"),
                        _parse_date(o.get("start_date")),
                        _parse_date(o.get("deadline")), today)
        if info is None:
            continue
        if info["lag"] > 0:
            o["lag_streak"] = int(o.get("lag_streak", 0)) + 1
        else:
            o["lag_streak"] = 0
        if o["lag_streak"] >= LAG_STREAK_TRIGGER:
            lagging.append({"objective": o, "lag": info["lag"]})

    # 4) 收入实绩监测（monthly_history[].income，非契约常量）
    series = _income_series(history or [])
    baseline_income = float(contract.get("monthly_contribution", 0) or 0)
    if baseline_income <= 0 and len(series) >= 3:
        # L7：近 3 月均值易被执行收入（一次性大额）拉高 → 改用中位数更稳健
        vals = sorted(v for _, v in series[-3:])
        n = len(vals)
        baseline_income = (vals[n // 2] if n % 2
                           else (vals[n // 2 - 1] + vals[n // 2]) / 2.0)
    income_drop = False
    income_recovered = False
    if baseline_income > 0 and len(series) >= 2:
        last2 = [v for _, v in series[-2:]]
        income_drop = all(v <= baseline_income * INCOME_DROP_RATIO for v in last2)
        income_recovered = all(
            abs(v - baseline_income) <= baseline_income * INCOME_RECOVER_BAND
            for v in last2)

    goal = contract.get("optimization_goal", "balanced")

    # 5) 临时层写入：收入放松优先于 lag 收紧（不挤压生存消费，§6.2）
    if income_drop:
        contract["rebalance_override"] = {
            "month": this_month,
            "reason": "income_drop",
            "boosts": [],
            "invest_ratio_adj": RELAX_INVEST_ADJ,
            "approval_rate_adj": 0.0,   # 暂停收紧
            "flex": None,
            "expire": "次月校准时",
        }
        changes.append({
            "type": "income_relax",
            "baseline_income": baseline_income,
            "recent_incomes": [v for _, v in series[-2:]],
            "invest_ratio_adj": RELAX_INVEST_ADJ,
            "note": "收入下行，已自动放松储蓄比例，优先保障生活；"
                    "本调整仅本月生效，次月自动重评，原始投资比例不变"})
    elif lagging:
        deepest = max(lagging, key=lambda x: x["lag"])
        obj = deepest["objective"]
        lag = float(deepest["lag"])
        if net_monthly > 0:
            # 柔性优先：按真实口径（F7）反推可达成数额 / 顺延月数
            real = F.f7_real_pace(0, obj.get("current_amount", 0),
                                  obj.get("target_amount"),
                                  _parse_date(obj.get("deadline")), today,
                                  net_monthly, inflation=inflation)
            remaining_months = (real["remaining_years"] * 12.0) if real else 0.0
            reachable = float(obj.get("current_amount", 0)) + net_monthly * remaining_months
            extend = 0
            if real and real.get("coverage_months") is not None:
                extend = max(math.ceil(real["coverage_months"] - remaining_months), 0)
            contract["rebalance_override"] = {
                "month": this_month,
                "reason": "lag_streak",
                "boosts": [],
                "invest_ratio_adj": 0.0,
                "approval_rate_adj": 0.0,
                "flex": {"obj": obj.get("name"),
                         "target_amount_adj": round(reachable, 2),
                         "deadline_adj_months": extend},
                "expire": "次月校准时",
            }
            changes.append({
                "type": "flex_calibrate", "objective": obj.get("name"),
                "lag": lag, "lag_streak": obj.get("lag_streak"),
                "flex": contract["rebalance_override"]["flex"],
                "note": "柔性方案（建议层，不改原始目标）：目标额按当前真实节奏"
                        "下调 / 期限顺延；原目标可在收入恢复后手动调回；仅本月生效"})
        else:
            # 刚性兜底：boost（≤+15pct）+ 非计划审批收紧（lag 深度映射）
            boost = BOOST_PCT_CAP if goal in ("wealth", "objective") else BOOST_PCT_DEFAULT
            adj = (APPROVAL_ADJ_FLOOR if goal in ("wealth", "objective")
                   else max(-round(lag, 4), APPROVAL_ADJ_FLOOR))
            contract["rebalance_override"] = {
                "month": this_month,
                "reason": "lag_streak",
                "boosts": [{"obj": obj.get("name"), "invest_boost_pct": boost}],
                "invest_ratio_adj": 0.0,
                "approval_rate_adj": adj,
                "flex": None,
                "expire": "次月校准时",
            }
            changes.append({
                "type": "rigid_calibrate", "objective": obj.get("name"),
                "lag": lag, "boost_pct": boost, "approval_rate_adj": adj,
                "note": "刚性方案（柔性不可行：无真实净月增）；仅本月生效，"
                        "次月自动回滚，原始权重不变"})
    elif income_recovered and not contract.get("rebalance_override"):
        changes.append({"type": "income_recovered",
                        "note": "收入恢复至基线 ±10% 内，维持常规校准态"})

    contract["last_calibrate"] = today.isoformat()
    return {"ok": True, "skipped": False, "changes": changes,
            "rebalance_override": contract.get("rebalance_override")}


def run_calibrate(data_dir: Path, *, today: date | None = None,
                  force: bool = False) -> dict[str, Any]:
    """校准编排：读契约 + audit monthly_history → calibrate → 引擎落盘（运行态区）。"""
    today = today or date.today()
    contract = contract_io.read_contract(data_dir)
    history = audit_io.read_all(data_dir, "monthly_history")
    result = calibrate(contract, history, today=today, force=force)
    if result["ok"] and not result.get("skipped"):
        contract_io.write_contract(data_dir, contract, actor="engine")
    return result


def transition_objective(
    data_dir: Path,
    name: str,
    dst: str,
    *,
    confirm: bool = False,
    today: date | None = None,
) -> dict[str, Any]:
    """§6.4 用户显式状态迁移（completed / archived / 延期回 active 由自定义走）。

    配置区写操作：objectives 属核心护栏字段，须 confirm=True（§5.4 闸门）。
    权重释放：completed/archived 后该目标 weight 释放，提示用户重分配
    （引擎不自动改其它目标权重，§10.3 配置区只读）。
    """
    if dst not in (ObjectiveStatus.COMPLETED.value, ObjectiveStatus.ARCHIVED.value):
        return {"ok": False, "error": "invalid_status",
                "message": "用户显式迁移仅支持 已达成 | 已归档"}
    contract = contract_io.read_contract(data_dir)
    obj = next((o for o in contract.get("objectives", [])
                if o.get("name") == name), None)
    if obj is None:
        return {"ok": False, "error": "objective_not_found",
                "message": f"未找到目标 {name}"}
    if dst == ObjectiveStatus.COMPLETED.value:
        target = obj.get("target_amount")
        if not target or float(obj.get("current_amount", 0)) < float(target):
            return {"ok": False, "error": "not_achieved",
                    "message": "未达成 100%，不可标记已达成"}
    if not confirm:
        return {"ok": False, "error": "need_confirm",
                "message": f"将把目标 {name} 迁移为 {zh(OBJECTIVE_STATUS_ZH, dst)}，"
                           f"权重 {obj.get('weight')} 将释放，需二次确认后生效",
                "released_weight": obj.get("weight")}
    prev = obj.get("status") or ObjectiveStatus.ACTIVE.value
    released = obj.get("weight")  # 记录释放前的权重（R2：归档后归零）
    obj["status"] = dst
    if dst == ObjectiveStatus.ARCHIVED.value:
        # R2：归档即释放权重（置 0），避免重新激活时旧权重仍参与分摊导致错配；
        #     重新激活须由用户经 customize 重新分配权重（与 §6.4 文档一致）。
        obj["weight"] = 0
    contract_io.write_contract(data_dir, contract, actor="configurator", confirm=True)
    # 归档留痕（§6.4：留 approval_log 归档记录）
    audit_io.append(data_dir, "approval_log", {
        "time": audit_io.now_iso(today),  # N3：审计时间对齐逻辑 today
        "event": f"objective_{dst}",
        "objective": name,
        "from": prev,
        "released_weight": released,
        "note": ("current_amount 为资金池内的标记额度，资金始终在 corpus 自由层"
                 "（archived 仅解除标记语义，corpus 不变，资金不消失）"
                 if dst == ObjectiveStatus.ARCHIVED.value else "达成收尾，奖励逻辑照常（§6.3）"),
    })
    return {"ok": True, "objective": name, "from": prev, "to": dst,
            "released_weight": released,
            "message": "权重已释放，请重分配到其余目标（记账自定义，过 §5.4 闸门）"}
