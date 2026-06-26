"""
motivation.py - 内在动机系统（v7.1 增强版）

Agent 的"好奇心"和"偏好"：在无外部刺激时主动探索。

Phase 4 核心模块。

核心概念：
- InternalState: 内在状态（好奇心、无聊度、自信度、满足感、紧迫感）
- MotivationEngine: 基于记忆内容动态更新内在状态
  - 好奇驱动：知识空白 + 信息质量 → 产生探索任务
  - 无聊驱动：重复信息 + 低信息熵 → 寻求新意
  - 学习动量：追踪学习曲线，检测"卡住"状态

v7.1 改进：
- 好奇心不再只看"新主题多不多"，而是看信息质量 + 覆盖度
- 无聊度考虑信息熵（重复内容 vs 多样内容）
- 新增学习动量维度：连续进步 vs 连续卡住
- 新增信息熵计算
- LLM 接入：信息质量深度评估（非关键词打分）
- 可观测性：每次 update_state 返回 trace
"""

from __future__ import annotations

import time
import json
import math
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional, Callable

logger = logging.getLogger(__name__)

# 每天秒数
_DAY = 86400


# ═══════════════════════════════════════════════════════
# InternalState — 内在状态
# ═══════════════════════════════════════════════════════

@dataclass
class InternalState:
    """Agent 的内在状态快照（v7.1 增强版）"""

    curiosity: float = 0.3        # [0, 1] 对未知的好奇
    boredom: float = 0.0          # [0, 1] 无新信息的无聊度
    confidence: float = 0.5       # [0, 1] 对当前知识的自信
    satisfaction: float = 0.5     # [0, 1] 目标达成满足感
    urgency: float = 0.0          # [0, 1] 时间紧迫感
    momentum: float = 0.5         # [0, 1] 学习动量（v7.1：进步趋势）
    entropy: float = 0.5          # [0, 1] 信息熵（v7.1：内容多样性）
    dominant_drive: str = "none"  # 当前主导动机

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def mood_summary(self) -> str:
        """人类可读的情绪摘要"""
        parts = []
        if self.curiosity > 0.6:
            parts.append("好奇")
        if self.boredom > 0.5:
            parts.append("无聊")
        if self.confidence < 0.3:
            parts.append("不确定")
        if self.satisfaction > 0.7:
            parts.append("满足")
        if self.urgency > 0.6:
            parts.append("紧迫")
        if self.momentum > 0.7:
            parts.append("在进步")
        elif self.momentum < 0.3:
            parts.append("卡住了")
        if not parts:
            parts.append("平静")
        return "、".join(parts)

    @property
    def mood_emoji(self) -> str:
        if self.curiosity > 0.6:
            return "🤔"
        if self.boredom > 0.5:
            return "😑"
        if self.satisfaction > 0.7:
            return "😊"
        if self.urgency > 0.6:
            return "⚡"
        if self.confidence < 0.3:
            return "❓"
        if self.momentum < 0.3:
            return "😰"
        return "😌"


# ═══════════════════════════════════════════════════════
# MotivationEngine — 内在动机引擎
# ═══════════════════════════════════════════════════════

class MotivationEngine:
    """
    内在动机引擎（v7.1 增强版）。

    基于最近记忆动态更新 Agent 的内在状态，
    并在特定条件下生成主动探索任务。

    使用模式：
        motivation = MotivationEngine(store, llm_fn=my_llm)
        state, trace = motivation.update_state(recent_memories)
        tasks = motivation.generate_curiosity_tasks()
        gaps = motivation.detect_knowledge_gaps()
    """

    # 衰减率：每次 update 时各维度向基线收敛
    DECAY_RATE = 0.15
    # 基线值
    BASELINES = {
        "curiosity": 0.3,
        "boredom": 0.0,
        "confidence": 0.5,
        "satisfaction": 0.5,
        "urgency": 0.0,
        "momentum": 0.5,
        "entropy": 0.5,
    }

    def __init__(self, store=None, topic_registry=None, llm_fn: Callable = None):
        """
        参数:
            store: MemoryStore 实例
            topic_registry: TopicRegistry 实例（用于检测知识空白）
            llm_fn: LLM 函数 fn(prompt: str) -> str。
                    用于信息质量深度评估和探索任务语义生成。
                    不传则降级为规则模式。
        """
        self.store = store
        self.topic_registry = topic_registry
        self.llm_fn = llm_fn
        self._state = InternalState()
        self._last_update_ts = 0.0
        self._recent_queries: list[str] = []  # 最近的查询（用于无聊度计算）
        self._recent_significances: list[str] = []  # 最近的情感标签
        self._update_count: int = 0
        self._trigger_thresholds = {k: dict(v) for k, v in self.TRIGGER_THRESHOLDS.items()}

    @property
    def state(self) -> InternalState:
        """当前内在状态"""
        return self._state

    # ── 状态更新 ─────────────────────────────────────

    def update_state(self, recent_memories: list[dict] = None) -> tuple[InternalState, dict]:
        """
        基于最近记忆更新内在状态（v7.1 增强版）。

        参数:
            recent_memories: 最近写入/检索的记忆列表

        返回: (InternalState, trace_dict)
        """
        now = time.time()
        t_start = time.monotonic()
        s = self._state
        self._update_count += 1
        trace = {"steps": [], "delta": {}, "before": s.to_dict()}

        # ── 向基线衰减 ───────────────────────────────
        for dim in ("curiosity", "boredom", "confidence", "satisfaction", "urgency", "momentum", "entropy"):
            current = getattr(s, dim)
            baseline = self.BASELINES[dim]
            new_val = current + (baseline - current) * self.DECAY_RATE
            setattr(s, dim, round(max(0.0, min(1.0, new_val)), 3))

        if not recent_memories:
            self._update_dominant_drive()
            self._last_update_ts = now
            trace["steps"].append("no_memories: decay_only")
            trace["elapsed_ms"] = round((time.monotonic() - t_start) * 1000, 2)
            trace["after"] = s.to_dict()
            return s, trace

        # ── 信息熵计算 ───────────────────────────────
        entropy = self._compute_information_entropy(recent_memories)
        s.entropy = round(entropy, 3)
        trace["steps"].append(f"entropy={entropy:.3f}")

        # ── 好奇心：信息质量 + 覆盖度 ────────────────
        # v7.1: 不再只看"新主题多不多"，而是综合评估
        new_topics = set()
        novelty_count = 0
        high_quality_count = 0
        for m in recent_memories:
            for t in m.get("topics", []):
                code = t.get("code", t) if isinstance(t, dict) else t
                new_topics.add(code)
            sig = m.get("significance", "")
            if sig in ("breakthrough", "crisis", "milestone"):
                novelty_count += 1
                self._recent_significances.append(sig)
            # 高置信 + 高重要度 = 高质量信息
            if m.get("importance") == "high" and m.get("confidence", 0) > 0.6:
                high_quality_count += 1

        if new_topics:
            topic_novelty = min(1.0, len(new_topics) / 10)
            # 质量加权：高质量信息对好奇心的刺激更大
            quality_weight = 1.0 + 0.5 * (high_quality_count / max(1, len(recent_memories)))
            s.curiosity = min(1.0, s.curiosity + topic_novelty * 0.1 * quality_weight)

        if novelty_count > 0:
            s.curiosity = min(1.0, s.curiosity + novelty_count * 0.05)

        # 高信息熵 → 好奇心上升（信息多样刺激探索欲）
        if entropy > 0.7:
            s.curiosity = min(1.0, s.curiosity + 0.05)

        trace["steps"].append(
            f"curiosity: topics={len(new_topics)}, novelty={novelty_count}, "
            f"high_quality={high_quality_count}, result={s.curiosity:.3f}"
        )

        # ── 无聊度：信息熵 + 重复度 + 低质量 ───────
        # v7.1: 低信息熵直接提升无聊度
        if entropy < 0.3:
            s.boredom = min(1.0, s.boredom + (0.3 - entropy) * 0.5)

        low_info_count = sum(
            1 for m in recent_memories
            if m.get("importance") == "low" or m.get("significance") == "trivial"
        )
        if low_info_count > len(recent_memories) * 0.6:
            s.boredom = min(1.0, s.boredom + 0.15)

        # 查询重复度 → 无聊度
        if len(self._recent_queries) >= 3:
            recent_q = self._recent_queries[-10:]
            unique_queries = set(recent_q)
            repetition_rate = 1.0 - len(unique_queries) / max(1, len(recent_q))
            s.boredom = min(1.0, s.boredom + repetition_rate * 0.1)

        trace["steps"].append(
            f"boredom: entropy={entropy:.2f}, low_info={low_info_count}/{len(recent_memories)}, "
            f"result={s.boredom:.3f}"
        )

        # ── 自信度 ───────────────────────────────────
        high_importance = sum(1 for m in recent_memories if m.get("importance") == "high")
        if high_importance > 0:
            s.confidence = min(1.0, s.confidence + high_importance * 0.03)

        if novelty_count > 0:
            s.confidence = min(1.0, s.confidence + 0.05)

        # 高信息熵 → 对当前知识体系更自信（覆盖面广）
        if entropy > 0.6:
            s.confidence = min(1.0, s.confidence + 0.02)

        # ── 满足感 ───────────────────────────────────
        positive_significances = sum(
            1 for sig in self._recent_significances[-5:]
            if sig in ("breakthrough", "milestone")
        )
        if positive_significances > 0:
            s.satisfaction = min(1.0, s.satisfaction + positive_significances * 0.08)

        # ── 学习动量 ─────────────────────────────────
        # 基于近期记忆的 valence 趋势
        # ⚠️ 安全: 情感稳态机制 — momentum 有下限(0.15)，
        # 防止持续负面 valence 导致动机完全衰退。
        # Agent 不会因为"害怕"而停止工作。
        MOMENTUM_FLOOR = 0.15
        valences = [m.get("valence", 0) for m in recent_memories if m.get("valence") is not None]
        if valences:
            avg_valence = sum(valences) / len(valences)
            if avg_valence > 0.2:
                s.momentum = min(1.0, s.momentum + 0.08)
            elif avg_valence < -0.2:
                s.momentum = max(MOMENTUM_FLOOR, s.momentum - 0.08)
                if s.momentum <= MOMENTUM_FLOOR:
                    logger.info(f"Motivation floor reached ({MOMENTUM_FLOOR}), negative valence dampened")

        trace["steps"].append(f"momentum={s.momentum:.3f}")

        # ── 紧迫感：deadline 任务 ────────────────────
        if self.store:
            try:
                urgent_tasks = self.store.conn.execute(
                    """SELECT COUNT(*) FROM tasks
                       WHERE status IN ('pending', 'in_progress')
                       AND deadline IS NOT NULL
                       AND deadline < ?""",
                    (int(now) + _DAY * 2,),
                ).fetchone()[0]
                if urgent_tasks > 0:
                    s.urgency = min(1.0, 0.3 + urgent_tasks * 0.15)
            except Exception as e:
                logger.warning("motivation: %s", e)

        # ── LLM 信息质量评估（可选）──────────────────
        if self.llm_fn and len(recent_memories) >= 3:
            try:
                llm_quality = self._assess_quality_with_llm(recent_memories[:5])
                if llm_quality:
                    # LLM 评估结果微调好奇心和自信度
                    novelty_score = llm_quality.get("novelty", 0.5)
                    depth_score = llm_quality.get("depth", 0.5)
                    if novelty_score > 0.7:
                        s.curiosity = min(1.0, s.curiosity + 0.05)
                    if depth_score > 0.7:
                        s.confidence = min(1.0, s.confidence + 0.03)
                    trace["steps"].append(
                        f"llm_quality: novelty={novelty_score:.2f}, depth={depth_score:.2f}"
                    )
            except Exception as e:
                trace["steps"].append(f"llm_quality_error: {e}")

        # ── 更新主导动机 ─────────────────────────────
        self._update_dominant_drive()
        self._last_update_ts = now

        # 持久化
        self._persist_state()

        # ── 可观测性 ─────────────────────────────────
        trace["elapsed_ms"] = round((time.monotonic() - t_start) * 1000, 2)
        trace["after"] = s.to_dict()
        trace["delta"] = {
            k: round(trace["after"][k] - trace["before"][k], 3)
            for k in trace["before"]
            if isinstance(trace["before"][k], (int, float))
        }
        trace["dominant_drive"] = s.dominant_drive

        if any(abs(v) > 0.1 for v in trace["delta"].values()):
            logger.debug(
                f"Motivation update #{self._update_count}: "
                f"drive={s.dominant_drive}, "
                f"curiosity={s.curiosity:.2f}, boredom={s.boredom:.2f}, "
                f"momentum={s.momentum:.2f}, entropy={s.entropy:.2f}, "
                f"{trace['elapsed_ms']:.1f}ms"
            )

        return s, trace

    def _compute_information_entropy(self, memories: list[dict]) -> float:
        """
        计算信息熵：衡量内容多样性。

        基于主题分布的香农熵：
        - 所有记忆集中在一个主题 → 熵低（无聊）
        - 记忆均匀分布在多个主题 → 熵高（丰富）

        返回: [0.0, 1.0]
        """
        if not memories:
            return 0.5

        # 统计主题分布
        topic_counts = {}
        for m in memories:
            topics = m.get("topics", [])
            if not topics:
                topic_counts["__none__"] = topic_counts.get("__none__", 0) + 1
                continue
            for t in topics:
                code = t.get("code", t) if isinstance(t, dict) else t
                topic_counts[code] = topic_counts.get(code, 0) + 1

        if not topic_counts:
            return 0.5

        # 只有 __none__ 主题 → 没有有效信息，返回中等
        if set(topic_counts.keys()) == {"__none__"}:
            return 0.5

        # 去掉 __none__ 计算真实熵
        real_counts = {k: v for k, v in topic_counts.items() if k != "__none__"}
        if not real_counts:
            return 0.5

        # 香农熵
        total = sum(real_counts.values())
        entropy = 0.0
        for count in real_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)

        # 归一化到 [0, 1]（最大熵 = log2(n_topics)）
        n_topics = len(real_counts)
        max_entropy = math.log2(max(2, n_topics))
        if max_entropy > 0:
            return entropy / max_entropy
        return 0.5

    def _assess_quality_with_llm(self, memories: list[dict]) -> Optional[dict]:
        """
        用 LLM 评估近期记忆的信息质量。

        返回: {"novelty": float, "depth": float, "coherence": float} 或 None
        """
        if not self.llm_fn:
            return None

        contents = []
        for m in memories[:5]:
            c = m.get("content", "")[:200]
            contents.append(f"- {c}")

        prompt = (
            "评估以下记忆片段的整体信息质量。返回 JSON，不要输出其他内容。\n\n"
            "维度（0.0-1.0）：\n"
            "- novelty: 信息新颖度（有新知识/新观点？还是重复已知？）\n"
            "- depth: 信息深度（有实质内容？还是表面描述？）\n"
            "- coherence: 连贯性（这些片段之间有逻辑关联？）\n\n"
            "记忆片段：\n" + "\n".join(contents) + "\n\n"
            "JSON: {\"novelty\": 0.0, \"depth\": 0.0, \"coherence\": 0.0}"
        )

        try:
            import re
            response = self.llm_fn(prompt)
            if not response:
                return None
            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    "novelty": max(0.0, min(1.0, float(result.get("novelty", 0.5)))),
                    "depth": max(0.0, min(1.0, float(result.get("depth", 0.5)))),
                    "coherence": max(0.0, min(1.0, float(result.get("coherence", 0.5)))),
                }
        except Exception as e:
            logger.debug(f"LLM 质量评估失败: {e}")

        return None

    def _update_dominant_drive(self):
        """根据当前状态确定主导动机"""
        s = self._state
        drives = {
            "curiosity_explore": s.curiosity,
            "boredom_break": s.boredom,
            "confidence_build": 1.0 - s.confidence,
            "goal_achieve": 1.0 - s.satisfaction,
            "deadline_urgent": s.urgency,
            "stuck_escape": 1.0 - s.momentum if s.momentum < 0.3 and s.momentum > 0.15 else 0.0,
        }
        dominant = max(drives, key=drives.get)
        if drives[dominant] > 0.4:
            s.dominant_drive = dominant
        else:
            s.dominant_drive = "none"

    # ── 知识空白检测 ─────────────────────────────────

    def detect_knowledge_gaps(self) -> list[dict]:
        """
        检测知识图谱中的空白。

        方法：
        1. 已注册但无记忆的主题
        2. 记忆很少的主题（<3 条）
        3. 长时间未更新的主题（>30 天）
        4. 低置信主题（平均 confidence < 0.4）

        返回: [{"topic": str, "gap_type": str, "detail": str, "priority": float}]
        """
        if not self.store:
            return []

        gaps = []

        try:
            # 统计每个主题的记忆数
            topic_counts = self.store.conn.execute(
                """SELECT mt.topic_code, COUNT(*) as cnt,
                          MAX(m.time_ts) as latest_ts,
                          AVG(COALESCE(m.confidence, 0.5)) as avg_confidence
                   FROM memory_topics mt
                   JOIN memories m ON m.memory_id = mt.memory_id
                   GROUP BY mt.topic_code"""
            ).fetchall()

            now = time.time()
            topic_stats = {}
            for row in topic_counts:
                topic_stats[row["topic_code"]] = {
                    "count": row["cnt"],
                    "latest_ts": row["latest_ts"],
                    "avg_confidence": row["avg_confidence"] or 0.5,
                }

            # 检查注册表中的主题
            if self.topic_registry:
                try:
                    all_topics = self.topic_registry.get_all_topic_codes()
                    for topic_code in all_topics:
                        if topic_code not in topic_stats:
                            gaps.append({
                                "topic": topic_code,
                                "gap_type": "empty_topic",
                                "detail": f"主题已注册但无记忆",
                                "priority": 0.7,
                            })
                except Exception as e:
                    logger.warning("motivation: %s", e)

            # 检查已有主题的薄弱环节
            for topic_code, stats in topic_stats.items():
                if stats["count"] < 3:
                    gaps.append({
                        "topic": topic_code,
                        "gap_type": "sparse_topic",
                        "detail": f"仅有 {stats['count']} 条记忆",
                        "priority": 0.5,
                    })

                age_days = (now - stats["latest_ts"]) / _DAY if stats["latest_ts"] else 999
                if age_days > 30:
                    gaps.append({
                        "topic": topic_code,
                        "gap_type": "stale_topic",
                        "detail": f"最近更新在 {int(age_days)} 天前",
                        "priority": round(0.3 + min(0.4, age_days / 90), 2),
                    })

                # 低置信主题
                if stats["avg_confidence"] < 0.4 and stats["count"] >= 2:
                    gaps.append({
                        "topic": topic_code,
                        "gap_type": "low_confidence",
                        "detail": f"平均置信度仅 {stats['avg_confidence']:.2f}",
                        "priority": round(0.4 + (0.4 - stats["avg_confidence"]), 2),
                    })

        except Exception as e:
            logger.warning("motivation: %s", e)

        # 按优先级排序
        gaps.sort(key=lambda g: -g["priority"])
        return gaps

    # ── 好奇驱动任务 ─────────────────────────────────

    def generate_curiosity_tasks(self) -> list[dict]:
        """
        基于好奇心和知识空白生成探索任务。

        返回: [{"title": str, "reason": str, "topic": str, "priority": float}]
        """
        tasks = []

        # 基于知识空白
        gaps = self.detect_knowledge_gaps()
        for gap in gaps[:3]:
            if gap["gap_type"] == "empty_topic":
                tasks.append({
                    "title": f"探索主题: {gap['topic']}",
                    "reason": f"该主题已注册但无任何记忆，值得探索",
                    "topic": gap["topic"],
                    "priority": gap["priority"],
                })
            elif gap["gap_type"] in ("sparse_topic", "low_confidence"):
                tasks.append({
                    "title": f"补充主题: {gap['topic']}",
                    "reason": gap["detail"],
                    "topic": gap["topic"],
                    "priority": gap["priority"],
                })
            elif gap["gap_type"] == "stale_topic":
                tasks.append({
                    "title": f"更新主题: {gap['topic']}",
                    "reason": gap["detail"],
                    "topic": gap["topic"],
                    "priority": gap["priority"],
                })

        # 基于好奇心状态
        if self._state.curiosity > 0.7:
            tasks.append({
                "title": "探索新方向",
                "reason": f"好奇心较高（{self._state.curiosity:.2f}），建议尝试新的查询或主题",
                "topic": None,
                "priority": self._state.curiosity,
            })

        # 基于低动量（卡住了 → 换方向）
        if self._state.momentum < 0.3:
            tasks.append({
                "title": "换个方向试试",
                "reason": f"学习动量偏低（{self._state.momentum:.2f}），可能需要换一个探索角度",
                "topic": None,
                "priority": 0.6,
            })

        # 基于低信息熵（信息太集中 → 扩展视野）
        if self._state.entropy < 0.3:
            tasks.append({
                "title": "扩展知识面",
                "reason": f"信息熵偏低（{self._state.entropy:.2f}），当前信息集中在少数主题",
                "topic": None,
                "priority": 0.5,
            })

        return tasks

    # ── 无聊度分析 ───────────────────────────────────

    def compute_boredom_analysis(self) -> dict:
        """
        分析无聊度的构成。

        返回: {"score": float, "factors": list[str], "suggestion": str}
        """
        factors = []
        s = self._state

        if s.boredom > 0.3:
            if len(self._recent_queries) >= 3:
                unique = set(self._recent_queries[-10:])
                rep_rate = 1.0 - len(unique) / max(1, len(self._recent_queries[-10:]))
                if rep_rate > 0.3:
                    factors.append(f"查询重复率 {rep_rate:.0%}")

            low_sig = sum(1 for sig in self._recent_significances[-10:] if sig == "trivial")
            if low_sig > 5:
                factors.append(f"近期 {low_sig} 条低显著性记忆")

            if s.entropy < 0.3:
                factors.append(f"信息熵低（{s.entropy:.2f}），内容过于集中")

        suggestion = ""
        if s.boredom > 0.5:
            suggestion = "建议探索新主题或从不同角度查询已有主题"
        elif s.boredom > 0.3:
            suggestion = "信息流有些单调，可以尝试多样化查询"

        return {
            "score": s.boredom,
            "factors": factors,
            "suggestion": suggestion,
            "entropy": s.entropy,
            "momentum": s.momentum,
        }

    # ── 查询追踪（供外部调用）────────────────────────

    def record_query(self, query: str):
        """记录一次查询（用于无聊度计算）"""
        if query:
            self._recent_queries.append(query)
            if len(self._recent_queries) > 50:
                self._recent_queries = self._recent_queries[-30:]

    # ── 持久化 ───────────────────────────────────────

    def _persist_state(self):
        """将内在状态写入数据库"""
        if not self.store:
            return
        try:
            self.store.conn.execute(
                """INSERT OR REPLACE INTO internal_state
                   (state_id, curiosity, boredom, confidence, satisfaction, urgency,
                    dominant_drive, updated_at)
                   VALUES ('current', ?, ?, ?, ?, ?, ?, ?)""",
                (
                    self._state.curiosity,
                    self._state.boredom,
                    self._state.confidence,
                    self._state.satisfaction,
                    self._state.urgency,
                    self._state.dominant_drive,
                    int(time.time()),
                ),
            )
            self.store.conn.commit()
        except Exception as e:
            logger.debug(f"内在状态持久化失败（表可能尚未创建）: {e}")

    def load_state(self):
        """从数据库加载内在状态"""
        if not self.store:
            return
        try:
            row = self.store.conn.execute(
                "SELECT * FROM internal_state WHERE state_id = 'current'"
            ).fetchone()
            if row:
                self._state.curiosity = row["curiosity"]
                self._state.boredom = row["boredom"]
                self._state.confidence = row["confidence"]
                self._state.satisfaction = row["satisfaction"]
                self._state.urgency = row["urgency"]
                self._state.dominant_drive = row["dominant_drive"]
                self._last_update_ts = row["updated_at"]
                logger.debug(f"内在状态已加载: {self._state.mood_summary}")
        except Exception as e:
            logger.warning("motivation: %s", e)

    # ── 统计 ─────────────────────────────────────────

    def get_stats(self) -> dict:
        """动机引擎统计"""
        return {
            "state": self._state.to_dict(),
            "mood": self._state.mood_summary,
            "mood_emoji": self._state.mood_emoji,
            "knowledge_gaps": len(self.detect_knowledge_gaps()),
            "recent_queries_tracked": len(self._recent_queries),
            "update_count": self._update_count,
            "has_llm": self.llm_fn is not None,
        }

    # ══════════════════════════════════════════════════════
    # v8.3: 触发机制
    # ══════════════════════════════════════════════════════

    TRIGGER_THRESHOLDS = {
        "curiosity_high": {"field": "curiosity", "op": ">", "value": 0.7, "action": "explore"},
        "boredom_high": {"field": "boredom", "op": ">", "value": 0.6, "action": "diversify"},
        "confidence_low": {"field": "confidence", "op": "<", "value": 0.3, "action": "verify"},
        "momentum_low": {"field": "momentum", "op": "<", "value": 0.25, "action": "redirect"},
        "urgency_high": {"field": "urgency", "op": ">", "value": 0.7, "action": "prioritize"},
        "entropy_low": {"field": "entropy", "op": "<", "value": 0.25, "action": "broaden"},
        "satisfaction_high": {"field": "satisfaction", "op": ">", "value": 0.8, "action": "consolidate"},
    }

    def check_triggers(self) -> list[dict]:
        """
        检查内在状态是否触发了任何行动。

        返回: [{
            "trigger": str,
            "field": str,
            "value": float,
            "threshold": float,
            "action": str,
            "suggestions": [str],
        }]
        """
        triggered = []
        s = self._state

        for trigger_name, config in self._trigger_thresholds.items():
            field_value = getattr(s, config["field"], None)
            if field_value is None:
                continue

            is_triggered = False
            if config["op"] == ">" and field_value > config["value"]:
                is_triggered = True
            elif config["op"] == "<" and field_value < config["value"]:
                is_triggered = True

            if is_triggered:
                suggestions = self._generate_trigger_suggestions(config["action"], field_value)
                triggered.append({
                    "trigger": trigger_name,
                    "field": config["field"],
                    "value": round(field_value, 3),
                    "threshold": config["value"],
                    "action": config["action"],
                    "suggestions": suggestions,
                })

        if triggered:
            logger.info(f"🎯 动机触发: {len(triggered)} 个触发器激活 "
                         f"({', '.join(t['trigger'] for t in triggered)})")

        return triggered

    def _generate_trigger_suggestions(self, action: str, value: float) -> list[str]:
        """根据触发的行动类型生成具体建议"""
        suggestions = []

        if action == "explore":
            gaps = self.detect_knowledge_gaps()[:3]
            for g in gaps:
                suggestions.append(f"探索主题 '{g['topic']}' ({g['gap_type']})")
            suggestions.append("尝试提出一个从未问过的问题")

        elif action == "diversify":
            suggestions.append("切换到一个完全不同的主题领域")
            suggestions.append("回顾并补充之前忽略的知识点")
            suggestions.append("从不同角度重新审视已有信息")

        elif action == "verify":
            suggestions.append("验证最近记录的关键信息是否准确")
            suggestions.append("查找已有知识的反例或矛盾")
            suggestions.append("向用户确认不确定的信息")

        elif action == "redirect":
            suggestions.append("当前方向可能遇到瓶颈，尝试换一个角度")
            suggestions.append("回顾之前的成功经验，寻找新的突破口")
            suggestions.append("暂时放下当前问题，处理其他待办事项")

        elif action == "prioritize":
            suggestions.append("有紧急任务需要处理，优先完成截止日期临近的任务")
            suggestions.append("暂时搁置探索性活动，集中精力完成紧急事项")

        elif action == "broaden":
            suggestions.append("当前知识过于集中，建议拓展到相关领域")
            suggestions.append("尝试跨主题的关联思考")

        elif action == "consolidate":
            suggestions.append("学习效果良好，建议总结和巩固已有知识")
            suggestions.append("将碎片化的理解整理成系统性的知识框架")

        return suggestions[:3]

    # ══════════════════════════════════════════════════════
    # v8.3: 主动探索
    # ══════════════════════════════════════════════════════

    def generate_proactive_actions(self, max_actions: int = 5) -> list[dict]:
        """
        基于当前内在状态生成主动行动建议。

        综合考虑：
        1. 触发器状态
        2. 知识空白
        3. 好奇心任务
        4. 主导动机

        返回: [{
            "action_type": str,
            "title": str,
            "reason": str,
            "priority": float,
            "topic": str | None,
            "estimated_impact": str,
        }]
        """
        actions = []

        triggers = self.check_triggers()
        for t in triggers:
            for suggestion in t["suggestions"]:
                actions.append({
                    "action_type": t["action"],
                    "title": suggestion,
                    "reason": f"{t['trigger']} 触发 (值={t['value']:.2f}, 阈值={t['threshold']})",
                    "priority": 0.8,
                    "topic": None,
                    "estimated_impact": "高" if t["action"] in ("explore", "prioritize") else "中",
                })

        curiosity_tasks = self.generate_curiosity_tasks()
        for task in curiosity_tasks:
            actions.append({
                "action_type": "curiosity_driven",
                "title": task["title"],
                "reason": task["reason"],
                "priority": task["priority"],
                "topic": task.get("topic"),
                "estimated_impact": "中",
            })

        dominant = self._state.dominant_drive
        if dominant and dominant != "none":
            drive_action = self._dominant_drive_to_action(dominant)
            if drive_action:
                actions.append(drive_action)

        actions.sort(key=lambda x: -x["priority"])

        seen_titles = set()
        unique_actions = []
        for a in actions:
            if a["title"] not in seen_titles:
                seen_titles.add(a["title"])
                unique_actions.append(a)

        return unique_actions[:max_actions]

    def _dominant_drive_to_action(self, drive: str) -> dict | None:
        """将主导动机转化为行动建议"""
        drive_actions = {
            "curiosity_explore": {
                "action_type": "drive_driven",
                "title": "深入探索当前感兴趣的领域",
                "reason": f"好奇心为主导动机（{self._state.curiosity:.2f}）",
                "priority": 0.7,
                "topic": None,
                "estimated_impact": "高",
            },
            "boredom_break": {
                "action_type": "drive_driven",
                "title": "打破信息茧房，尝试全新领域",
                "reason": f"无聊度为主导动机（{self._state.boredom:.2f}）",
                "priority": 0.7,
                "topic": None,
                "estimated_impact": "高",
            },
            "confidence_build": {
                "action_type": "drive_driven",
                "title": "验证和巩固已有知识",
                "reason": f"自信度不足（{self._state.confidence:.2f}），需要建立信心",
                "priority": 0.6,
                "topic": None,
                "estimated_impact": "中",
            },
            "goal_achieve": {
                "action_type": "drive_driven",
                "title": "推进未完成的任务",
                "reason": f"满足度不足（{self._state.satisfaction:.2f}），需要成就感",
                "priority": 0.6,
                "topic": None,
                "estimated_impact": "中",
            },
            "deadline_urgent": {
                "action_type": "drive_driven",
                "title": "优先处理紧急任务",
                "reason": f"紧迫感较高（{self._state.urgency:.2f}）",
                "priority": 0.9,
                "topic": None,
                "estimated_impact": "高",
            },
            "stuck_escape": {
                "action_type": "drive_driven",
                "title": "改变策略，寻找新突破口",
                "reason": f"学习动量极低（{self._state.momentum:.2f}），可能陷入瓶颈",
                "priority": 0.7,
                "topic": None,
                "estimated_impact": "高",
            },
        }
        return drive_actions.get(drive)

    # ══════════════════════════════════════════════════════
    # v8.3: 动机状态报告
    # ══════════════════════════════════════════════════════

    def get_motivation_report(self) -> dict:
        """
        生成完整的动机状态报告。

        返回: {
            "state": dict,
            "triggers": [dict],
            "proactive_actions": [dict],
            "knowledge_gaps_summary": str,
            "dominant_drive": str,
            "mood": str,
        }
        """
        triggers = self.check_triggers()
        actions = self.generate_proactive_actions()
        gaps = self.detect_knowledge_gaps()

        gap_summary_parts = []
        gap_types = {}
        for g in gaps:
            gt = g["gap_type"]
            gap_types[gt] = gap_types.get(gt, 0) + 1
        for gt, count in gap_types.items():
            gap_summary_parts.append(f"{gt}: {count}")

        return {
            "state": self._state.to_dict(),
            "triggers": triggers,
            "proactive_actions": actions,
            "knowledge_gaps_summary": "；".join(gap_summary_parts) if gap_summary_parts else "无盲区",
            "dominant_drive": self._state.dominant_drive,
            "mood": self._state.mood_summary,
        }
