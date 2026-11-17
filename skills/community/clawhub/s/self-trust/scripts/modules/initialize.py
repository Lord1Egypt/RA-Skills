# -*- coding: utf-8 -*-
"""初始化模块（§7.1 懒人模板 / §7.2 三场景模拟演示）。

懒人模板：必填 3 项（corpus / monthly_contribution / objectives），
其余参数统一固化 balanced 默认值（§7.1 表）。

初始化护栏（§7.1）：
1. 重复初始化防护：contract.json 已存在 → 拒绝覆盖，提示走 记账自定义 / 记账重置；
2. 净口径警告：未补 liabilities / rigid_annual_expenses → 回执附毛口径警告；
3. deadline 校验：必须晚于 start_date（当日），否则驳回该目标；
4. 对账锚点：reconcile.last_reconcile = 初始化当日。
"""
from __future__ import annotations

import copy
import math
from datetime import date
from pathlib import Path
from typing import Any

from core import contract as contract_io
from core import crypto as crypto_io
from core.models import ObjectiveStatus
from core.contract import GuardError  # noqa: F401  (re-export for callers)


def lazy_init(
    data_dir: Path,
    *,
    corpus: float,
    monthly_contribution: float,
    objectives: list[dict[str, Any]],
    today: date | None = None,
    currency: str = "CNY",
    encrypt: bool = False,
    crypto_mode: str = "passphrase",
) -> dict[str, Any]:
    """懒人一键初始化。返回结构化结果 {ok, contract_path, warnings, rejected_objectives}。

    已存在契约 → 返回 {ok: False, error: "exists", ...}（护栏 1，不覆盖）。
    """
    today = today or date.today()
    if contract_io.contract_exists(data_dir):
        return {
            "ok": False,
            "error": "exists",
            "message": (
                "已存在契约，增量修改请用 `记账自定义`；"
                "如需彻底重建请用 `记账重置`（带二次确认，且保留 audit 目录历史）"
            ),
        }

    if not objectives or len(objectives) > 3:
        return {"ok": False, "error": "objectives_count",
                "message": "核心目标须为 1~3 个"}

    warnings: list[str] = []
    rejected: list[dict[str, Any]] = []
    accepted: list[dict[str, Any]] = []
    today_iso = today.isoformat()

    for obj in objectives:
        deadline = obj.get("deadline")
        # 护栏 3：deadline 必须晚于 start_date（当日）；None 允许（无期限目标）。
        # L6：按日期对象比较（非字符串），避免 "2036-1-10" < "2036-1-9" 这类字典序误判；
        # 格式非法（非 YYYY-MM-DD）视为无效 deadline 直接拒绝。
        if deadline is not None:
            try:
                dl = date.fromisoformat(str(deadline)[:10])
            except ValueError:
                rejected.append({"name": obj.get("name"), "reason":
                                f"deadline {deadline} 格式非法（须 YYYY-MM-DD）"})
                continue
            if dl <= today:
                rejected.append({"name": obj.get("name"), "reason":
                                f"deadline {deadline} 不晚于当日 {today_iso}，不生成负周期"})
                continue
        accepted.append(obj)

    if not accepted:
        return {"ok": False, "error": "no_valid_objectives",
                "message": "所有目标均未通过 deadline 校验",
                "rejected_objectives": rejected}

    c = contract_io.new_default_contract()
    c["corpus"] = float(corpus)
    c["monthly_contribution"] = float(monthly_contribution)
    c["currency"] = (currency or "CNY").upper()
    n = len(accepted)
    c["objectives"] = [
        {
            "name": o["name"],
            "weight": round(1.0 / n, 6),          # §7.1 多目标等权起步
            "current_amount": float(o.get("current_amount", 0) or 0),
            "start_date": today_iso,              # §7.1 start_date = 初始化当日
            "deadline": o.get("deadline"),
            "target_amount": o.get("target_amount"),
            "lag_streak": 0,
            "reward_unlocked": False,
            "reward_quota": 0.0,
            "status": ObjectiveStatus.ACTIVE.value,
        }
        for o in accepted
    ]
    # 护栏 4：对账锚点从首日起算
    c["reconcile"]["last_reconcile"] = today_iso

    # 护栏 2：净口径警告（层 A：置标记位 + 说清等式）
    # 净口径 = 录入 − 负债月供 − 刚性月摊；当前两者均为 0，故净=毛，无法确认是否高估。
    c["monthly_is_gross_estimate"] = True
    if not c["liabilities"] and not c["rigid_annual_expenses"]:
        warnings.append(
            "⚠️ 当前月度净流入按「毛口径」录入（未录入负债/刚性年支出），"
            "净口径 = 录入 − 负债月供 − 刚性月摊；当前两项均为 0，故净=毛，"
            "无法确认是否高估，生活费基线 / 安全垫据此偏高；"
            "说「记账自定义·补负债」或「补刚性」即净口径化"
        )

    # 静态加密配置（方案 C：开关 + 双路线）
    if encrypt:
        mode = crypto_mode if crypto_mode in ("passphrase", "keyfile") else "passphrase"
        key_file: str | None = None
        if mode == "keyfile":
            # 生成随机 key 文件（权限 600），路径相对 data-dir，便于整体备份迁移
            key_file = str(crypto_io.generate_key_file(
                Path(data_dir) / ".self-trust.key"))
            crypto_io.set_session(key_file=key_file)   # 让 write_contract 能密封
        # passphrase 模式：密钥由 CLI 经 --pass 设入 session，此处不接触明文密码
        c["crypto"] = {
            "enabled": True,
            "mode": mode,
            "kdf": "pbkdf2",
            "iterations": 200_000,
            "key_file": key_file,
        }
        if mode == "keyfile":
            warnings.append(
                "⚠️ 已启用静态加密（key-file 模式）：密钥文件 .self-trust.key 已生成"
                "（权限 600），迁移/备份 data-dir 时须一并带走，丢失则数据不可恢复"
            )
        else:
            warnings.append(
                "已启用静态加密（passphrase 模式）：每次操作需 --pass 或 "
                "SELFTRUST_PASS 环境变量，密码不落盘"
            )

    path = contract_io.write_contract(
        data_dir, c, actor="configurator", confirm=True, allow_create=True)
    return {
        "ok": True,
        "contract_path": str(path),
        "corpus": float(corpus),
        "monthly_contribution": float(monthly_contribution),
        "monthly_basis": "gross_estimate" if c["monthly_is_gross_estimate"] else "net",
        "currency": (currency or "CNY").upper(),
        "objectives": accepted,
        "warnings": warnings,
        "rejected_objectives": rejected,
        "message": "已生成默认契约（balanced），可随时说『自定义』逐项调",
        # §7.2：初始化成功后自动附三场景演示（用刚生成的真实契约参数干跑，
        # judge 为纯函数不落盘，不影响真实账目/审计）
        "demo": demo_scenarios(c, today=today),
    }


# ---------------------------------------------------------------- §7.2 演示
# 演示专用默认契约参数（无真实契约时的内存兼容层；绝不落盘）
DEMO_CORPUS = 50000.0
DEMO_MONTHLY = 8000.0
DEMO_OBJECTIVE = {"name": "演示目标（FIRE）", "target_amount": 300000.0}
# 设计文档 §7.2 表格的三个示例金额（仅作首选；若与当前契约参数下的目标场景
# 不匹配，则用引擎中间变量确定性推导替代金额，保证三类判定都真实可见）
DEMO_AMOUNT_SMALL = 35.0      # 奶茶（合理享受，计划内）
DEMO_AMOUNT_LARGE = 6000.0    # 新款手机（非计划）
DEMO_AMOUNT_BREACH = 30000.0  # 奢侈品包（非计划·破垫）


def _demo_contract(today: date) -> dict[str, Any]:
    """演示专用内存契约（balanced 默认值 + 演示参数），不写任何目录。"""
    c = contract_io.new_default_contract()
    c["corpus"] = DEMO_CORPUS
    c["monthly_contribution"] = DEMO_MONTHLY
    deadline = date(today.year + 10, today.month, 1)
    c["objectives"] = [{
        "name": DEMO_OBJECTIVE["name"],
        "weight": 1.0,
        "current_amount": 0.0,
        "start_date": today.isoformat(),
        "deadline": deadline.isoformat(),
        "target_amount": DEMO_OBJECTIVE["target_amount"],
        "lag_streak": 0,
        "reward_unlocked": False,
        "reward_quota": 0.0,
        "status": ObjectiveStatus.ACTIVE.value,
    }]
    return c


def _dry_judge(contract: dict[str, Any], *, amount: float, category: str,
               planned: bool, today: date) -> dict[str, Any]:
    """干跑 judge（纯函数，不落盘不入队不写审计）；延迟导入避免环。"""
    from modules.judge import judge
    return judge(contract, amount=amount, category=category,
                 planned=planned, today=today)


def demo_scenarios(contract: dict[str, Any] | None = None, *,
                   today: date | None = None) -> dict[str, Any]:
    """§7.2 三场景模拟演示：真实调用 judge 引擎干跑，不落地真实账目。

    - contract 传入 → 用初始化生成的真实契约参数推算（§7.2 原文口径）；
      内部 deepcopy，绝不回写调用方对象；
    - contract=None → 用演示专用默认契约（纯内存，绝不落盘）；
    - 全部数字来自 judge 引擎真实输出（F0~F7 真算），LLM 禁止心算铁律同样适用；
    - 示例金额首选 §7.2 表格值（35/6000/30000），若与当前契约下的目标场景
      不匹配则用引擎中间变量确定性推导替代金额（推导式随结果输出，可验算）。
    """
    today = today or date.today()
    is_demo_defaults = contract is None
    c = _demo_contract(today) if contract is None else copy.deepcopy(contract)

    # 探针干跑：取引擎真实中间变量（阈值/安全垫/corpus/月度净流入）
    probe = _dry_judge(c, amount=1.0, category="合理享受",
                       planned=False, today=today)
    if not probe.get("ok"):
        return {"ok": False, "error": "demo_probe_failed", "detail": probe}
    threshold = float(probe["cooldown"]["threshold"])
    judge_cushion = float(probe["optimization_applied"]["judge_cushion"])
    corpus = float(probe["inputs"]["corpus"])
    monthly_net = float(probe["inputs"]["monthly_net"])

    # 场景金额（确定性推导，保证三类判定真实命中）
    amt1 = DEMO_AMOUNT_SMALL if DEMO_AMOUNT_SMALL < threshold \
        else round(threshold * 0.2, 2)                       # 小额：阈值之下
    amt2 = DEMO_AMOUNT_LARGE if DEMO_AMOUNT_LARGE > threshold \
        else round(threshold * 1.5, 2)                       # 大额：阈值之上
    # 破垫：需 corpus - amount < 垫 且 缺口 > 月度净流入（§4.4 场景 C 硬条件）
    breach_min = corpus - judge_cushion + max(monthly_net, 0.0)
    amt3 = DEMO_AMOUNT_BREACH if DEMO_AMOUNT_BREACH > breach_min \
        else round(breach_min + max(monthly_net, 1.0), 2)

    r1 = _dry_judge(c, amount=amt1, category="合理享受",
                    planned=True, today=today)
    r2 = _dry_judge(c, amount=amt2, category="数码", planned=False, today=today)
    if r2.get("ok") and r2["decision"]["scene"] == "C":
        # 契约余量极紧时 6000 可能直接破垫；降到刚过阈值，保留「冷静期」演示语义
        amt2 = round(threshold * 1.05, 2)
        r2 = _dry_judge(c, amount=amt2, category="数码",
                        planned=False, today=today)
    r3 = _dry_judge(c, amount=amt3, category="奢侈品",
                    planned=False, today=today)

    # 场景 3 替代方案：分 N 月支取，每笔 ≤ 冷静期阈值（不触发冷静期的分期口径，
    # N 由引擎阈值推导，非硬编码）
    split_n = max(int(math.ceil(amt3 / threshold)), 2) if threshold > 0 else None
    alt_plan = None
    if split_n:
        alt_plan = {
            "months": split_n,
            "per_month": round(amt3 / split_n, 2),
            "note": "每笔不超冷静期阈值，不击穿安全垫不损目标（§5.3 替代路径）",
        }

    def _pack(idx: int, name: str, expect: str, amount: float, planned: bool,
              r: dict[str, Any]) -> dict[str, Any]:
        if not r.get("ok"):
            return {"id": idx, "name": name, "error": r}
        return {
            "id": idx, "name": name, "expect": expect, "ref": "§7.2",
            "amount": amount, "planned": planned,
            "scene": r["decision"]["scene"],
            "result": r["decision"]["result"],
            "summary": r["decision"]["summary"],
            "cooldown_triggered": r["cooldown"]["triggered"],
            "cooldown_days": r["cooldown"]["days"],
            "delay_months_simple": r["impact"]["delay_months_simple"],
            "remaining_after": r["inputs"]["remaining_after"],
        }

    notes = ["这是演示，不影响真实账户（干跑不落账目、不入冷静期队列、不写审计）；"
             "现在可以说『审查：买X花Y』开始真实审批"]
    if is_demo_defaults:
        notes.insert(0, "⚠️ 演示数据，非您的真实契约（尚未初始化，使用演示专用默认参数）")

    return {
        "ok": True,
        "stub": False,
        "demo_defaults_used": is_demo_defaults,
        "engine_params": {
            "corpus": corpus,
            "monthly_net": monthly_net,
            "cooldown_threshold": threshold,
            "judge_cushion": judge_cushion,
        },
        "scenarios": [
            _pack(1, "小额合理消费（奶茶）", "场景 A 直接批准",
                  amt1, True, r1),
            _pack(2, "大额非计划消费（新款手机）", "触发冷静期（§5.1）",
                  amt2, False, r2),
            _pack(3, "击穿安全垫大额消费（奢侈品包）", "驳回 + 分期替代方案",
                  amt3, False, r3),
        ],
        "alt_plan_scenario3": alt_plan,
        "notes": notes,
    }
