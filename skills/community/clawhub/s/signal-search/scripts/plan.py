"""scripts/plan.py - 意图 + 查询规划（§5.7 / D10）。"""

import re
from typing import Any, Dict, List

INTENT_KEYWORDS = {
    "compare": ["对比", "比较", "区别", "差异", "优劣", " vs ", "对比"],
    "why": ["为什么", "为何", "原因", "怎么选", "凭什么"],
    "howto": ["怎么", "如何", "怎么装", "怎么读", "步骤", "教程", "搭建"],
    "research": ["调研", "研究", "综述", "前沿", "全景", "系统性", "梳理"],
    "latest": ["最新", "今天", "实时", "近期", "2024", "2025", "2026"],
    "verify": ["是否合规", "对不对", "验证", "靠谱吗", "真假"],
}
COMPARE_PAT = re.compile(
    r"对比\s*([^，。；,;]+?)\s*(?:在|于)?\s*([^，。；,;]+?)\s*(?:的|上)?\s*(隐私|差异|区别|合规|表现|覆盖|优劣)",
    re.S,
)


def classify_intent(query: str) -> Dict[str, Any]:
    q = query.strip()
    intent = "fact"
    for it, kws in INTENT_KEYWORDS.items():
        if any(kw in q for kw in kws):
            intent = it
            break
    has_entity = bool(re.search(r"[A-Za-z\u4e00-\u9fa5]{2,}", q))
    confidence = 0.85 if (has_entity and len(q) >= 4) else 0.45
    return {
        "intent": intent,
        "confidence": confidence,
        "granularity": "single" if intent in ("fact", "howto") else "multi",
        "implicit_needs": [],
        "need_clarify": confidence < 0.6,
    }


def plan_queries(query: str, intent: Dict[str, Any], width_cap: int = 20) -> List[Dict[str, Any]]:
    """四范式拆解（成分型 fan-out / 多跳 / 实体锚定 / 迭代重写）；返回叶子列表。

    宽度上限由调用方按 tier 传入（L2<=8, L3<=20），超出截断并标 note。
    """
    q = query.strip()
    leaves: List[Dict[str, Any]] = []
    if "对比" in q:
        after = q.split("对比", 1)[1]
        if "的" in after:
            head, dim = after.rsplit("的", 1)
        else:
            head, dim = after, ""
        entities = [e.strip() for e in re.split(r"[与和及、,，/／]+", head) if e.strip()]
        if dim:
            entities = [e.replace(dim, "").strip() for e in entities]
            entities = [e for e in entities if e]
        if entities:
            dim = dim or "区别"
            for e in entities:
                leaves.append(
                    {
                        "q": f"{e} 的{dim}",
                        "depends_on": [],
                        "rewrite": f"{e} {dim}",
                        "dimension": f"{e}/{dim}",
                    }
                )
    if not leaves:
        # 单叶子（原中英重写变体位为恒等占位、永不触发，已清理，S6）
        leaves.append({"q": q, "depends_on": [], "rewrite": q, "dimension": "default"})

    if len(leaves) > width_cap:
        trimmed = leaves[:width_cap]
        trimmed.append(
            {
                "q": f"(宽度超限，原 {len(leaves)} 叶子截断至 {width_cap})",
                "depends_on": [],
                "rewrite": "",
                "dimension": "note",
                "truncated": True,
            }
        )
        leaves = trimmed
    return leaves
