"""
engines/ingest.py - 统一写入引擎

将以下模块整合为一条完整的写入管道：
  filter → cleaner → dedup → pipeline → store

核心方法 IngestEngine.remember() 按序执行：
  1. Agent 推理前缀剥离（"I think", "In my opinion" 等）
  2. MemoryFilter  — 判断是否值得记忆
  3. ContentCleaner — 清洗内容
  4. MemoryDeduplicator — 去重检查
  5. 主题写入冷却  — 单会话每主题最多 MAX_WRITES_PER_TOPIC 次写入
  6. IngestPipeline — 实际写入存储

返回结构化结果：StoredResult / FilteredResult / DedupResult / CooldownResult
"""

from __future__ import annotations

import re
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..memory_filter import MemoryFilter
from ..content_cleaner import ContentCleaner
from ..dedup import MemoryDeduplicator
from ..pipeline import IngestPipeline
from ..feeding_mode import FeedingMode

logger = logging.getLogger(__name__)


@dataclass
class StoredResult:
    """成功写入"""
    status: str = field(default="stored", init=False)
    memory_id: str = ""
    topics: list = field(default_factory=list)
    importance: str = "medium"
    emotion: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "memory_id": self.memory_id,
            "topics": self.topics,
            "importance": self.importance,
            "emotion": self.emotion,
        }


@dataclass
class FilteredResult:
    """被过滤器拦截"""
    status: str = field(default="filtered", init=False)
    reason: str = ""
    confidence: float = 0.0
    suggested_importance: str = "low"
    suggested_nature: str = "chat"

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "reason": self.reason,
            "confidence": self.confidence,
            "suggested_importance": self.suggested_importance,
            "suggested_nature": self.suggested_nature,
        }


@dataclass
class DedupResult:
    """与已有记忆重复"""
    status: str = field(default="duplicate", init=False)
    duplicate_of: str = ""
    similarity: float = 0.0
    method: str = ""
    action: str = "skip"

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "duplicate_of": self.duplicate_of,
            "similarity": self.similarity,
            "method": self.method,
            "action": self.action,
        }


@dataclass
class CooldownResult:
    """主题写入冷却中"""
    status: str = field(default="cooldown", init=False)
    topic: str = ""
    writes_this_session: int = 0
    max_writes: int = 3

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "topic": self.topic,
            "writes_this_session": self.writes_this_session,
            "max_writes": self.max_writes,
        }


_AGENT_REASONING_PATTERNS = [
    re.compile(
        r'^(I\s+think|I\s+believe|I\s+feel\s+like|In\s+my\s+opinion|'
        r'My\s+thought\s+is|It\s+seems\s+to\s+me\s+that|'
        r'I\s+would\s+say|I\s+guess|I\s+suppose|'
        r'我觉得|我认为|在我看来|个人认为|我想|我估计|我感觉|我猜)[,，:：]?\s*',
        re.IGNORECASE,
    ),
]


def _strip_agent_reasoning(text: str) -> str:
    """剥离 Agent 推理前缀，保留核心陈述。"""
    for pat in _AGENT_REASONING_PATTERNS:
        text = pat.sub('', text)
    return text.strip()


class IngestEngine:
    """
    统一写入引擎：编排 filter → cleaner → dedup → pipeline 全流程。

    用法::

        engine = IngestEngine(pipeline=pipeline, store=store, embedding_store=emb)
        result = engine.remember("决定采用 Chroma 作为向量库", topics=["vector_db"])
        # result.status in ("stored", "filtered", "duplicate", "cooldown")
    """

    MAX_WRITES_PER_TOPIC: int = 3

    MAX_CONTENT_LENGTH: int = 50_000
    MAX_CONTENT_WARN: int = 10_000

    CAUSAL_ANALYSIS_INTERVAL: int = 10  # 每 N 次插入触发一次因果分析，降低 LLM 调用成本

    def __init__(
        self,
        pipeline: IngestPipeline,
        store,
        embedding_store=None,
        llm_fn=None,
        memory_bridge=None,
        causal_chain=None,
        reactor=None,
        memory_filter=None,
        content_cleaner=None,
        deduplicator=None,
        emotion_tracker=None,
        motivation=None,
        quality_gate: str = "auto",
        config: dict = None,
    ):
        self._config = config or {}

        # Apply config overrides
        self.MAX_WRITES_PER_TOPIC = self._config.get("max_writes_per_topic", self.MAX_WRITES_PER_TOPIC)
        self.MAX_CONTENT_LENGTH = self._config.get("max_content_length", self.MAX_CONTENT_LENGTH)
        quality_gate = self._config.get("quality_gate", quality_gate)

        self.pipeline = pipeline
        self.store = store
        self.embedding_store = embedding_store

        self.filter = memory_filter or MemoryFilter(llm_fn=llm_fn)
        self.cleaner = content_cleaner or ContentCleaner()
        self.dedup = deduplicator or MemoryDeduplicator(store=store, embedding_store=embedding_store)
        self.feeding_mode = FeedingMode(memory_bridge) if memory_bridge else None
        self.causal_chain = causal_chain
        self.reactor = reactor
        self.emotion_tracker = emotion_tracker
        self.motivation = motivation
        self._quality_gate = quality_gate

        self._topic_write_counts: dict[str, int] = {}
        self._insert_count: int = 0
        self._lock = threading.Lock()
        self._llm_call_counter: dict[str, int] = {}
        self._llm_call_date: str = datetime.now().strftime("%Y-%m-%d")

    def _check_llm_budget(self) -> bool:
        """Check if LLM budget allows another call."""
        try:
            from agent_memory.config.settings import settings
            limit = settings.get("cost.llm_daily_call_limit", 500)

            today = datetime.now().strftime("%Y-%m-%d")
            if self._llm_call_date != today:
                self._llm_call_counter = {}
                self._llm_call_date = today

            current_count = self._llm_call_counter.get("total", 0)
            if current_count >= limit:
                logger.warning(f"LLM daily call limit reached ({current_count}/{limit})")
                return False
            return True
        except Exception:
            return True

    def __repr__(self):
        return f"IngestEngine(inserts={getattr(self, '_insert_count', 0)})"

    def _assess_quality(self, content: str) -> dict:
        """Assess memory content quality.

        Returns:
            {"score": float, "level": str, "reasons": list[str]}
            score: 0.0-1.0, higher is better
            level: "high" / "medium" / "low" / "trivial"
            reasons: list of quality issues found
        """
        reasons = []
        score = 1.0

        # Check 1: Content length
        stripped = content.strip()
        if len(stripped) < 3:
            return {"score": 0.0, "level": "trivial", "reasons": ["content_too_short"]}
        elif len(stripped) < 10:
            score -= 0.3
            reasons.append("very_short_content")

        # Check 2: Repetitive characters (e.g., "啊啊啊啊啊")
        unique_chars = len(set(stripped))
        if unique_chars < 4 and len(stripped) > 5:
            score -= 0.4
            reasons.append("highly_repetitive")

        # Check 3: Common filler phrases
        filler_phrases = ["嗯", "好的", "哦", "啊", "ok", "yes", "no", "嗯嗯", "哈哈"]
        if stripped.lower() in filler_phrases:
            score -= 0.5
            reasons.append("filler_phrase")

        # Check 4: Information density (unique words / total words)
        words = stripped.split()
        if len(words) > 2:
            unique_words = len(set(w.lower() for w in words))
            density = unique_words / len(words)
            if density < 0.3:
                score -= 0.3
                reasons.append("low_information_density")

        # Check 5: No meaningful verbs or nouns (very basic heuristic)
        has_substance = any(len(w) > 1 for w in words)
        if not has_substance and len(words) <= 3:
            score -= 0.2
            reasons.append("lacks_substance")

        # Clamp score
        score = max(0.0, min(1.0, score))

        # Determine level
        if score >= 0.7:
            level = "high"
        elif score >= 0.4:
            level = "medium"
        elif score >= 0.2:
            level = "low"
        else:
            level = "trivial"

        return {"score": score, "level": level, "reasons": reasons}

    def remember(
        self,
        content: str,
        person_code: str = "main",
        ts: float | None = None,
        topics: list[str] | None = None,
        nature_code: str | None = None,
        tool_codes: list[str] | None = None,
        knowledge_codes: list[str] | None = None,
        importance: str = "medium",
        owner_agent_id: str = "_system",
        visibility: str = "team",
        skip_filter: bool = False,
        skip_dedup: bool = False,
        skip_cooldown: bool = False,
        context: dict | None = None,
        force: bool = False,
        auto_write: bool = True,
    ) -> dict:
        """
        统一写入入口。

        执行流程:
          1. 剥离 Agent 推理前缀
          2. 输入长度校验
          3. auto_write 审核门
          4. MemoryFilter 判断是否值得记忆
          5. ContentCleaner 清洗内容
          6. MemoryDeduplicator 去重检查
          7. 主题写入冷却检查
          8. IngestPipeline.ingest() 写入存储
          9. 情感轨迹记录 + 动机状态更新

        参数与 IngestPipeline.ingest() 基本一致，额外:
            skip_filter:   跳过过滤（投喂模式等场景）
            skip_dedup:    跳过去重
            skip_cooldown: 跳过冷却
            context:       上下文信息（传递给管道）
            force:         跳过过滤强制写入（映射为 skip_filter=True）
            auto_write:    是否直接写入（False 则返回待审核状态）

        返回:
            dict — 包含 status 字段的结果字典
        """
        if not content or not content.strip():
            return FilteredResult(reason="空文本", confidence=1.0).to_dict()

        _remember_start = time.time()
        content_len = len(content)
        if content_len > self.MAX_CONTENT_LENGTH:
            return FilteredResult(
                reason=f"内容过长: {content_len} 字符（上限 {self.MAX_CONTENT_LENGTH}）",
                confidence=1.0,
            ).to_dict()
        if content_len > self.MAX_CONTENT_WARN:
            logger.warning(f"记忆内容较长: {content_len} 字符，建议拆分")

        if not auto_write:
            preview = content[:200] + ("..." if len(content) > 200 else "")
            return {
                "status": "pending_review",
                "memory_id": None,
                "reason": "pending_review",
                "preview": preview,
                "content_length": content_len,
                "message": "记忆待人工审核。设置 auto_write=True 可跳过审核直接写入（仅限受信任环境）。",
            }

        if force:
            skip_filter = True

        content = _strip_agent_reasoning(content)
        if not content:
            return FilteredResult(reason="推理前缀剥离后为空", confidence=1.0).to_dict()

        if not skip_filter:
            filter_result = self.filter.should_remember(content)
            if not filter_result["remember"]:
                return FilteredResult(
                    reason=filter_result["reason"],
                    confidence=filter_result["confidence"],
                    suggested_importance=filter_result["suggested_importance"],
                    suggested_nature=filter_result["suggested_nature"],
                ).to_dict()
            if importance == "medium" and filter_result["suggested_importance"] != "medium":
                importance = filter_result["suggested_importance"]
            if nature_code is None and filter_result.get("suggested_nature"):
                nature_code = filter_result["suggested_nature"]

        # Quality gate: assess content quality before cleaning
        quality = None
        if self._quality_gate != "off" and not skip_filter:
            if not self._check_llm_budget():
                logger.warning("LLM budget exceeded, skipping quality assessment")
            else:
                quality = self._assess_quality(content)
                if quality["level"] == "trivial" and self._quality_gate == "strict":
                    return {
                        "written": False,
                        "status": "filtered",
                        "reason": f"Low quality: {', '.join(quality['reasons'])}",
                        "quality_score": quality["score"],
                        "quality_level": quality["level"],
                    }
                # For "auto" mode, trivial memories get stored as ephemeral
                # The quality info is attached to the result later

        content = self.cleaner.clean(content, importance=importance)
        if not content or not content.strip():
            return FilteredResult(reason="清洗后内容为空", confidence=1.0).to_dict()

        if not skip_dedup:
            dedup_result = self.dedup.check_duplicate(content)
            if dedup_result["is_duplicate"]:
                if dedup_result["action"] == "skip":
                    return DedupResult(
                        duplicate_of=dedup_result["duplicate_of"],
                        similarity=dedup_result["similarity"],
                        method=dedup_result["method"],
                        action=dedup_result["action"],
                    ).to_dict()
                if dedup_result["action"] == "merge":
                    existing = self.store.get_memory(dedup_result["duplicate_of"])
                    if existing:
                        merged_content = existing.get("content", "") + "\n" + content
                        self.store.update_memory(
                            dedup_result["duplicate_of"],
                            merged_content,
                            change_reason="dedup_merge",
                        )
                        return DedupResult(
                            duplicate_of=dedup_result["duplicate_of"],
                            similarity=dedup_result["similarity"],
                            method=dedup_result["method"],
                            action="merged",
                        ).to_dict()

        if not skip_cooldown and topics:
            primary_topic = topics[0]
            with self._lock:
                count = self._topic_write_counts.get(primary_topic, 0)
                if count >= self.MAX_WRITES_PER_TOPIC:
                    return CooldownResult(
                        topic=primary_topic,
                        writes_this_session=count,
                        max_writes=self.MAX_WRITES_PER_TOPIC,
                    ).to_dict()

        ingest_kwargs = dict(
            content=content,
            person_code=person_code,
            ts=ts,
            topics=topics,
            nature_code=nature_code,
            tool_codes=tool_codes,
            knowledge_codes=knowledge_codes,
            importance=importance,
            owner_agent_id=owner_agent_id,
            visibility=visibility,
        )
        if context:
            ingest_kwargs["context"] = context

        ingest_result = self.pipeline.ingest(**ingest_kwargs)

        if ingest_result.get("memory_id") is None:
            reason = ingest_result.get("reason") or ingest_result.get("throttled") and "throttled" or "unknown"
            return FilteredResult(reason=f"pipeline 跳过: {reason}", confidence=0.5).to_dict()

        if not skip_cooldown and topics:
            primary_topic = topics[0]
            with self._lock:
                self._topic_write_counts[primary_topic] = (
                    self._topic_write_counts.get(primary_topic, 0) + 1
                )

        result = StoredResult(
            memory_id=ingest_result["memory_id"],
            topics=ingest_result.get("topics", []),
            importance=ingest_result.get("importance", importance),
            emotion=ingest_result.get("emotion"),
        )
        result_dict = result.to_dict()
        result_dict["written"] = True
        result_dict["reason"] = "ok"

        # Attach quality info if assessed
        if quality is not None:
            result_dict["quality_score"] = quality["score"]
            result_dict["quality_level"] = quality["level"]
            if quality["reasons"]:
                result_dict["quality_issues"] = quality["reasons"]
            # For "auto" mode, downgrade trivial memories to ephemeral importance
            if quality["level"] == "trivial" and self._quality_gate == "auto":
                result_dict["importance"] = "ephemeral"
                result_dict["reason"] = "ok (downgraded to ephemeral by quality gate)"

        self._insert_count += 1
        if self.causal_chain and self._insert_count % self.CAUSAL_ANALYSIS_INTERVAL == 0:
            try:
                self.causal_chain.full_causal_analysis(window_hours=6, embedding_store=self.embedding_store)
            except Exception as e:
                logger.warning("因果分析失败: %s", e)

        if self.reactor:
            try:
                mem_dict = self.store.get_memory(result.memory_id) or {}
                self.reactor.fire_write(mem_dict, self.store)
            except Exception as e:
                logger.exception("反应器触发失败: %s", e)

        if self.emotion_tracker:
            try:
                emotion_data = result_dict.get("emotion") or {}
                if emotion_data:
                    self.emotion_tracker.record(emotion_data, agent_id=getattr(self.store, 'agent_id', None) or owner_agent_id or "_system")
            except Exception as e:
                logger.exception("情感轨迹记录失败: %s", e)

        if self.motivation:
            try:
                memory_for_state = {
                    "content": content,
                    "importance": result_dict.get("importance", importance),
                    "topics": result_dict.get("topics", []),
                    "significance": (result_dict.get("emotion") or {}).get("significance", "notable"),
                }
                self.motivation.update_state([memory_for_state])
            except Exception as e:
                logger.exception("动机状态更新失败: %s", e)

        _remember_elapsed = time.time() - _remember_start
        logger.info("remember_completed", extra={
            "event": "remember_completed",
            "memory_id": result_dict.get("memory_id", ""),
            "content_length": content_len,
            "filter_result": result_dict.get("status", "unknown"),
            "duration_ms": int(_remember_elapsed * 1000),
        })

        return result_dict

    def batch_remember(
        self,
        items: list[dict],
        skip_filter: bool = False,
    ) -> list[dict]:
        """Remember multiple items at once."""
        if not items:
            return []

        results = []

        for item in items:
            content = item.get("content", "")
            if not content or len(content) > self.MAX_CONTENT_LENGTH:
                results.append({"status": "rejected", "reason": "invalid_content", "written": False})
                continue

            try:
                result = self.remember(
                    content=content,
                    topics=item.get("topics", []),
                    importance=item.get("importance", "medium"),
                    nature_code=item.get("nature_code"),
                    tool_codes=item.get("tool_codes"),
                    knowledge_codes=item.get("knowledge_codes"),
                    owner_agent_id=item.get("owner_agent_id", "_system"),
                    visibility=item.get("visibility", "team"),
                    skip_filter=True,
                    skip_dedup=True,
                )
                if isinstance(result, dict):
                    mid = result.get("memory_id", "")
                    results.append({"status": result.get("status", "stored" if mid else "error"), "memory_id": mid, "written": result.get("written", bool(mid))})
                else:
                    mid = getattr(result, "memory_id", "")
                    results.append({"status": "stored" if mid else "error", "memory_id": mid, "written": bool(mid)})
            except Exception as e:
                results.append({"status": "error", "reason": str(e), "written": False})

        stored_ids = [r.get("memory_id") for r in results if r.get("written")]
        if stored_ids and self.causal_chain:
            try:
                self.causal_chain.full_causal_analysis()
            except Exception as e:
                logger.debug("batch_remember causal_analysis: %s", e)

        return results

    def reset_cooldown(self, topic: str | None = None) -> None:
        """
        重置写入冷却计数。

        参数:
            topic: 指定主题，None 则重置全部
        """
        with self._lock:
            if topic is None:
                self._topic_write_counts.clear()
            else:
                self._topic_write_counts.pop(topic, None)

    def get_cooldown_status(self) -> dict[str, int]:
        """返回各主题的当前写入计数。"""
        with self._lock:
            return dict(self._topic_write_counts)

    def get_stats(self) -> dict:
        """Return ingestion statistics."""
        dedup_stats = self.dedup.get_stats()
        queue_stats = self.pipeline.get_queue_stats()
        return {
            "dedup": dedup_stats,
            "queue": queue_stats,
            "cooldown": self.get_cooldown_status(),
            "max_writes_per_topic": self.MAX_WRITES_PER_TOPIC,
        }


__all__ = [
    "IngestEngine",
    "StoredResult",
    "FilteredResult",
    "DedupResult",
    "CooldownResult",
    "MemoryFilter",
    "ContentCleaner",
    "MemoryDeduplicator",
    "IngestPipeline",
    "FeedingMode",
]
