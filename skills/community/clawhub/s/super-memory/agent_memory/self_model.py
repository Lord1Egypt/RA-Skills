"""
self_model.py - 自我指涉机制

记录 Agent 的推理过程、置信度变化和自我反思。
Phase 2 核心模块。

核心概念：
- ReasoningTrace: 一次检索/决策的推理过程记录
- SelfModel: 管理推理追踪、置信度历史、反思生成

系统不仅记录"世界发生了什么"，还记录"我怎么想的"。
"""

from __future__ import annotations

import time
import json
import uuid
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════
# ReasoningTrace — 单次推理过程
# ═══════════════════════════════════════════════════════

@dataclass
class ReasoningStep:
    """推理中的一个步骤"""
    step_type: str          # fts_search / vec_search / rrf_fusion / rerank / filter / ...
    detail: str             # 描述
    timestamp: float = 0.0  # 步骤时间戳

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()


@dataclass
class ReasoningTrace:
    """一次检索/决策的完整推理记录"""

    trace_id: str = ""
    query: str = ""
    result_summary: str = ""
    confidence: float = 0.0
    sources_consulted: list[str] = field(default_factory=list)
    steps: list[ReasoningStep] = field(default_factory=list)
    alternatives_considered: list[str] = field(default_factory=list)
    uncertainty_factors: list[str] = field(default_factory=list)
    created_at: float = 0.0

    def __post_init__(self):
        if not self.trace_id:
            self.trace_id = f"tr_{uuid.uuid4().hex[:12]}"
        if not self.created_at:
            self.created_at = time.time()

    def add_step(self, step_type: str, detail: str):
        """添加推理步骤"""
        self.steps.append(ReasoningStep(step_type=step_type, detail=detail))

    def add_source(self, memory_id: str):
        """记录查阅了哪条记忆"""
        if memory_id and memory_id not in self.sources_consulted:
            self.sources_consulted.append(memory_id)

    def add_uncertainty(self, factor: str):
        """记录不确定因素"""
        if factor and factor not in self.uncertainty_factors:
            self.uncertainty_factors.append(factor)

    def add_alternative(self, description: str):
        """记录考虑过但排除的方案"""
        if description:
            self.alternatives_considered.append(description)

    def finalize(self, result_summary: str, confidence: float):
        """完成推理追踪"""
        self.result_summary = result_summary
        self.confidence = confidence

    def to_dict(self) -> dict:
        """转为字典（用于序列化存储）"""
        return {
            "trace_id": self.trace_id,
            "query": self.query,
            "result_summary": self.result_summary,
            "confidence": self.confidence,
            "sources_consulted": self.sources_consulted,
            "steps": [
                {"step_type": s.step_type, "detail": s.detail, "timestamp": s.timestamp}
                for s in self.steps
            ],
            "uncertainty_factors": self.uncertainty_factors,
            "alternatives_considered": self.alternatives_considered,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ReasoningTrace":
        """从字典恢复"""
        trace = cls(
            trace_id=data.get("trace_id", ""),
            query=data.get("query", ""),
            result_summary=data.get("result_summary", ""),
            confidence=data.get("confidence", 0.0),
            sources_consulted=data.get("sources_consulted", []),
            uncertainty_factors=data.get("uncertainty_factors", []),
            alternatives_considered=data.get("alternatives_considered", []),
            created_at=data.get("created_at", 0.0),
        )
        for s in data.get("steps", []):
            trace.steps.append(ReasoningStep(**s))
        return trace

    @property
    def step_count(self) -> int:
        return len(self.steps)

    @property
    def source_count(self) -> int:
        return len(self.sources_consulted)

    @property
    def is_uncertain(self) -> bool:
        """是否存在不确定性"""
        return self.confidence < 0.5 or len(self.uncertainty_factors) > 0

    @property
    def duration_seconds(self) -> float:
        """推理总耗时"""
        if not self.steps:
            return 0.0
        return self.steps[-1].timestamp - self.created_at


# ═══════════════════════════════════════════════════════
# SelfModel — 自我认知模型管理
# ═══════════════════════════════════════════════════════

class SelfModel:
    """
    Agent 的自我认知模型。

    核心职责：
    1. 管理推理追踪的生命周期（创建 → 记录 → 完成 → 持久化）
    2. 查询推理历史
    3. 追踪对各主题的置信度变化
    4. 生成自我反思
    """

    def __init__(self, store=None):
        """
        参数:
            store: MemoryStore 实例（用于数据库读写）
        """
        self.store = store
        self._active_traces: dict[str, ReasoningTrace] = {}  # trace_id → trace（进行中）

    # ── 推理追踪生命周期 ─────────────────────────────

    def start_trace(self, query: str) -> ReasoningTrace:
        """开始一次新的推理追踪"""
        trace = ReasoningTrace(query=query)
        self._active_traces[trace.trace_id] = trace
        logger.debug(f"推理追踪开始: {trace.trace_id} query={query[:50]}")
        return trace

    def record_step(self, trace: ReasoningTrace, step_type: str, detail: str):
        """在推理过程中记录步骤"""
        trace.add_step(step_type, detail)

    def record_source(self, trace: ReasoningTrace, memory_id: str):
        """记录本次推理查阅了哪条记忆"""
        trace.add_source(memory_id)

    def record_uncertainty(self, trace: ReasoningTrace, factor: str):
        """记录不确定因素"""
        trace.add_uncertainty(factor)

    def finalize_trace(self, trace: ReasoningTrace, result_summary: str = "", confidence: float = 0.5):
        """完成推理追踪并持久化"""
        trace.finalize(result_summary, confidence)

        # 从活跃列表移除
        self._active_traces.pop(trace.trace_id, None)

        # 持久化到数据库
        if self.store:
            self._persist_trace(trace)

        logger.debug(
            f"推理追踪完成: {trace.trace_id} confidence={confidence:.2f} "
            f"steps={trace.step_count} sources={trace.source_count}"
        )
        return trace

    # ── 查询接口 ─────────────────────────────────────

    def get_traces(self, limit: int = 50, topic: str = None) -> list[dict]:
        """
        获取推理历史。

        参数:
            limit: 返回条数
            topic: 按查询内容过滤（模糊匹配）

        返回: [ReasoningTrace.to_dict(), ...]
        """
        if not self.store:
            return []

        try:
            if topic:
                rows = self.store.conn.execute(
                    """SELECT * FROM reasoning_traces
                       WHERE query LIKE ?
                       ORDER BY created_at DESC LIMIT ?""",
                    (f"%{topic}%", limit),
                ).fetchall()
            else:
                rows = self.store.conn.execute(
                    "SELECT * FROM reasoning_traces ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
        except Exception:
            return []

        traces = []
        for row in rows:
            traces.append({
                "trace_id": row["trace_id"],
                "query": row["query"],
                "result_summary": row["result_summary"],
                "confidence": row["confidence"],
                "sources_used": json.loads(row["sources_used"]) if row["sources_used"] else [],
                "steps": json.loads(row["steps"]) if row["steps"] else [],
                "uncertainty": json.loads(row["uncertainty"]) if row["uncertainty"] else [],
                "created_at": row["created_at"],
            })
        return traces

    def get_confidence_history(self, topic: str = None, limit: int = 100) -> list[dict]:
        """
        获取置信度变化历史。

        参数:
            topic: 按查询内容过滤

        返回: [{"timestamp": float, "query": str, "confidence": float}, ...]
        """
        traces = self.get_traces(limit=limit, topic=topic)
        return [
            {
                "timestamp": t["created_at"],
                "query": t["query"][:60],
                "confidence": t["confidence"],
                "uncertainty_count": len(t.get("uncertainty", [])),
            }
            for t in traces
        ]

    def get_confidence_overview(self) -> dict:
        """
        获取置信度概览：对不同主题的平均置信度。

        返回: {topic_keyword: {"avg_confidence": float, "trace_count": int, "trend": str}}
        """
        traces = self.get_traces(limit=200)
        if not traces:
            return {}

        # 按查询关键词粗略分组
        topic_confidence: dict[str, list[float]] = {}
        for t in traces:
            query = t.get("query", "").strip()
            if not query:
                continue
            # 用查询前 20 字符作为粗略主题 key
            key = query[:20]
            if key not in topic_confidence:
                topic_confidence[key] = []
            topic_confidence[key].append(t.get("confidence", 0.5))

        overview = {}
        for key, confs in topic_confidence.items():
            avg = sum(confs) / len(confs)
            # 趋势：最近 3 个 vs 之前
            if len(confs) >= 4:
                recent_avg = sum(confs[:3]) / 3
                older_avg = sum(confs[3:]) / len(confs[3:])
                if recent_avg > older_avg + 0.1:
                    trend = "rising"
                elif recent_avg < older_avg - 0.1:
                    trend = "falling"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"

            overview[key] = {
                "avg_confidence": round(avg, 3),
                "trace_count": len(confs),
                "trend": trend,
            }

        return overview

    def get_uncertainty_patterns(self, limit: int = 100) -> list[dict]:
        """
        获取不确定因素的模式分析：哪些因素频繁出现。

        返回: [{"factor": str, "count": int, "avg_confidence": float}, ...]
        """
        traces = self.get_traces(limit=limit)
        factor_stats: dict[str, list[float]] = {}

        for t in traces:
            for factor in t.get("uncertainty", []):
                if factor not in factor_stats:
                    factor_stats[factor] = []
                factor_stats[factor].append(t.get("confidence", 0.5))

        result = []
        for factor, confs in factor_stats.items():
            result.append({
                "factor": factor,
                "count": len(confs),
                "avg_confidence": round(sum(confs) / len(confs), 3),
            })

        result.sort(key=lambda x: -x["count"])
        return result

    # ── 反思生成 ─────────────────────────────────────

    def generate_reflection(self, trace: ReasoningTrace) -> Optional[dict]:
        """
        基于推理追踪生成反思。

        当推理置信度低或存在不确定因素时，生成结构化反思。

        返回: {"insight": str, "action": str, "reflection_id": str} 或 None
        """
        if not trace.is_uncertain:
            return None

        # 分析不确定性来源
        insights = []
        actions = []

        if trace.confidence < 0.3:
            insights.append(f"对'{trace.query}'的检索置信度很低（{trace.confidence:.2f}），结果可能不可靠")
            actions.append("建议补充更多相关信息以提高置信度")

        if len(trace.sources_consulted) < 2:
            insights.append("检索结果来源单一，缺乏多角度印证")
            actions.append("尝试从不同角度或主题重新检索")

        for uf in trace.uncertainty_factors:
            if "outdated" in uf.lower() or "过时" in uf:
                insights.append(f"存在信息过时风险: {uf}")
                actions.append("需要确认信息的时效性")
            elif "conflict" in uf.lower() or "矛盾" in uf:
                insights.append(f"存在矛盾信息: {uf}")
                actions.append("需要人工确认哪条信息是正确的")
            elif "missing" in uf.lower() or "缺失" in uf:
                insights.append(f"信息缺失: {uf}")
                actions.append("需要补充缺失的信息维度")

        if not insights:
            insights.append(f"推理过程中存在 {len(trace.uncertainty_factors)} 个不确定因素")

        insight = "；".join(insights)
        action = "；".join(actions) if actions else "暂无建议行动"

        reflection = {
            "insight": insight,
            "action": action,
            "trace_id": trace.trace_id,
            "confidence": trace.confidence,
            "uncertainty_count": len(trace.uncertainty_factors),
        }

        # 持久化反思
        if self.store:
            self._persist_reflection(reflection)

        return reflection

    # ── 持久化 ───────────────────────────────────────

    def _persist_trace(self, trace: ReasoningTrace):
        """将推理追踪写入数据库"""
        if not self.store:
            return
        try:
            self.store.conn.execute(
                """INSERT OR REPLACE INTO reasoning_traces
                   (trace_id, query, result_summary, confidence, sources_used, steps, uncertainty, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    trace.trace_id,
                    trace.query,
                    trace.result_summary,
                    trace.confidence,
                    json.dumps(trace.sources_consulted, ensure_ascii=False),
                    json.dumps(
                        [{"step_type": s.step_type, "detail": s.detail, "timestamp": s.timestamp}
                         for s in trace.steps],
                        ensure_ascii=False,
                    ),
                    json.dumps(trace.uncertainty_factors, ensure_ascii=False),
                    int(trace.created_at),
                ),
            )
            self.store.conn.commit()
        except Exception as e:
            logger.warning("self_model: %s", e)

    def _persist_reflection(self, reflection: dict):
        """将反思写入数据库"""
        if not self.store:
            return
        try:
            ref_id = f"ref_{uuid.uuid4().hex[:12]}"
            self.store.conn.execute(
                """INSERT INTO self_reflections
                   (reflection_id, trace_id, insight, action_taken, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    ref_id,
                    reflection.get("trace_id", ""),
                    reflection.get("insight", ""),
                    reflection.get("action", ""),
                    int(time.time()),
                ),
            )
            self.store.conn.commit()
            reflection["reflection_id"] = ref_id
        except Exception as e:
            logger.warning("self_model: %s", e)

    def get_reflections(self, limit: int = 20) -> list[dict]:
        """获取反思历史"""
        if not self.store:
            return []
        try:
            rows = self.store.conn.execute(
                "SELECT * FROM self_reflections ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [
                {
                    "reflection_id": r["reflection_id"],
                    "trace_id": r["trace_id"],
                    "insight": r["insight"],
                    "action": r["action_taken"],
                    "created_at": r["created_at"],
                }
                for r in rows
            ]
        except Exception:
            return []

    def get_stats(self) -> dict:
        """自我模型统计"""
        if not self.store:
            return {"traces": 0, "reflections": 0, "active_traces": len(self._active_traces)}

        try:
            trace_count = self.store.conn.execute(
                "SELECT COUNT(*) FROM reasoning_traces"
            ).fetchone()[0]
            reflection_count = self.store.conn.execute(
                "SELECT COUNT(*) FROM self_reflections"
            ).fetchone()[0]

            # 最近 20 条的平均置信度
            rows = self.store.conn.execute(
                "SELECT confidence FROM reasoning_traces ORDER BY created_at DESC LIMIT 20"
            ).fetchall()
            avg_conf = sum(r["confidence"] for r in rows) / len(rows) if rows else 0

            return {
                "traces": trace_count,
                "reflections": reflection_count,
                "active_traces": len(self._active_traces),
                "recent_avg_confidence": round(avg_conf, 3),
            }
        except Exception:
            return {"traces": 0, "reflections": 0, "active_traces": len(self._active_traces)}
