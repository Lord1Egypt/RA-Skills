"""v8.9 — memory_decision.py — 记忆驱动决策引擎

原理:
    不是让 LLM 泛泛地"根据记忆做决策"，而是：
    1. 维度坐标交叉分析 — 找出 topic+person+tool 交叉模式
    2. 生命周期追溯 — 相关记忆是否被 superseded/merged/contradicted
    3. 情感趋势加权 — 历史上相似场景的情感 valence 加权 confidence
    4. 生成结构化建议 — recommendation + confidence + evidence + risks

与 v8.9 lifecycle + v8.8 recall 的关系:
    lifecycle: 提供演化链追溯 → decision 知道记忆是否"过时"
    recall: 提供检索结果 → decision 在 top-K 回忆基础上做模式分析
"""

from __future__ import annotations

import time
import json
import hashlib
import logging
from typing import Optional, Callable
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


@dataclass
class EvidenceItem:
    summary: str
    source_id: str
    weight: float = 0.5
    detail: str = ""


@dataclass
class RiskFactor:
    description: str
    severity: str = "medium"  # low/medium/high/critical
    source_id: str = ""
    lifecycle_state: str = ""


@dataclass
class DecisionAdvice:
    recommendation: str
    confidence: float
    evidence: list[dict] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
    risk_factors: list[dict] = field(default_factory=list)
    coordinate_analysis: dict = field(default_factory=dict)
    lifecycle_summary: dict = field(default_factory=dict)
    emotional_context: dict = field(default_factory=dict)


class MemoryDecisionEngine:
    """基于历史记忆的行为模式分析引擎"""

    def __init__(self, store=None, recall_engine=None,
                 lifecycle: 'MemoryLifecycle' = None, emotion_analyzer=None):
        self.store = store
        self.recall = recall_engine
        self.lifecycle = lifecycle
        self.emotion = emotion_analyzer

    def analyze_pattern(self, agent_id: str, query: str,
                        context: dict = None, top_k: int = 20) -> DecisionAdvice:
        relevant = []
        if self.recall:
            try:
                result = self.recall.recall(
                    query=query, limit=top_k,
                    query_agent_id=agent_id,
                )
                relevant = result.get("primary", []) or result.get("results", [])
            except Exception as e:
                logger.warning("memory_decision: %s", e)

        if not relevant and self.store:
            relevant = self.store.query(limit=top_k, query_agent_id=agent_id, keyword=query)

        if not relevant:
            return DecisionAdvice(
                recommendation="no_data",
                confidence=0.0,
                evidence=[{"summary": "无相关记忆", "source_id": ""}],
            )

        coordinate = self._analyze_coordinate_crossing(relevant, agent_id)
        lifecycle = self._analyze_lifecycle_state(relevant)
        emotional = self._analyze_emotional_context(relevant)
        recommendation = self._synthesize(relevant, coordinate, lifecycle, emotional, query)
        return recommendation

    def _analyze_coordinate_crossing(self, memories: list[dict],
                                      agent_id: str) -> dict:
        person_map = {}
        topic_map = {}
        tool_map = {}

        for mem in memories:
            pid = mem.get("person_id", "")
            if pid:
                person_map[pid] = person_map.get(pid, 0) + 1

            topics = mem.get("topics", [])
            for t in topics:
                tc = t.get("code", str(t)) if isinstance(t, dict) else str(t)
                topic_map[tc] = topic_map.get(tc, 0) + 1

            tools = mem.get("tools", [])
            for t in tools:
                tid = t.get("code", str(t)) if isinstance(t, dict) else str(t)
                tool_map[tid] = tool_map.get(tid, 0) + 1

        top_persons = sorted(person_map.items(), key=lambda x: -x[1])[:3]
        top_topics = sorted(topic_map.items(), key=lambda x: -x[1])[:3]
        top_tools = sorted(tool_map.items(), key=lambda x: -x[1])[:3]

        return {
            "dominant_agents": top_persons,
            "dominant_topics": top_topics,
            "dominant_tools": top_tools,
            "total_memories_analyzed": len(memories),
        }

    def _analyze_lifecycle_state(self, memories: list[dict]) -> dict:
        state_counts = {"active": 0, "superseded": 0, "merged": 0,
                        "decaying": 0, "deprecated": 0, "unknown": 0}
        outdated = []

        for mem in memories:
            state = mem.get("lifecycle_state", "active")
            state_counts[state] = state_counts.get(state, 0) + 1

            if state in ("superseded", "deprecated", "decaying"):
                outdated.append({
                    "memory_id": mem.get("memory_id", "")[:32],
                    "state": state,
                    "content_preview": (mem.get("content", "") or "")[:60],
                })

        return {
            "state_distribution": state_counts,
            "outdated_count": len(outdated),
            "outdated_items": outdated[:5],
            "reliability": 1.0 - len(outdated) / max(len(memories), 1),
        }

    def _analyze_emotional_context(self, memories: list[dict]) -> dict:
        if not self.emotion:
            return {"available": False}

        valences = []
        for mem in memories:
            primary = mem.get("primary_emotions", "{}")
            try:
                emotions = json.loads(primary) if isinstance(primary, str) else primary
                v = emotions.get("valence", mem.get("valence", 0))
                valences.append(float(v))
            except (json.JSONDecodeError, ValueError, TypeError):
                valences.append(0.0)

        if not valences:
            return {"available": True, "avg_valence": 0, "valence_count": 0}

        avg = sum(valences) / len(valences)
        pos = sum(1 for v in valences if v > 0.15)
        neg = sum(1 for v in valences if v < -0.15)
        neutral = len(valences) - pos - neg

        return {
            "available": True,
            "avg_valence": round(avg, 3),
            "positive_ratio": round(pos / len(valences), 3),
            "negative_ratio": round(neg / len(valences), 3),
            "neutral_ratio": round(neutral / len(valences), 3),
            "trend": "rising" if avg > 0.3 else "declining" if avg < -0.3 else "stable",
            "valence_count": len(valences),
        }

    def _synthesize(self, memories: list[dict], coordinate: dict,
                     lifecycle: dict, emotional: dict, query: str) -> DecisionAdvice:
        evidence = []
        risk_factors = []

        for mc in coordinate.get("dominant_topics", [])[:2]:
            topic, count = mc
            evidence.append({
                "summary": f"主题 '{topic}' 出现 {count} 次",
                "source_id": f"coordinate:topic:{topic}",
                "weight": min(1.0, count / 5),
                "detail": f"跨 {coordinate.get('total_memories_analyzed', 0)} 条记忆的分析",
            })

        for pa in coordinate.get("dominant_agents", []):
            agent, count = pa
            evidence.append({
                "summary": f"Agent '{agent}' 参与 {count} 次",
                "source_id": f"coordinate:agent:{agent}",
                "weight": min(0.8, count / 10),
                "detail": "高频参与者",
            })

        reliability = lifecycle.get("reliability", 1.0)
        if lifecycle.get("outdated_count", 0) > 0:
            evidence.append({
                "summary": f"{lifecycle['outdated_count']} 条记忆已过时（superseded/deprecated）",
                "source_id": "lifecycle:state",
                "weight": -0.3,
                "detail": "降低总体置信度",
            })
            risk_factors.append({
                "description": f"{lifecycle['outdated_count']} 条过时记忆可能影响判断",
                "severity": "medium" if lifecycle['outdated_count'] < 5 else "high",
                "source_id": "lifecycle:state",
                "lifecycle_state": "outdated",
            })

        if emotional.get("available") and emotional.get("negative_ratio", 0) > 0.5:
            risk_factors.append({
                "description": f"相关记忆中 {emotional['negative_ratio']:.0%} 带有负面情感",
                "severity": "medium",
                "source_id": "emotion:valence",
                "lifecycle_state": "active",
            })

        confidence = (0.6 + reliability * 0.3 + emotional.get("positive_ratio", 0.5) * 0.1)
        confidence = max(0.1, min(0.95, confidence))

        recommendation_text = self._generate_recommendation(
            memories, coordinate, confidence, query
        )

        alternatives = [f"{t[0]} (频次={t[1]})" for t in coordinate.get("dominant_topics", [])[1:3]]

        return DecisionAdvice(
            recommendation=recommendation_text,
            confidence=round(confidence, 3),
            evidence=evidence,
            alternatives=alternatives,
            risk_factors=risk_factors,
            coordinate_analysis=coordinate,
            lifecycle_summary=lifecycle,
            emotional_context=emotional,
        )

    def _generate_recommendation(self, memories: list[dict],
                                  coordinate: dict, confidence: float,
                                  query: str) -> str:
        top_topics = coordinate.get("dominant_topics", [])
        top_agents = coordinate.get("dominant_agents", [])

        if not top_topics:
            return f"关于 '{query[:30]}' 的相关记忆不足，无法生成可靠建议"

        primary_topic = top_topics[0][0] if top_topics else "unknown"
        primary_agent = top_agents[0][0] if top_agents else "unknown_agent"
        count = len(memories)
        conf_label = "高" if confidence > 0.7 else "中" if confidence > 0.4 else "低"

        content_samples = [m.get("content", "")[:80] for m in memories[:3]]
        context_hint = " | ".join(content_samples)

        return (
            f"基于 {count} 条记忆分析（置信度: {conf_label}@{confidence:.0%}）:\n"
            f"- 核心主题: {primary_topic}\n"
            f"- 主要关联 Agent: {primary_agent}\n"
            f"- 最近相关记忆: {context_hint[:120]}"
        )