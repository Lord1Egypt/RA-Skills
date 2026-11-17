# -*- coding: utf-8 -*-
"""审批判定模块（§4.4 统一判定 + §5.1 冷静期生命周期 + §5.1.2 白名单 + §7 调度）。

已实装（本模块为确定性引擎，LLM 铁律：禁止心算，数字必须原样引用引擎输出）：
- F0~F3.5 中间变量 → 场景 A/B/C 三段式路由（§4.4）；
- lag 恶化校验（F4 + F7 遍历 objectives，impacted 列表 + 整体恶化降级）；
- 白名单双上限（单笔 per_tx_cap 且 年度 annual_cap，跨年 used_annual 归零）；
- optimization_goal 三档对 B/C 边界的收紧调度（§7，阈值乘数修正）；
- corpus_status=imported_pending 前置拦截（§7.3，禁止一切审批）；
- pending_requests 入队 / withdraw / finalize / expire 生命周期（§5.1 状态机落盘）；
- 撤回正向激励要素（§5.1.1，基于 F5/F7 公式估算，绝不硬编码具体月数）；
- 双阶段提醒数据产出 list_due_reminders（§5.1，引擎只出数据，LLM 负责说人话）。
"""
from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from core import audit as audit_io
from core import contract as contract_io
from core import formulas as F
from core.models import (
    PendingRequest, RequestStatus, ObjectiveStatus, SpendStatus, can_transition,
    living_baseline_value, currency_symbol, monthly_basis, monthly_net_effective,
)
from modules import streaks
from core.i18n import REQUEST_STATUS_ZH, zh

# ---------------------------------------------------------------- 确定性阈值常量
# （§4.4 lag 恶化 / §7 调度；集中定义，全局唯一标准，不散落各分支）
IMPACT_DELAY_THRESHOLD_MONTHS = 1.0   # 非计划支出使单目标真实延后 ≥1 月 → impacted
SEVERE_DELAY_MONTHS = 6.0             # 已实质落后目标再延 ≥6 月 → 严重拖慢（场景 C）
LAG_MATERIAL = 0.05                   # lag ≥ 5pct 视为「实质落后」（防日常小 lag 噪声）

# §7 optimization_goal 三档：对 §4.4 场景 B/C 边界的安全垫判定阈值乘数
# wealth 收紧全部支出边界；objective 仅对「非计划（非目标类）」支出额外收紧；
# balanced 维持公式原值。乘数只作用于判定边界，不改动 F1 的 effective_cushion 本值。
OPT_CUSHION_MULT = {"wealth": 1.2, "balanced": 1.0, "objective": 1.0}
OPT_CUSHION_MULT_UNPLANNED = {"wealth": 1.2, "balanced": 1.0, "objective": 1.3}

# 融资购房默认参数（§4.4 融资购房可行性）
DEFAULT_MORTGAGE_TERM_YEARS = 30
DEFAULT_MORTGAGE_RATE = 0.04


def estimate_mortgage_monthly(principal: float, term_years: float,
                              annual_rate: float) -> float:
    """等额本息月供（确定性公式，禁止心算，调用方须原样引用返回）。"""
    n = int(round(float(term_years) * 12))
    p = float(principal)
    if n <= 0:
        return 0.0  # L1：无期限（0 年）视作一次性付清，无月供（不再返回全额本金）
    r = float(annual_rate) / 12.0
    if r == 0:
        return p / n
    f = (1.0 + r) ** n
    return p * r * f / (f - 1.0)


def check_whitelist(contract: dict[str, Any], category: str,
                    amount: float) -> dict[str, Any]:
    """白名单双上限判定（§5.1.2）：单笔≤per_tx_cap 且 累计+本笔≤annual_cap。"""
    for item in contract.get("fast_track_whitelist", []):
        if item.get("name") != category:
            continue
        per_ok = amount <= float(item.get("per_tx_cap", 0))
        annual_ok = (float(item.get("used_annual", 0)) + amount
                     <= float(item.get("annual_cap", 0)))
        return {
            "listed": True,
            "fast_track": per_ok and annual_ok,
            "per_tx_ok": per_ok,
            "annual_ok": annual_ok,
            "remaining_annual": float(item.get("annual_cap", 0))
            - float(item.get("used_annual", 0)),
        }
    return {"listed": False, "fast_track": False}


def _objective_impacts(
    contract: dict[str, Any],
    amount: float,
    planned: bool,
    invest_nominal: float,
    invest_real: float,
    inflation: float,
    today: date,
    boost_map: dict[str, float] | None = None,
) -> tuple[list[dict[str, Any]], bool, bool]:
    """lag 恶化校验（§4.4 场景 A 条件 2）：遍历 active 目标，按权重分摊本笔支出，
    用 F7 测算真实延后月数。返回 (impacted 列表, 整体恶化, 严重拖慢)。

    确定性规则（常量见文件头）：
    - impacted   ：非计划 且 该目标真实延后 ≥ IMPACT_DELAY_THRESHOLD_MONTHS；
    - 整体恶化   ：任一 impacted 目标当前 lag ≥ LAG_MATERIAL（实质落后被进一步拖累）→ A 降 B；
    - 严重拖慢   ：任一实质落后目标真实延后 ≥ SEVERE_DELAY_MONTHS → 场景 C（§4.4）。
    """
    impacted: list[dict[str, Any]] = []
    worsened = False
    severe = False
    # H3 修复：weight 是相对权重，分摊须除 active 目标总权重，否则多目标时
    # 各目标 share 直接相加会超过实际支出（影响被放大、lag 恶化判定过于激进）。
    active_objs = [o for o in contract.get("objectives", [])
                   if (o.get("status") or ObjectiveStatus.ACTIVE.value) == ObjectiveStatus.ACTIVE.value]
    total_weight = sum(float(o.get("weight", 1.0)) for o in active_objs) or 1.0
    for o in contract.get("objectives", []):
        if (o.get("status") or ObjectiveStatus.ACTIVE.value) != ObjectiveStatus.ACTIVE.value:
            continue
        deadline = _parse_date(o.get("deadline"))
        start = _parse_date(o.get("start_date"))
        target = o.get("target_amount")
        lag_info = F.f4_lag(o.get("current_amount", 0), target, start,
                            deadline, today) if deadline and start else None
        share = float(amount) * float(o.get("weight", 1.0)) / total_weight
        boost_pct = (boost_map or {}).get(o.get("name"), 0.0)
        obj_invest_real = invest_real * (1.0 + _boost_pct_to_frac(boost_pct))  # R1/N5
        real = F.f7_real_pace(share, o.get("current_amount", 0), target,
                              deadline, today, obj_invest_real,
                              inflation=inflation) if deadline and target else None
        delay_real = real.get("real_delay_months") if real else None
        delay_simple = F.f5_impact_simple(share, invest_nominal)
        lag = lag_info["lag"] if lag_info else None
        is_impacted = (not planned and delay_real is not None
                       and delay_real >= IMPACT_DELAY_THRESHOLD_MONTHS)
        material = lag is not None and lag >= LAG_MATERIAL
        if is_impacted:
            impacted.append({
                "name": o.get("name"),
                "weight": o.get("weight"),
                "amount_share": share,
                "delay_months_real": delay_real,
                "delay_months_simple": delay_simple,
                "lag": lag,
                "material_lag": material,
            })
            if material:
                worsened = True
                if delay_real >= SEVERE_DELAY_MONTHS:
                    severe = True
    return impacted, worsened, severe


def _parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    return date.fromisoformat(str(s)[:10])


def _boost_pct_to_frac(pct: float) -> float:
    """N5：invest_boost_pct 为整数百分比（如 15 表示 15%），转为小数比例。

    守卫：
    - 必须在 [0, 100]；
    - 0 < pct < 1 视为「误传比率」（如把 15% 写成 0.15），显式报错避免静默误用。
    """
    pct = float(pct)
    if not (0.0 <= pct <= 100.0):
        raise ValueError(f"invest_boost_pct 须为整数百分比 [0,100]，收到 {pct!r}")
    if 0.0 < pct < 1.0:
        raise ValueError(f"invest_boost_pct 疑似误传比率（{pct!r}）；"
                         f"整数百分比应为 15 而非 0.15")
    return pct / 100.0


def judge(
    contract: dict[str, Any],
    *,
    amount: float,
    category: str,
    planned: bool,
    today: date | None = None,
    financed_amount: float = 0.0,
    financed_term_years: float | None = None,
    financed_rate: float | None = None,
    financed_monthly: float | None = None,
    currency: str = "CNY",
    exchange_rate: float | None = None,
) -> dict[str, Any]:
    """§4.4 统一判定入口（纯函数，不落盘）。返回结构化 JSON。

    多币种支持（Level B）：
    - currency=CNY（默认）：直接用 amount 判定，行为不变（向后兼容）。
    - currency≠CNY：须提供 exchange_rate；amount_cny = amount * rate，
      全部判定逻辑在 amount_cny 上运行。inputs 额外记录原始金额/币种/汇率。

    融资购房（financed_amount>0）：大额资产购买拆为「首付(打 liquid) + 房贷(变负债+月供)」。
    决策口径：
    - 非融资：remaining = 净资产(corpus-负债) - amount（§4.4 line360 净资产口径）；
    - 融资：liquid_remaining = corpus - 首付（净资产不因按揭变，故用流动口径）；
      另加「月供可覆盖性」硬约束（月供 ≤ 月度净流入）。
    目标 lag 一律用 actual_cash_out（非融资=全额，融资=首付）测算。

    LLM 铁律：禁止心算，数字必须原样引用本函数输出。
    """
    today = today or date.today()

    # ---- 多币种换算（Level B）----
    currency = (currency or "CNY").upper()
    base_currency = (contract.get("currency") or "CNY").upper()
    original_amount = float(amount)
    original_currency = currency
    rate_used: float | None = None
    if currency != base_currency:
        if exchange_rate is None or exchange_rate <= 0:
            return {"ok": False, "error": "missing_rate",
                    "message": f"币种 {currency} ≠ 基准币种 {base_currency}，"
                               f"须提供有效 --rate（>0）"}
        rate_used = float(exchange_rate)
        amount = original_amount * rate_used    # 判定用换算后金额

    if amount <= 0:
        return {"ok": False, "error": "invalid_amount",
                "message": "申请金额必须为正数"}

    # ---- §7.3 imported_pending 前置拦截：未经人工核对的导入资产禁止一切审批 ----
    if contract.get("corpus_status") == "imported_pending":
        return {"ok": False, "error": "import_pending",
                "message": "资产为第三方导入待核对状态，"
                           "禁止审批；请先完成人工核对确认（§7.3）"}

    # ---- 中间变量（F0 ~ F3.5）----
    f0 = F.f0_net_position(
        contract.get("corpus", 0),
        contract.get("liabilities"),
        contract.get("rigid_annual_expenses"),
        contract.get("monthly_contribution", 0),
    )
    baseline = living_baseline_value(contract)
    sc = contract.get("safety_cushion", {})
    cushion = F.f1_effective_cushion(
        sc.get("mode", "months"), baseline,
        months=sc.get("months", 6), fixed=sc.get("fixed", 0),
        ratio=sc.get("ratio", 0.2), net_assets=f0["net_assets"])
    threshold_cfg = contract.get("cooldown_threshold", "auto")
    if threshold_cfg == "auto":
        threshold = F.f2_cooldown_threshold(
            cushion, contract.get("cooldown_days", 3), baseline)
    else:
        threshold = float(threshold_cfg)
    dr = contract.get("distribution_rules", {})
    ro = contract.get("rebalance_override") or {}  # R1：读取临时重平衡层
    eff_invest_ratio = max(0.0, min(1.0,
        float(dr.get("invest_ratio", 0.5)) + float(ro.get("invest_ratio_adj") or 0.0)))
    invest_nominal = F.f3_monthly_invest_nominal(f0["monthly_net"], eff_invest_ratio)
    cp = dr.get("calc_params", {})
    inflation = cp.get("inflation", 0.025)
    invest_real = F.f3_5_monthly_invest_real(
        invest_nominal,
        inflation=inflation,
        drawdown_factor=cp.get("drawdown_factor", 0.10),
        r_gross=cp.get("r_gross", 0.05))
    delay_simple = F.f5_impact_simple(amount, invest_nominal)

    # ---- 融资购房（§4.4 融资购房可行性）----
    financed = float(financed_amount or 0) > 0
    if financed:
        down_payment = max(float(amount) - float(financed_amount), 0.0)
        term = financed_term_years if financed_term_years is not None \
            else DEFAULT_MORTGAGE_TERM_YEARS
        rate = financed_rate if financed_rate is not None \
            else DEFAULT_MORTGAGE_RATE
        if financed_monthly is not None:
            mortgage_monthly = float(financed_monthly)
        else:
            mortgage_monthly = estimate_mortgage_monthly(
                float(financed_amount), term, rate)
        actual_cash_out = down_payment
        # 净资产不因按揭变化（房产+负债抵消），流动口径用 corpus-首付
        remaining = f0["corpus"] - down_payment
        debt_service_ok = (
            mortgage_monthly <= f0["monthly_net"]
            if f0["monthly_net"] > 0 else mortgage_monthly <= 0)
    else:
        down_payment = float(amount)
        mortgage_monthly = 0.0
        actual_cash_out = float(amount)
        # §4.4 line360 净资产口径：remaining = 净资产 - 支出（负债高时自动收敛）
        remaining = f0["net_assets"] - float(amount)
        debt_service_ok = True

    # ---- 白名单 / 冷静期（触发额用 actual_cash_out）----
    wl = check_whitelist(contract, category, actual_cash_out)
    cooldown_triggered = actual_cash_out > threshold and not wl["fast_track"]

    # ---- §7 optimization_goal 调度：判定边界乘数（不改 F1 本值）----
    goal = contract.get("optimization_goal", "balanced")
    mult_table = OPT_CUSHION_MULT_UNPLANNED if not planned else OPT_CUSHION_MULT
    mult = mult_table.get(goal, 1.0)
    judge_cushion = cushion * mult
    # R1：审批收紧（approval_rate_adj，负数=收紧）→ 提高审批门槛（乘以 1-|adj|）
    approval_adj = float(ro.get("approval_rate_adj") or 0.0)
    judge_cushion_eff = judge_cushion * (1.0 - approval_adj)

    # ---- lag 恶化校验（F4 + F7 遍历 objectives，用实际现金流出测算）----
    # R1/N5：目标投资加成映射；同名 obj 重复条目求和合并，避免 dict comprehension 静默覆盖
    boost_map: dict[str, float] = {}
    boost_warnings: list[str] = []
    for b in (ro.get("boosts") or []):
        obj = b.get("obj")
        pct = float(b.get("invest_boost_pct", 0))
        if obj in boost_map:
            boost_map[obj] += pct
            boost_warnings.append(f"同名目标投资加成重复，已合并: {obj}（当前合计 +{boost_map[obj]:g}）")
        else:
            boost_map[obj] = pct
    impacted, worsened, severe = _objective_impacts(
        contract, actual_cash_out, planned, invest_nominal, invest_real,
        inflation, today, boost_map=boost_map)

    # ---- §4.4 三场景路由（资金/垫口径 + 目标进度不恶化条件）----
    if severe:
        scene, result = "C", "驳回"
        summary = ("严重拖慢目标达成：实质落后目标将被进一步延后超过 "
                   f"{SEVERE_DELAY_MONTHS:g} 个月（§4.4 场景 C）")
    elif financed and not debt_service_ok:
        scene, result = "C", "驳回"
        summary = (f"月供 {mortgage_monthly:g} 超过月度净流入 {f0['monthly_net']:g}，"
                   "债务无法覆盖（月供压垮现金流，§4.4 融资购房可行性）")
    elif remaining >= judge_cushion_eff and not worsened:
        scene, result = "A", "批准"
        summary = "扣除后仍在安全垫之上且不恶化目标进度，合理享受额度正常使用"
    elif remaining >= judge_cushion and worsened:
        scene, result = "B", "附条件"
        summary = ("资金面在安全垫之上，但将进一步拖累已实质落后的目标"
                   "（建议分期/延迟/缩减，§4.4 场景 A 条件 2 降级）")
    elif f0["monthly_net"] > 0 and (judge_cushion_eff - remaining) <= f0["monthly_net"]:
        scene, result = "B", "附条件"
        summary = "扣除后跌破安全垫，但月度净流入可覆盖缺口（建议分期/延迟/缩减）"
    else:
        scene, result = "C", "驳回"
        summary = "击穿安全垫且无月度净流入兜底"

    return {
        "ok": True,
        "stub": False,
        "decision": {"scene": scene, "result": result, "summary": summary},
        "cooldown": {
            "triggered": cooldown_triggered,
            "threshold": threshold,
            "days": contract.get("cooldown_days", 3),
        },
        "whitelist": wl,
        "impacted_objectives": impacted,
        "optimization_applied": {
            "goal": goal,
            "cushion_multiplier": mult,
            "judge_cushion": judge_cushion,
            "rebalance_override": ro or None,             # R1
            "effective_invest_ratio": eff_invest_ratio,   # R1
            "approval_adj": approval_adj,                 # R1
            "judge_cushion_eff": judge_cushion_eff,       # R1
            "boost_warnings": boost_warnings,             # R1/N5：同名目标加成合并告警
        },
        "inputs": {
            **f0,
            "living_baseline": baseline,
            "monthly_basis": monthly_basis(contract),
            "monthly_net_effective": monthly_net_effective(contract),
            "effective_cushion": cushion,
            "invest_ratio": dr.get("invest_ratio", 0.5),
            "monthly_invest_nominal": invest_nominal,
            "monthly_invest_real": invest_real,
            "inflation": inflation,
            "amount": float(amount),
            "category": category,
            "planned": planned,
            "remaining_after": remaining,
            "financed": financed,
            "down_payment": down_payment,
            "financed_amount": float(financed_amount or 0),
            "mortgage_monthly": mortgage_monthly,
            "debt_service_ok": debt_service_ok,
            "actual_cash_out": actual_cash_out,
            "base_currency": base_currency,
            "original_amount": original_amount if currency != base_currency else None,
            "original_currency": original_currency if currency != base_currency else None,
            "exchange_rate": rate_used,
        },
        "impact": {
            "delay_months_simple": delay_simple,
            "note": "简化口径误差 ±20%~50%，长期目标以真实口径（F7）为准",
        },
        "formulas_used": ["F0", "F1", "F2", "F3", "F3.5", "F4", "F5", "F7"],
    }


# ================================================================ 落盘编排层
def _find_request(contract: dict[str, Any], request_id: str) -> dict[str, Any] | None:
    for r in contract.get("pending_requests", []):
        if r.get("request_id") == request_id:
            return r
    return None


def _record_pending_spend(contract: dict[str, Any], request_id: str,
                          result: dict[str, Any], amount: float, category: str,
                          planned: bool, financed_amount: float, status: str,
                          today: date | None = None) -> None:
    """M4：把审批通过的支出记入运行时台账 pending_spends（引擎可写，不碰配置区 corpus）。
    仅记录实际现金流出，供 reconcile 对账时并入并清空，消除「审批不自动扣 corpus」的静默坑。"""
    inp = result.get("inputs", {})
    contract.setdefault("pending_spends", []).append({
        "request_id": request_id,
        "time": audit_io.now_iso(today),   # M1：审计时间对齐逻辑 today
        "amount": float(amount),           # 原始金额（用户输入）
        "amount_base": float(inp.get("amount", amount)),  # 换算后金额（基准币种）
        "actual_cash_out": float(inp.get("actual_cash_out", amount)),
        "category": category,
        "planned": planned,
        "scene": result["decision"]["scene"],
        "financed_amount": float(financed_amount or 0),
        "currency": inp.get("original_currency"),       # None=CNY 原生
        "exchange_rate": inp.get("exchange_rate"),       # None=CNY 原生
        "base_currency": inp.get("base_currency", "CNY"),
        "status": status,
    })


def _update_pending_spend_status(contract: dict[str, Any], request_id: str,
                                 status: str) -> None:
    """M4：冷却窗终裁/撤回时同步台账条目状态。"""
    for s in contract.get("pending_spends", []):
        if s.get("request_id") == request_id:
            s["status"] = status
            return


def _reset_whitelist_year_if_needed(contract: dict[str, Any], today: date) -> bool:
    """§5.1.2 跨年重置：自然年变化 → 全部 used_annual 归零 + 更新 whitelist_cap_year。"""
    if contract.get("whitelist_cap_year") == today.year:
        return False
    for item in contract.get("fast_track_whitelist", []):
        item["used_annual"] = 0
    contract["whitelist_cap_year"] = today.year
    return True


def submit(
    data_dir: Path,
    *,
    amount: float,
    category: str,
    planned: bool,
    today: date | None = None,
    financed_amount: float = 0.0,
    financed_term_years: float | None = None,
    financed_rate: float | None = None,
    financed_monthly: float | None = None,
    currency: str = "CNY",
    exchange_rate: float | None = None,
) -> dict[str, Any]:
    """审批提交编排：judge → 冷静期入队 / 白名单额度记账 → F8 快照落审计。

    引擎只写运行态区（pending_requests / used_annual / whitelist_cap_year），
    契约配置区不动（§10.3）。融资购房参数透传 judge；落盘仅记录，不改 corpus/负债
    （首付支取 / 房贷负债由用户经 reconcile / customize --record-home-purchase 显式落账）。
    """
    today = today or date.today()
    contract = contract_io.read_contract(data_dir)
    result = judge(
        contract, amount=amount, category=category, planned=planned, today=today,
        financed_amount=financed_amount, financed_term_years=financed_term_years,
        financed_rate=financed_rate, financed_monthly=financed_monthly,
        currency=currency, exchange_rate=exchange_rate)
    if not result.get("ok"):
        return result

    scene = result["decision"]["scene"]
    cooldown_triggered = result["cooldown"]["triggered"]
    fast_track = bool(result["whitelist"].get("fast_track"))
    # M4：场景 A/B（批准/附条件）或进入冷静期队列（待终裁）→ 视为「将发生的支出」，
    # 记入运行时台账；场景 C 硬驳回（非冷静期、非白名单）→ 无支出，不记。
    will_spend = scene in ("A", "B") or cooldown_triggered

    changed = _reset_whitelist_year_if_needed(contract, today)
    # §3.1 观察事件：审批不算上报，仅惰性刷新 gap_streak / 断档归零 report_streak
    changed = streaks.observe(contract, today) or changed
    request_id: Optional[str] = None

    if will_spend:
        # M4：登记支出台账（运行时态，不碰配置区 corpus；§10.3 最小权限）。
        # 冷静期入队者状态 cooling，其余（即时批准/白名单放行）状态 approved。
        request_id = uuid.uuid4().hex[:12]
        _record_pending_spend(
            contract, request_id, result, amount, category, planned,
            financed_amount,
            status=SpendStatus.COOLING.value if cooldown_triggered else SpendStatus.APPROVED.value,
            today=today)
        changed = True

    if cooldown_triggered:
        # §5.1 大额非白名单 → 入冷静期队列（跨会话持久不丢单）
        days = int(contract.get("cooldown_days", 3))
        now = datetime.combine(today, datetime.min.time())
        req = PendingRequest(
            request_id=request_id,  # 与台账条目共用 id，便于终裁/撤回联动
            time=now.isoformat(timespec="seconds"),
            amount=float(amount),
            category=category,
            planned=planned,
            expire_at=(now + timedelta(days=days)).isoformat(timespec="seconds"),
        )
        entry = req.__dict__ | {
            "decision": result["decision"],
            "financed_amount": float(financed_amount or 0),
            "down_payment": result["inputs"].get("down_payment", float(amount)),
            "mortgage_monthly": result["inputs"].get("mortgage_monthly", 0.0),
            "original_amount": result["inputs"].get("original_amount"),
            "original_currency": result["inputs"].get("original_currency"),
            "exchange_rate": result["inputs"].get("exchange_rate"),
            "base_currency": result["inputs"].get("base_currency", "CNY"),
            "amount_base": float(result["inputs"].get("amount", amount)),
        }
        contract.setdefault("pending_requests", []).append(entry)
        result["request_id"] = request_id
        result["expire_at"] = req.expire_at
        changed = True
    elif fast_track and scene in ("A", "B"):
        # §5.1.2 极速放行 → 年度额度记账
        # 修复 H3：与白名单限额闸门口径一致，记「实际现金流出」而非全款。
        #   非融资：actual_cash_out == amount（无变化）；融资购房：actual_cash_out == 首付，
        #   避免用全款累加把年度 cap 倍数吃光。
        actual_out = float(result["inputs"].get("actual_cash_out", amount))
        for item in contract.get("fast_track_whitelist", []):
            if item.get("name") == category:
                item["used_annual"] = float(item.get("used_annual", 0)) + actual_out
        changed = True

    if changed:
        contract_io.write_contract(data_dir, contract, actor="engine")

    # F8 完整中间变量快照（§10.1，复盘验算）
    audit_io.append_approval_snapshot(data_dir, {
        "time": audit_io.now_iso(today),   # M1：审计时间对齐逻辑 today
        "amount": float(amount),
        "category": category,
        "scene": result["decision"]["scene"],
        "inputs": result["inputs"],
        "formulas_used": result["formulas_used"],
        "decision": result["decision"],
        "alt_plan": "",
        "fast_track": bool(result["whitelist"].get("fast_track")),
        "request_id": request_id,
        "planned": planned,
        "original_amount": result["inputs"].get("original_amount"),
        "original_currency": result["inputs"].get("original_currency"),
        "exchange_rate": result["inputs"].get("exchange_rate"),
        "base_currency": result["inputs"].get("base_currency", "CNY"),
    })
    # §3.1 平滑过渡软建议（仅 hybrid；文案带真实计数；引擎不自动改 mode）
    result["mode_transition_hint"] = streaks.transition_hint(contract)
    return result


def withdraw(data_dir: Path, request_id: str,
             today: date | None = None) -> dict[str, Any]:
    """§5.1.1 撤回正向激励：cooling → withdrawn + 基于 F5/F7 的提前月数估算。

    注意：提前月数是**公式估算**（简化/真实双口径区间），非承诺；无自由现金流
    覆盖时给相对表述标记，绝不硬编码具体月数。
    """
    today = today or date.today()
    contract = contract_io.read_contract(data_dir)
    entry = _find_request(contract, request_id)
    if entry is None:
        return {"ok": False, "error": "request_not_found",
                "message": f"未找到申请 {request_id}"}
    src = RequestStatus(entry["status"])
    if not can_transition(src, RequestStatus.WITHDRAWN):
        return {"ok": False, "error": "invalid_transition",
                "message": f"申请状态 {zh(REQUEST_STATUS_ZH, src.value)} 不可撤回（仅冷静期可）"}
    # H2 修复：过期后状态机仍 cooling（终裁懒惰），须阻止撤回，改走 expire 终裁
    expire_d = datetime.fromisoformat(entry["expire_at"]).date()
    if today > expire_d:
        return {"ok": False, "error": "already_expired",
                "message": f"申请 {request_id} 已过期，请走到期终裁"}
    entry["status"] = RequestStatus.WITHDRAWN.value
    _update_pending_spend_status(contract, request_id, SpendStatus.WITHDRAWN.value)  # M4 台账联动
    contract_io.write_contract(data_dir, contract, actor="engine")

    # 正向激励要素（引擎只算，LLM 负责说人话）
    amount = float(entry["amount"])
    dr = contract.get("distribution_rules", {})
    cp = dr.get("calc_params", {})
    f0 = F.f0_net_position(contract.get("corpus", 0), contract.get("liabilities"),
                           contract.get("rigid_annual_expenses"),
                           contract.get("monthly_contribution", 0))
    invest_nominal = F.f3_monthly_invest_nominal(
        f0["monthly_net"], dr.get("invest_ratio", 0.5))
    invest_real = F.f3_5_monthly_invest_real(
        invest_nominal, inflation=cp.get("inflation", 0.025),
        drawdown_factor=cp.get("drawdown_factor", 0.10),
        r_gross=cp.get("r_gross", 0.05))
    ahead_simple = F.f5_impact_simple(amount, invest_nominal)
    # 选最相关目标 = active 中权重最高且有 deadline 的目标（§5.3 同源规则）
    top = None
    for o in contract.get("objectives", []):
        if (o.get("status") or ObjectiveStatus.ACTIVE.value) != ObjectiveStatus.ACTIVE.value or not o.get("deadline"):
            continue
        if top is None or float(o.get("weight", 0)) > float(top.get("weight", 0)):
            top = o
    ahead_real = None
    if top is not None:
        real = F.f7_real_pace(amount, top.get("current_amount", 0),
                              top.get("target_amount"),
                              _parse_date(top.get("deadline")), today,
                              invest_real, inflation=cp.get("inflation", 0.025))
        ahead_real = real.get("real_delay_months") if real else None

    feedback = {
        "withdrawn_amount": amount,
        "monthly_invest_nominal": invest_nominal,
        "monthly_invest_real": invest_real,
        "objective": top.get("name") if top else None,
        "ahead_months_simple": ahead_simple,    # 简化口径（保守，无复利）
        "ahead_months_real": ahead_real,        # 真实口径（复利+通胀+回撤）
        "estimation_note": ("提前月数为公式估算区间（简化/真实双口径），非承诺"
                            if ahead_simple is not None else
                            "当前无自由现金流覆盖，仅给相对表述：撤回即多攒下等额资金"),
    }
    # 审计：追加反向记录（不抹原记录，§10.1）
    audit_io.append(data_dir, "approval_log", {
        "time": audit_io.now_iso(today),   # M1
        "event": "withdrawn",
        "request_id": request_id,
        "amount": amount,
        "category": entry.get("category"),
        "feedback": feedback,
    })
    return {"ok": True, "request_id": request_id,
            "status": RequestStatus.WITHDRAWN.value, "feedback": feedback}


def finalize(data_dir: Path, request_id: str,
             today: date | None = None) -> dict[str, Any]:
    """§5.1 用户到期前确认执行 → cooling → decided，按入队时原判定终裁。

    对齐 withdraw/expire（H2 同源）：过期后状态机仍 cooling（终裁懒惰），
    须阻止终裁、改走 expire 惰性终裁；场景 C（原判定驳回）终裁维持 EXPIRED
    而非 DECIDED，避免批准一个引擎本应自动驳回的申请。
    """
    today = today or date.today()
    contract = contract_io.read_contract(data_dir)
    entry = _find_request(contract, request_id)
    if entry is None:
        return {"ok": False, "error": "request_not_found",
                "message": f"未找到申请 {request_id}"}
    # 过期护栏：与 withdraw 对齐，过期须走 expire 惰性终裁
    expire_d = datetime.fromisoformat(entry["expire_at"]).date()
    if today > expire_d:
        return {"ok": False, "error": "already_expired",
                "message": f"申请 {request_id} 已过期，请走到期终裁"}
    src = RequestStatus(entry["status"])
    # 场景 C 终裁维持 EXPIRED（原判定驳回失效）；其余 DECIDED
    scene = (entry.get("decision") or {}).get("scene")
    dst = RequestStatus.EXPIRED if scene == "C" else RequestStatus.DECIDED
    if not can_transition(src, dst):
        return {"ok": False, "error": "invalid_transition",
                "message": f"申请状态 {zh(REQUEST_STATUS_ZH, src.value)} "
                           f"不可终裁为 {zh(REQUEST_STATUS_ZH, dst.value)}"}
    entry["status"] = dst.value
    _update_pending_spend_status(
        contract, request_id,
        SpendStatus.APPROVED.value if dst == RequestStatus.DECIDED
        else SpendStatus.EXPIRED.value)  # M4 台账联动
    contract_io.write_contract(data_dir, contract, actor="engine")
    decision = entry.get("decision", {})
    audit_io.append(data_dir, "approval_log", {
        "time": audit_io.now_iso(today),   # M1
        "event": "finalized",
        "request_id": request_id,
        "amount": entry.get("amount"),
        "category": entry.get("category"),
        "decision": decision,
    })
    return {"ok": True, "request_id": request_id,
            "status": dst.value, "decision": decision}


def expire(data_dir: Path, request_id: str | None = None,
           today: date | None = None) -> dict[str, Any]:
    """§5.1 到期惰性终裁：过期未撤回的 cooling 申请按原判定收尾。

    原判定 A/B → decided（批准/附条件生效）；原判定 C → expired（维持驳回失效）。
    request_id=None 时处理全部到期项。
    """
    today = today or date.today()
    contract = contract_io.read_contract(data_dir)
    processed: list[dict[str, Any]] = []
    audit_records: list[dict[str, Any]] = []
    now = datetime.combine(today, datetime.max.time())
    for entry in contract.get("pending_requests", []):
        if request_id and entry.get("request_id") != request_id:
            continue
        if entry.get("status") != RequestStatus.COOLING.value:
            continue
        if datetime.fromisoformat(entry["expire_at"]) > now:
            if request_id:
                return {"ok": False, "error": "not_due",
                        "message": f"申请 {request_id} 尚未到期"
                                   f"（expire_at={entry['expire_at']}）"}
            continue
        scene = (entry.get("decision") or {}).get("scene")
        dst = RequestStatus.EXPIRED if scene == "C" else RequestStatus.DECIDED
        if not can_transition(RequestStatus(entry["status"]), dst):
            return {"ok": False, "error": "invalid_transition",
                    "message": f"{zh(REQUEST_STATUS_ZH, entry['status'])} → {zh(REQUEST_STATUS_ZH, dst.value)} 非法"}
        entry["status"] = dst.value
        _update_pending_spend_status(
            contract, entry["request_id"],
            SpendStatus.APPROVED.value if dst == RequestStatus.DECIDED
            else SpendStatus.EXPIRED.value)  # M4 台账联动
        processed.append({"request_id": entry["request_id"],
                          "final_status": dst.value,
                          "amount": entry.get("amount"),
                          "category": entry.get("category", ""),
                          "decision": entry.get("decision")})
        audit_records.append({
            "time": audit_io.now_iso(today),   # M1
            "event": "expired_ruling",
            "request_id": entry["request_id"],
            "amount": entry.get("amount"),
            "final_status": dst.value,
            "decision": entry.get("decision"),
        })
    # M2：先落盘契约（状态迁移一次性原子），再批量写审计；契约已一致，
    # 即便某条审计追加失败也不会让 request 状态回退重处理。
    if processed:
        contract_io.write_contract(data_dir, contract, actor="engine")
        for rec in audit_records:
            audit_io.append(data_dir, "approval_log", rec)
    if request_id and not processed:
        return {"ok": False, "error": "request_not_found",
                "message": f"未找到可到期终裁的申请 {request_id}"}
    return {"ok": True, "processed": processed}


def list_due_reminders(contract: dict[str, Any],
                       today: date | None = None) -> list[dict[str, Any]]:
    """§5.1 双阶段提醒数据（不主动发，只产出；LLM 负责说人话）。

    kind: "expiring"（到期 ≤1 天，二次确认窗）| "cooling"（冷静中，锚定提醒）。
    """
    today = today or date.today()
    out: list[dict[str, Any]] = []
    for entry in contract.get("pending_requests", []):
        if entry.get("status") != RequestStatus.COOLING.value:
            continue
        expire_d = datetime.fromisoformat(entry["expire_at"]).date()
        days_left = (expire_d - today).days
        out.append({
            "request_id": entry.get("request_id"),
            "amount": entry.get("amount"),
            "category": entry.get("category"),
            "expire_at": entry.get("expire_at"),
            "days_left": days_left,
            "kind": "expiring" if days_left <= 1 else "cooling",
        })
    return out
