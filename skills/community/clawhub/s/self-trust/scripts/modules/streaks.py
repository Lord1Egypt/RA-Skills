# -*- coding: utf-8 -*-
"""§3.1 模式切换平滑过渡计数器（report_streak / gap_streak）。

设计文档 §3.1 原文口径：
- 监测字段（运行态区，FIELD_ZONES 已白名单）：last_report_date（最近一次完整上报日）、
  report_streak（连续上报天数，断则归零）、gap_streak（连续缺报天数，报则归零）；
- 阈值：hybrid 下连续 7 天上报 → 建议升 ledger；连续 14 天缺报 → 建议降 conversational；
- 仅 hybrid 模式触发提示；ledger / conversational 已定态不弹；
- 提示为软建议（`记账切模式` 由用户主动确认才生效），引擎绝不自动改 mode；
- 计数器随每次上报 / 报表生成更新；跨日判断用自然日。

挂载点（本模块只算不落盘，读写由调用方编排）：
- 上报事件 record_report()：governance.reconcile（对账/实绩补录）、report.run_report（报表生成）；
- 观察事件 observe()：judge.submit（审批不算上报，仅惰性刷新 gap / 断档归零）；
- 提示 transition_hint()：附在 report / judge / reconcile 的 JSON 输出（文案带真实计数）。
"""
from __future__ import annotations

from datetime import date
from typing import Any, Optional

# §3.1 阈值（设计文档原文：7 天连续上报 → ledger；14 天缺报 → conversational）
REPORT_STREAK_LEDGER_THRESHOLD = 7
GAP_STREAK_CONVERSATIONAL_THRESHOLD = 14


def _last_report(contract: dict[str, Any]) -> Optional[date]:
    s = contract.get("last_report_date")
    return date.fromisoformat(str(s)[:10]) if s else None


def record_report(contract: dict[str, Any], today: date) -> bool:
    """上报 / 报表生成事件：report_streak 按连续自然日 +1（断则重计 1），gap_streak 归零。

    同日重复上报幂等（不重复计数）。返回是否有字段变更（调用方据此决定落盘）。
    """
    last = _last_report(contract)
    streak = int(contract.get("report_streak", 0) or 0)
    if last is None:
        new_streak = 1
    else:
        delta = (today - last).days
        if delta == 0:
            new_streak = max(streak, 1)      # 同日幂等
        elif delta == 1:
            new_streak = streak + 1          # 连续自然日
        else:
            new_streak = 1                   # 断档（或日期回拨）→ 重计
    changed = (contract.get("last_report_date") != today.isoformat()
               or int(contract.get("report_streak", 0) or 0) != new_streak
               or int(contract.get("gap_streak", 0) or 0) != 0)
    contract["last_report_date"] = today.isoformat()
    contract["report_streak"] = new_streak
    contract["gap_streak"] = 0
    return changed


def observe(contract: dict[str, Any], today: date) -> bool:
    """观察事件（审批等非上报动作）：按自然日惰性刷新 gap_streak；断档归零 report_streak。

    gap_streak = 距最近上报日的自然日数（上报当日为 0）；无上报锚点时维持原值不虚构。
    断档判定：距最近上报 >1 天（昨日已缺报）→ report_streak 归零（§3.1「断则归零」）。
    """
    last = _last_report(contract)
    if last is None:
        return False
    gap = max((today - last).days, 0)
    changed = False
    if int(contract.get("gap_streak", 0) or 0) != gap:
        contract["gap_streak"] = gap
        changed = True
    if gap > 1 and int(contract.get("report_streak", 0) or 0) != 0:
        contract["report_streak"] = 0
        changed = True
    return changed


def transition_hint(contract: dict[str, Any], *,
                    observed_gap: int | None = None) -> Optional[dict[str, Any]]:
    """§3.1 平滑过渡软建议（仅 hybrid；文案带真实计数；引擎不自动改 mode）。

    observed_gap：调用方可传「记录前观察到的缺报天数」（report 场景先观察后记录，
    记录会把 gap 归零，若不回传观察值则缺报提示永远不可见）。
    """
    if contract.get("mode") != "hybrid":
        return None   # ledger / conversational 已定态不弹提示（§3.1）
    rs = int(contract.get("report_streak", 0) or 0)
    gs = int(observed_gap if observed_gap is not None
             else contract.get("gap_streak", 0) or 0)
    if rs >= REPORT_STREAK_LEDGER_THRESHOLD:
        return {
            "suggest_mode": "ledger",
            "report_streak": rs,
            "message": (f"你已连续 {rs} 天记账，是否切到全 ledger 持久台账，"
                        "让规则引擎看得更准？（`记账切模式 ledger`，仅建议，用户终裁）"),
            "ref": "§3.1",
        }
    if gs >= GAP_STREAK_CONVERSATIONAL_THRESHOLD:
        return {
            "suggest_mode": "conversational",
            "gap_streak": gs,
            "message": (f"最近 {gs} 天没怎么记账，可轻量化切回对话式，"
                        "避免繁琐放弃使用（`记账切模式 conversational`，仅建议，用户终裁）"),
            "ref": "§3.1",
        }
    return None
