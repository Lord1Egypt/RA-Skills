"""规则冲突检测（Pipeline Step 8a）。

若多条有效规则对同一步产出矛盾结论：禁止 AI 自选，必须标 conflict、列出冲突规则、
说明原因、返回 NEEDS_REVIEW。
"""
from __future__ import annotations

from evidence import EvidenceRecord


def detect_conflicts(records: list) -> dict:
    conflicts = []
    # 1) 步骤自带 conflict 标记
    for r in records:
        if r.conflict:
            conflicts.append({
                "step": r.step,
                "rule_ids": r.rules_used,
                "reason": "步骤内部标记规则冲突",
            })
    # 2) 格局与用忌一致性（天星密派口径）
    by = {r.step: r for r in records}
    if "pattern" in by and "yongji" in by:
        pat = by["pattern"].output["pattern"]
        yj_in = by["yongji"].input.get("pattern")
        if yj_in and yj_in != pat:
            conflicts.append({
                "step": "yongji",
                "rule_ids": by["yongji"].rules_used,
                "reason": f"取用忌引用格局“{yj_in}”与定格局输出“{pat}”不一致",
            })
    return {
        "has_conflict": len(conflicts) > 0,
        "conflicts": conflicts,
        "verdict": "NEEDS_REVIEW" if conflicts else "OK",
    }
