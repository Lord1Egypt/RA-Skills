"""scripts/stop.py - 模式感知自适应停止（§5.10 / §8）。"""

from typing import Any, Dict, List


def _new_url_count(history: List[Any], new_results: List[Any]) -> int:
    seen = set()
    for h in history:
        for s in (h if isinstance(h, list) else []):
            if isinstance(s, dict) and s.get("url"):
                seen.add(s["url"])
    fresh = 0
    for s in new_results:
        if isinstance(s, dict) and s.get("url") and s["url"] not in seen:
            fresh += 1
    return fresh


def should_stop(
    tier: str,
    history: List[Any],
    new_results: List[Any],
    llm_says_enough: bool = False,
    budget_hit: bool = False,
    coverage_closed: bool = False,
) -> Dict[str, Any]:
    """L0/L1 预算即停(exhausted=False)；L2/L3 覆盖饱和度即停；必写 stop_reason。

    返回 {stop, reason, exhausted}。
    """
    fresh = _new_url_count(history, new_results)
    # L0/L1 缩范围模式
    if tier in ("L0", "L1"):
        if budget_hit:
            return {"stop": True, "reason": "预算到达即停(缩范围模式)", "exhausted": False}
        if fresh == 0 and history:
            return {"stop": True, "reason": "连续两轮无新信息", "exhausted": False}
        if llm_says_enough:
            return {"stop": True, "reason": "证据足够，决定不检索", "exhausted": False}
        return {"stop": False, "reason": "", "exhausted": False}
    # L2/L3 保覆盖模式
    if coverage_closed or llm_says_enough:
        return {"stop": True, "reason": "覆盖饱和度达成(子问题全答/缺口闭合)", "exhausted": False}
    if fresh == 0 and history:
        return {"stop": True, "reason": "连续两轮无新信息", "exhausted": False}
    if budget_hit:
        # 红线：预算兜底必须显式标未穷尽，不静默
        return {"stop": True, "reason": "预算截断，覆盖可能不完整", "exhausted": True}
    return {"stop": False, "reason": "", "exhausted": False}
