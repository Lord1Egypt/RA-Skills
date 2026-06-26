"""
trace_logger.py - 结构化追踪日志
提供 JSON Lines 格式的追踪日志，支持 recall RRF 分数、maintain 阶段耗时、反思修正追踪
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class TraceLogger:
    """
    结构化追踪日志器。

    功能：
    - JSON Lines 格式写入日志文件
    - 模块级追踪开关（运行时动态控制）
    - recall RRF 分数追踪
    - maintain 阶段耗时追踪
    - meta_recall 反思修正追踪
    - recall 原始分数记录（结构化 + 语义两路）
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_dir: str = None, enabled: bool = False):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self._project_dir = Path(log_dir) if log_dir else Path(__file__).parent
        self._log_dir = self._project_dir / "logs"
        self._log_dir.mkdir(exist_ok=True)

        self._trace_file = self._log_dir / "traces.jsonl"
        self._enabled = enabled
        self._module_filters: set[str] = set()
        self._trace_id_counter = 0
        self._id_lock = threading.Lock()
        self._initialized = True

    def enable(self, enabled: bool = True):
        """全局开关"""
        self._enabled = enabled

    def set_module_filter(self, *modules: str):
        """设置模块过滤器，只记录指定模块的日志"""
        self._module_filters = set(modules)

    def clear_module_filter(self):
        """清除模块过滤器"""
        self._module_filters.clear()

    def _next_id(self) -> int:
        with self._id_lock:
            self._trace_id_counter += 1
            return self._trace_id_counter

    def log(
        self,
        module: str,
        operation: str,
        trace: dict = None,
        trace_id: int = None,
        parent_id: int = None,
        **extra,
    ):
        """
        写入一条追踪日志。

        参数：
            module: 模块名（emotion/motivation/narrative/recall/metacognition/maintain）
            operation: 操作名（如 emotion_analyze/rrf_fusion/reflection_correction）
            trace: 追踪数据 dict
            trace_id: 追踪 ID（用于关联父子操作）
            parent_id: 父追踪 ID
            **extra: 其他字段
        """
        if not self._enabled:
            return

        if self._module_filters and module not in self._module_filters:
            return

        record = {
            "trace_id": trace_id or self._next_id(),
            "parent_id": parent_id,
            "timestamp": datetime.now().isoformat(timespec="milliseconds"),
            "timestamp_ts": time.time(),
            "module": module,
            "operation": operation,
        }
        if trace:
            record["trace"] = trace
        record.update(extra)

        try:
            with open(self._trace_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.warning("trace_logger: %s", e)

    @contextmanager
    def span(
        self,
        module: str,
        operation: str,
        trace_id: int = None,
        parent_id: int = None,
        **extra,
    ):
        """
        上下文管理器，自动记录耗时。

        用法：
            with tracer.span("maintain", "causal_analysis") as tid:
                # do work
                tracer.log(tid, "causal_analysis", result={...})
        """
        tid = trace_id or self._next_id()
        start = time.perf_counter()
        start_ts = datetime.now().isoformat(timespec="milliseconds")

        self.log(
            module=module,
            operation=f"{operation}.start",
            trace_id=tid,
            parent_id=parent_id,
            start_ts=start_ts,
            **extra,
        )

        try:
            yield tid
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.log(
                module=module,
                operation=f"{operation}.end",
                trace_id=tid,
                parent_id=parent_id,
                elapsed_ms=round(elapsed_ms, 2),
                **extra,
            )

    def log_recall_rrf(
        self,
        trace_id: int = None,
        query: str = None,
        mode: str = None,
        structured_raw: list[dict] = None,
        semantic_raw: list[dict] = None,
        merged: list[dict] = None,
        final_ranked: list[dict] = None,
        intent: str = None,
        confidence: float = None,
        **extra,
    ):
        """
        记录 recall 检索的 RRF 融合追踪数据。

        参数：
            structured_raw: 结构化检索的原始结果列表（包含原始分数）
            semantic_raw: 语义检索的原始结果列表（包含原始相似度分数）
            merged: RRF 融合后的列表（包含 _rrf_score/_structured_rrf/_semantic_rrf/_dual_hit）
            final_ranked: 综合打分排序后的列表（包含 _rank_score 及各维度分数）
        """
        if not self._enabled:
            return

        record = {
            "trace_id": trace_id or self._next_id(),
            "timestamp": datetime.now().isoformat(timespec="milliseconds"),
            "module": "recall",
            "operation": "rrf_fusion",
            "query": query,
            "mode": mode,
            "intent": intent,
            "confidence": confidence,
        }

        if structured_raw is not None:
            record["structured_count"] = len(structured_raw)
            record["structured_top5"] = [
                {
                    "memory_id": m.get("memory_id"),
                    "score": m.get("_rank_score") if "_rank_score" in m else None,
                }
                for m in structured_raw[:5]
            ]

        if semantic_raw is not None:
            record["semantic_count"] = len(semantic_raw)
            record["semantic_top5"] = [
                {
                    "memory_id": m.get("memory_id"),
                    "score": m.get("_semantic_score") if "_semantic_score" in m else None,
                }
                for m in semantic_raw[:5]
            ]

        if merged is not None:
            record["merged_count"] = len(merged)
            record["dual_hit_count"] = sum(1 for m in merged if m.get("_dual_hit"))
            record["merged_top5"] = [
                {
                    "memory_id": m.get("memory_id"),
                    "rrf_score": m.get("_rrf_score"),
                    "structured_rrf": m.get("_structured_rrf"),
                    "semantic_rrf": m.get("_semantic_rrf"),
                    "dual_hit": m.get("_dual_hit"),
                }
                for m in merged[:5]
            ]

        if final_ranked is not None:
            record["final_top5"] = [
                {
                    "memory_id": m.get("memory_id"),
                    "rank_score": m.get("_rank_score"),
                    "breakdown": m.get("_rank_breakdown"),
                }
                for m in final_ranked[:5]
            ]

        record.update(extra)

        try:
            with open(self._trace_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.warning("trace_logger: %s", e)

    def log_maintain_stage(
        self,
        stage: str,
        elapsed_ms: float,
        stats: dict = None,
        trace_id: int = None,
        **extra,
    ):
        """记录 maintain() 各阶段耗时"""
        if not self._enabled:
            return

        self.log(
            module="maintain",
            operation=f"stage.{stage}",
            trace_id=trace_id,
            elapsed_ms=round(elapsed_ms, 2),
            stats=stats,
            **extra,
        )

    def log_meta_recall_reflection(
        self,
        round_num: int,
        original_query: str,
        refined_query: str = None,
        strategy: str = None,
        before_results: list = None,
        after_results: list = None,
        confidence_before: float = None,
        confidence_after: float = None,
        trace_id: int = None,
        **extra,
    ):
        """
        记录 meta_recall 反思修正过程。

        参数：
            round_num: 第几轮反思（1 或 2）
            original_query: 原始查询
            refined_query: 修正后的查询
            strategy: 使用的修正策略
            before_results: 修正前的检索结果
            after_results: 修正后的检索结果
            confidence_before: 修正前的置信度
            confidence_after: 修正后的置信度
        """
        if not self._enabled:
            return

        record = {
            "trace_id": trace_id or self._next_id(),
            "timestamp": datetime.now().isoformat(timespec="milliseconds"),
            "module": "metacognition",
            "operation": "reflection_correction",
            "round": round_num,
            "original_query": original_query,
            "refined_query": refined_query,
            "strategy": strategy,
            "confidence_before": confidence_before,
            "confidence_after": confidence_after,
            "improvement": (
                round(confidence_after - confidence_before, 3)
                if confidence_before is not None and confidence_after is not None
                else None
            ),
            "before_result_count": len(before_results) if before_results else 0,
            "after_result_count": len(after_results) if after_results else 0,
            **extra,
        }

        try:
            with open(self._trace_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.warning("trace_logger: %s", e)

    def get_recent_traces(self, module: str = None, limit: int = 50) -> list[dict]:
        """读取最近的追踪日志"""
        if not self._trace_file.exists():
            return []

        traces = []
        try:
            with open(self._trace_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in reversed(lines):
                if len(traces) >= limit:
                    break
                try:
                    record = json.loads(line.strip())
                    if module is None or record.get("module") == module:
                        traces.append(record)
                except Exception:
                    continue
        except Exception as e:
            logger.warning("trace_logger: %s", e)

        return list(reversed(traces))

    def clear_logs(self):
        """清空日志文件"""
        try:
            if self._trace_file.exists():
                self._trace_file.unlink()
            logger.info("追踪日志已清空")
        except Exception as e:
            logger.warning("trace_logger: %s", e)


_tracer: TraceLogger = None


def get_tracer() -> TraceLogger:
    """获取全局 tracer 实例"""
    global _tracer
    if _tracer is None:
        _tracer = TraceLogger()
    return _tracer


def enable_tracing(enabled: bool = True):
    """全局启用/禁用追踪"""
    get_tracer().enable(enabled)


def set_trace_module(*modules: str):
    """设置要追踪的模块"""
    get_tracer().set_module_filter(*modules)
