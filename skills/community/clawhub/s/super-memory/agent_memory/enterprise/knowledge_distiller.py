"""
enterprise/knowledge_distiller.py — Distill personal memories into organizational knowledge.

Extract reusable knowledge from individual experiences while
removing personal/private information.

v12: 适配器化 — 优先委托核心 MemoryDistiller 做高质量蒸馏，
     无核心蒸馏器时回退到简陋的拼接截断实现。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class OrganizationalKnowledge:
    """Distilled organizational knowledge."""
    topic: str = ""
    summary: str = ""
    source_count: int = 0
    department: str = ""
    contributors: list[str] = field(default_factory=list)
    confidence: float = 0.0
    tags: list[str] = field(default_factory=list)


class KnowledgeDistiller:
    """Distill personal memories into organizational knowledge.

    Process:
    1. Select work-scope memories from a department
    2. Group by topic
    3. Summarize each group (removing PII)
       - 优先委托核心 MemoryDistiller（高质量 LLM/启发式摘要）
       - 无核心蒸馏器时回退到拼接截断
    4. Create OrganizationalKnowledge entries
    """

    def __init__(self, store=None, compliance_guard=None, core_distiller=None):
        self.store = store
        self.compliance_guard = compliance_guard
        self.core_distiller = core_distiller  # 可选：核心 MemoryDistiller 实例

    def distill(self, department: str = "",
                min_source_count: int = 3) -> list[OrganizationalKnowledge]:
        """Distill organizational knowledge from personal memories.

        Args:
            department: Filter by department
            min_source_count: Minimum memories to form a knowledge item

        Returns:
            List of OrganizationalKnowledge items
        """
        if not self.store:
            return []

        try:
            # Get work-scope memories
            memories = self.store.query(limit=5000) if hasattr(self.store, 'query') else []
            work_memories = [m for m in memories
                           if m.get("tenant_id", "default") in ("work", department)]

            if len(work_memories) < min_source_count:
                return []

            # 优先委托核心蒸馏器
            if self.core_distiller:
                return self._distill_via_core(work_memories, department, min_source_count)

            # 回退：简陋的拼接截断实现
            return self._distill_simple(work_memories, department, min_source_count)

        except Exception as e:
            logger.error("Knowledge distillation failed: %s", e)
            return []

    def _distill_via_core(self, memories: list[dict], department: str,
                          min_source_count: int) -> list[OrganizationalKnowledge]:
        """通过核心 MemoryDistiller 做高质量蒸馏"""
        results = []
        try:
            # 委托核心蒸馏器处理
            core_result = self.core_distiller.distill(force=True)
            topic_summaries = core_result.get("topic_summaries", [])

            for ts in topic_summaries:
                summary_text = ts.get("summary", "")
                if self.compliance_guard and summary_text:
                    summary_text = self.compliance_guard.redact(summary_text)

                results.append(OrganizationalKnowledge(
                    topic=ts.get("topic", ""),
                    summary=summary_text[:500],
                    source_count=ts.get("source_count", 0),
                    department=department,
                    contributors=[],
                    confidence=min(ts.get("source_count", 0) / 10, 1.0),
                    tags=[ts.get("topic", "")],
                ))
        except Exception as e:
            logger.warning("Core distiller failed, falling back to simple: %s", e)
            return self._distill_simple(memories, department, min_source_count)

        return results

    def _distill_simple(self, memories: list[dict], department: str,
                        min_source_count: int) -> list[OrganizationalKnowledge]:
        """结构化回退蒸馏（替代简陋的拼接截断实现）"""
        # Group by topic
        topic_groups: dict[str, list[dict]] = {}
        for mem in memories:
            topics = mem.get("topics", [])
            if isinstance(topics, str):
                try:
                    import json
                    topics = json.loads(topics)
                except Exception:
                    topics = [topics]
            for topic in (topics or ["uncategorized"]):
                topic_groups.setdefault(topic, []).append(mem)

        # Distill each group
        results = []
        for topic, group in topic_groups.items():
            if len(group) < min_source_count:
                continue

            # Sort by importance and recency
            sorted_group = sorted(
                group,
                key=lambda m: (
                    {"high": 3, "normal": 2, "low": 1, "ephemeral": 0}.get(m.get("importance", "normal"), 2),
                    m.get("time_ts", 0),
                ),
                reverse=True,
            )

            # Extract key points from top memories
            key_points = []
            for m in sorted_group[:20]:
                content = (m.get("content") or "").strip()
                if content:
                    first_sentence = content.split("。")[0].split(". ")[0]
                    if len(first_sentence) > 150:
                        first_sentence = first_sentence[:150] + "..."
                    key_points.append(first_sentence)

            # Build structured summary
            topic_str = f"关于{topic}" if topic else "综合"
            summary = f"【{topic_str}知识摘要】\n"
            summary += f"基于 {len(sorted_group)} 条记忆提炼：\n\n"
            for i, point in enumerate(key_points[:15], 1):
                summary += f"{i}. {point}\n"

            if len(sorted_group) > 20:
                summary += f"\n...另有 {len(sorted_group) - 20} 条相关记忆未展示"

            # Redact PII if compliance guard available
            if self.compliance_guard:
                summary = self.compliance_guard.redact(summary)

            ok = OrganizationalKnowledge(
                topic=topic,
                summary=summary[:500],
                source_count=len(group),
                department=department,
                contributors=list(set(m.get("owner_agent_id", "") for m in group
                                    if m.get("owner_agent_id"))),
                confidence=min(len(group) / 10, 1.0),
                tags=[topic],
            )
            results.append(ok)

        return results
