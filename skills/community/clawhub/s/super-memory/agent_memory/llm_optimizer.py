"""v8.9 — llm_optimizer.py — LLM Token 消耗优化策略

解决 TECHNICAL_ANALYSIS.md §6.4 中标记的问题:
    "LLM 蒸馏成本 | 🟡 中 | 大量记忆蒸馏需要多次 LLM 调用"

策略层次:
    1. Token Cache        — SHA256 内容键 → LLM 结果缓存，避免相同/相似内容重复调用
    2. Batch Gating       — 阈值控制：同类记忆 < threshold → 纯规则合成，不调用 LLM
    3. Content Truncation — 输入截断：内容超过 max_input_tokens → 优先保留首尾关键句
    4. Cached Embedding   — 蒸馏管道中 embedding 结果缓存（encode 一次，多处复用）
    5. Progressive Summarization — 金字塔式渐进摘要：先 5 条一组，再组合组摘要

与 distill.py 的关系:
    distill.py 是蒸馏管道，llm_optimizer.py 是其前置优化层
"""

from __future__ import annotations

import time
import json
import hashlib
import logging
import threading
from collections import OrderedDict
from typing import Optional, Callable

logger = logging.getLogger(__name__)

DEFAULT_MAX_INPUT_TOKENS = 2000
DEFAULT_CACHE_SIZE = 500
DEFAULT_CACHE_TTL_SECONDS = 3600
DEFAULT_BATCH_GATING_THRESHOLD = 3
CHINESE_CHAR_TO_TOKEN_RATIO = 1.5


class LLMOptimizer:
    """LLM 调用优化器 — 缓存 + 批控 + 截断 + 渐进摘要"""

    def __init__(self, cache_size: int = None, max_input_tokens: int = None):
        self._max_input_tokens = max_input_tokens or DEFAULT_MAX_INPUT_TOKENS
        self._max_cache_size = cache_size or DEFAULT_CACHE_SIZE
        self._cache: OrderedDict = OrderedDict()
        self._cache_lock = threading.Lock()
        self._stats = {
            "total_calls": 0, "cache_hits": 0, "batch_skipped": 0,
            "tokens_saved": 0, "truncations": 0,
        }

    def estimate_tokens(self, text: str) -> int:
        return max(1, int(len(text) / CHINESE_CHAR_TO_TOKEN_RATIO))

    def should_call_llm(self, item_count: int, average_similarity: float = 0) -> bool:
        """批控判断: 是否需要调用 LLM

        规则:
        - item_count < DEFAULT_BATCH_GATING_THRESHOLD → 跳过 LLM (纯规则合成)
        - item_count >= 阈值但平均相似度 < 0.5 → 跳过 (差异太大不做融合)
        - 其余 → 调用 LLM
        """
        if item_count < DEFAULT_BATCH_GATING_THRESHOLD:
            self._stats["batch_skipped"] += 1
            return False
        if average_similarity > 0 and average_similarity < 0.5:
            self._stats["batch_skipped"] += 1
            logger.debug(f"批控跳过: count={item_count}, avg_sim={average_similarity:.2f}")
            return False
        return True

    def cache_key(self, content: str, context: str = "") -> str:
        return hashlib.sha256(f"{content}|{context}".encode()).hexdigest()

    def get_cached(self, key: str) -> Optional[str]:
        with self._cache_lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() - entry["ts"] < DEFAULT_CACHE_TTL_SECONDS:
                    self._cache.move_to_end(key)
                    self._stats["cache_hits"] += 1
                    return entry["result"]
                del self._cache[key]
        return None

    def set_cache(self, key: str, result: str, tokens_saved: int = 0):
        with self._cache_lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = {"result": result, "ts": time.time()}
            if len(self._cache) > self._max_cache_size:
                self._cache.popitem(last=False)
            self._stats["tokens_saved"] += tokens_saved

    def call_with_cache(self, prompt: str, llm_fn: Callable,
                         context: str = "") -> str:
        key = self.cache_key(prompt, context)
        cached = self.get_cached(key)
        if cached is not None:
            return cached

        self._stats["total_calls"] += 1
        result = llm_fn(prompt)
        estimated_tokens = self.estimate_tokens(prompt)
        self.set_cache(key, result, estimated_tokens)
        return result

    def progressive_summarize(self, items: list[str],
                               llm_fn: Callable,
                               max_items_per_call: int = 5) -> str:
        """金字塔渐进摘要: 每 max_items_per_call 组摘要 → 再次摘要"""
        if not items:
            return ""

        if len(items) <= max_items_per_call:
            prompt = "将以下内容合并为一条简洁摘要:\n" + "\n".join(items)
            return self.call_with_cache(prompt, llm_fn)

        groups = []
        for i in range(0, len(items), max_items_per_call):
            group = items[i:i + max_items_per_call]
            prompt = "将以下内容合并为一条简洁摘要:\n" + "\n".join(group)
            summary = self.call_with_cache(prompt, llm_fn, f"round1_g{i}")
            groups.append(summary)

        if len(groups) == 1:
            return groups[0]

        return self.progressive_summarize(groups, llm_fn, max_items_per_call)

    def truncate_content(self, content: str, max_tokens: int = None) -> str:
        max_tokens = max_tokens or self._max_input_tokens
        current_tokens = self.estimate_tokens(content)
        if current_tokens <= max_tokens:
            return content

        self._stats["truncations"] += 1
        head_chars = max_tokens // 2
        tail_chars = max_tokens // 4
        head = content[:head_chars]
        tail = content[-tail_chars:] if len(content) > head_chars + tail_chars else ""
        return f"{head}\n...[截断]...\n{tail}"

    def smart_truncate(self, content: str, max_tokens: int = None) -> str:
        """智能截断: 保留首段 + 末段 + 中间关键句"""
        max_tokens = max_tokens or self._max_input_tokens
        current_tokens = self.estimate_tokens(content)
        if current_tokens <= max_tokens:
            return content

        self._stats["truncations"] += 1
        sentences = content.replace("。", "。\n").replace(".", ".\n").split("\n")
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 3:
            return content[:max_tokens * 2]

        first = sentences[0]
        last = sentences[-1]
        middle = []
        mid_tokens = 0
        mid_budget = max_tokens - self.estimate_tokens(first) - self.estimate_tokens(last)

        for s in sentences[1:-1]:
            t = self.estimate_tokens(s)
            if mid_tokens + t > mid_budget:
                break
            middle.append(s)
            mid_tokens += t

        return first + "\n" + "\n".join(middle) + "\n" + last

    def cached_embed(self, content: str, embed_fn: Callable) -> list[float]:
        key = hashlib.sha256(content.encode()).hexdigest()
        cached = self.get_cached(key)
        if cached is not None:
            try:
                return json.loads(cached)
            except json.JSONDecodeError:
                pass

        self._stats["total_calls"] += 1
        vec = embed_fn(content)
        result = vec.tolist() if hasattr(vec, 'tolist') else list(vec)
        self.set_cache(key, json.dumps(result), 0)
        return result

    def batch_embed(self, contents: list[str], embed_fn: Callable) -> list[list[float]]:
        uncached = []
        uncached_indices = []
        results = [None] * len(contents)

        for i, content in enumerate(contents):
            key = hashlib.sha256(content.encode()).hexdigest()
            cached = self.get_cached(key)
            if cached is not None:
                try:
                    results[i] = json.loads(cached)
                except json.JSONDecodeError:
                    uncached.append(content)
                    uncached_indices.append(i)
            else:
                uncached.append(content)
                uncached_indices.append(i)

        if uncached:
            self._stats["total_calls"] += len(uncached)
            try:
                vecs = embed_fn(uncached)
                for j, vec in enumerate(vecs):
                    idx = uncached_indices[j]
                    result = vec.tolist() if hasattr(vec, 'tolist') else list(vec)
                    results[idx] = result
                    key = hashlib.sha256(uncached[j].encode()).hexdigest()
                    self.set_cache(key, json.dumps(result), 0)
            except Exception as e:
                logger.warning("llm_optimizer: %s", e)
                for content, idx in zip(uncached, uncached_indices):
                    results[idx] = self.cached_embed(content, embed_fn)

        return results

    def get_stats(self) -> dict:
        total = self._stats["total_calls"]
        hits = self._stats["cache_hits"]
        return {
            **self._stats,
            "cache_hit_rate": f"{hits / max(total, 1) * 100:.1f}%",
            "total_llm_calls": total,
            "tokens_saved_estimated": self._stats["tokens_saved"],
        }

    def clear_cache(self):
        with self._cache_lock:
            self._cache.clear()

    def resize_cache(self, new_size: int):
        self._max_cache_size = new_size
        with self._cache_lock:
            while len(self._cache) > self._max_cache_size:
                self._cache.popitem(last=False)