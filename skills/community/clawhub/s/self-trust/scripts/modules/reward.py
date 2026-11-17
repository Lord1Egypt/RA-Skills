# -*- coding: utf-8 -*-
"""里程碑奖励模块（§6.3：达成率 ≥120% 解锁超额 20%，免冷静期专项支取）。

- 解锁（F6）：达成率 ≥120% 且 reward_unlocked=false → reward_quota = 超额×20%；
- 支取：免冷静期（正反馈非冲动拦截），但仍走 §4.4 统一判定与安全垫校验
  （免等待不豁免判定）；支持分次部分支取，quota 递减到 0 即用尽；
- 单目标仅解锁一次基础奖励；150%/200% 梯度为扩展规划（留参数不实现，§8.2）；
- 全程 reward_log 留痕（仅追加，§10.1）。

LLM 铁律：禁止心算，数字必须原样引用引擎输出。
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from core import audit as audit_io
from core import contract as contract_io
from core import formulas as F
from core.models import RewardStatus

# §8.2 扩展规划占位：更高梯度阈值（当前仅实现 120% 基础解锁，不启用）
REWARD_TIERS_RESERVED = (1.5, 2.0)


def _reward_status_of(o: dict[str, Any], r6: dict[str, Any]) -> str:
    """由运行态子字段推导奖励状态枚举值（.value 即落盘字串）。

    - 已解锁且额度用尽 → exhausted；已解锁且有额度 → unlocked；
    - 未解锁但达标 → unlockable；未达标 → locked。
    """
    if bool(o.get("reward_unlocked")):
        if float(o.get("reward_quota", 0) or 0) <= 0:
            return RewardStatus.EXHAUSTED.value
        return RewardStatus.UNLOCKED.value
    return RewardStatus.UNLOCKABLE.value if r6["unlockable"] else RewardStatus.LOCKED.value


def reward_status(contract: dict[str, Any]) -> dict[str, Any]:
    """各目标奖励状态（F6 口径，只读）。"""
    out = []
    for o in contract.get("objectives", []):
        r6 = F.f6_reward(float(o.get("current_amount", 0) or 0),
                         o.get("target_amount"), bool(o.get("reward_unlocked")))
        out.append({
            "name": o.get("name"),
            "achieve_ratio": r6["achieve_ratio"],
            "unlockable": r6["unlockable"],
            "reward_unlocked": bool(o.get("reward_unlocked")),
            "reward_quota": float(o.get("reward_quota", 0) or 0),
            "potential_reward_max": r6["reward_max"],
            "reward_status": _reward_status_of(o, r6),
        })
    return {"ok": True, "rewards": out, "ref": "§6.3"}


def unlock_rewards(data_dir: Path, today: date | None = None) -> dict[str, Any]:
    """扫描并解锁达标目标（引擎写运行态子字段 reward_unlocked/reward_quota）。"""
    contract = contract_io.read_contract(data_dir)
    unlocked = []
    for o in contract.get("objectives", []):
        r6 = F.f6_reward(float(o.get("current_amount", 0) or 0),
                         o.get("target_amount"), bool(o.get("reward_unlocked")))
        if r6["unlockable"]:
            o["reward_unlocked"] = True
            o["reward_quota"] = r6["reward_max"]
            unlocked.append({"name": o.get("name"),
                             "achieve_ratio": r6["achieve_ratio"],
                             "reward_quota": r6["reward_max"]})
    if unlocked:
        contract_io.write_contract(data_dir, contract, actor="engine")
        for u in unlocked:
            audit_io.append(data_dir, "reward_log", {
                "time": audit_io.now_iso(today),
                "event": "unlocked", "obj": u["name"],
                "achieve_ratio": u["achieve_ratio"],
                "reward_quota": u["reward_quota"]})
    return {"ok": True, "unlocked": unlocked}


def claim_reward(
    data_dir: Path,
    *,
    objective: str,
    amount: float,
    purpose: str,
    today: date | None = None,
) -> dict[str, Any]:
    """奖励支取：quota 校验 + §4.4 统一判定（免冷静期不豁免安全垫）→ 递减落盘。"""
    from modules.judge import judge  # 延迟导入避免环

    today = today or date.today()
    if amount <= 0:
        return {"ok": False, "error": "invalid_amount",
                "message": "支取金额必须为正数"}
    contract = contract_io.read_contract(data_dir)
    obj = next((o for o in contract.get("objectives", [])
                if o.get("name") == objective), None)
    if obj is None:
        return {"ok": False, "error": "objective_not_found",
                "message": f"未找到目标 {objective}"}
    quota = float(obj.get("reward_quota", 0) or 0)
    if not obj.get("reward_unlocked") or quota <= 0:
        return {"ok": False, "error": "no_reward_quota",
                "message": f"目标 {objective} 无可用奖励额度"
                           "（未解锁或已用尽；单目标仅解锁一次基础奖励）"}
    if amount > quota:
        return {"ok": False, "error": "quota_exceeded",
                "message": f"支取 ¥{amount:,.0f} 超过剩余奖励额度 ¥{quota:,.0f}"}

    # 免冷静期，但仍走 §4.4 统一判定与安全垫校验（§6.3 护栏）
    verdict = judge(contract, amount=amount, category="里程碑奖励",
                    planned=True, today=today)
    if not verdict.get("ok"):
        return verdict
    if verdict["decision"]["scene"] == "C":
        return {"ok": False, "error": "cushion_violation",
                "message": "奖励支取不得击穿安全垫（§6.3 护栏）",
                "judge": verdict}

    obj["reward_quota"] = quota - amount
    contract_io.write_contract(data_dir, contract, actor="engine")
    audit_io.append(data_dir, "reward_log", {
        "time": audit_io.now_iso(today),   # M1：审计时间对齐逻辑 today
        "event": "claimed", "obj": objective,
        "amount": float(amount), "purpose": purpose,
        "quota_remaining": obj["reward_quota"],
        "scene": verdict["decision"]["scene"],
    })
    return {"ok": True, "objective": objective, "amount": float(amount),
            "purpose": purpose, "quota_remaining": obj["reward_quota"],
            "cooldown_exempt": True, "judge": verdict["decision"],
            "note": "免冷静期（正反馈）；已过 §4.4 统一判定与安全垫校验"}
