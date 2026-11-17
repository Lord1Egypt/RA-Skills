"""
幂等性保证模块 — 防止重复执行产生叠加副作用。

问题：如果相同输入重复执行 Triangulate 工作流，会产生：
- 重复的 sessions_spawn（消耗 tokens）
- 重复的副作用调用
- 不一致的状态

解决：
- 基于 input_hash 的幂等性缓存
- 可选的 TTL 过期策略
- 写入前检查（Check-Before-Write）
"""
from __future__ import annotations

import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from schemas import FinalReport, UserInput


# ============================================================================
# 幂等性缓存
# ============================================================================

@dataclass
class CacheEntry:
    """缓存条目"""
    input_hash: str
    result: FinalReport
    created_at: float = field(default_factory=time.time)
    ttl_seconds: float = 3600  # 默认 1 小时过期


class IdempotencyGuard:
    """
    幂等性守卫 — 确保相同输入产生一致结果，不重复执行副作用。

    用法:
        guard = IdempotencyGuard(ttl_seconds=1800)
        result = guard.execute_or_cache(
            user_input,
            executor_fn=lambda: orchestrator.run(user_input),
        )
    """

    def __init__(self, ttl_seconds: float = 3600, max_entries: int = 100):
        """
        Args:
            ttl_seconds: 缓存过期时间（秒）
            max_entries: 最大缓存条目数
        """
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self._cache: Dict[str, CacheEntry] = {}
        self._hit_count: int = 0
        self._miss_count: int = 0
        self._lock = threading.RLock()

    # ------------------------------------------------------------------
    # 公共接口
    # ------------------------------------------------------------------

    def execute_or_cache(
        self,
        user_input: UserInput,
        executor_fn: callable,
        force_refresh: bool = False,
    ) -> Tuple[FinalReport, bool]:
        """
        幂等执行：如果缓存命中则返回缓存结果，否则执行并缓存。

        Args:
            user_input: 标准化用户输入
            executor_fn: 实际执行函数
            force_refresh: True=跳过缓存，强制执行

        Returns:
            (FinalReport, is_cache_hit): 结果和是否命中缓存
        """
        input_hash = self._compute_hash(user_input)

        # 检查缓存
        if not force_refresh:
            cached = self._get(input_hash)
            if cached is not None:
                self._hit_count += 1
                return cached, True

        # 执行
        self._miss_count += 1
        result = executor_fn()

        # 缓存
        self._set(input_hash, result)

        return result, False

    def check_cache(self, user_input: UserInput) -> Tuple[Optional[FinalReport], bool]:
        """检查缓存并返回结果（线程安全）。

        Returns:
            (cached_result, is_hit): 缓存结果和是否命中
        """
        input_hash = self._compute_hash(user_input)
        with self._lock:
            entry = self._cache.get(input_hash)
            if entry is not None:
                if time.time() - entry.created_at <= entry.ttl_seconds:
                    self._hit_count += 1
                    return entry.result, True
                else:
                    del self._cache[input_hash]
        self._miss_count += 1
        return None, False

    def is_duplicate(self, user_input: UserInput) -> bool:
        """检查是否为重复请求（已缓存且未过期）"""
        _, is_hit = self.check_cache(user_input)
        return is_hit

    def invalidate(self, user_input: UserInput) -> bool:
        """使指定输入的缓存失效（线程安全）"""
        input_hash = self._compute_hash(user_input)
        with self._lock:
            if input_hash in self._cache:
                del self._cache[input_hash]
                return True
        return False

    def cache_result(self, user_input: UserInput, result: FinalReport) -> None:
        """将结果写入缓存（线程安全）。"""
        input_hash = self._compute_hash(user_input)
        self._set(input_hash, result)

    def clear(self):
        """清空所有缓存（线程安全）"""
        with self._lock:
            self._cache.clear()

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    def _compute_hash(self, user_input: UserInput) -> str:
        """计算输入哈希（覆盖 UserInput 的全部 7 个字段）。"""
        # 构建确定性字符串 — 覆盖全部字段
        canonical = json.dumps({
            "task_description": user_input.task_description,
            "importance": user_input.importance,
            "keywords": sorted(user_input.keywords),
            "preferred_templates": sorted(user_input.preferred_templates),
            "require_execution_layer": user_input.require_execution_layer,
            "require_management_layer": user_input.require_management_layer,
            "max_total_timeout_seconds": user_input.max_total_timeout_seconds,
        }, sort_keys=True, ensure_ascii=True)

        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _get(self, input_hash: str) -> Optional[FinalReport]:
        """从缓存获取（线程安全）"""
        with self._lock:
            entry = self._cache.get(input_hash)
            if entry is None:
                return None

            # 检查 TTL
            if time.time() - entry.created_at > entry.ttl_seconds:
                del self._cache[input_hash]
                return None

            return entry.result

    def _set(self, input_hash: str, result: FinalReport):
        """写入缓存（线程安全）"""
        with self._lock:
            # LRU 淘汰
            if len(self._cache) >= self.max_entries:
                oldest_key = min(
                    self._cache.keys(),
                    key=lambda k: self._cache[k].created_at,
                )
                del self._cache[oldest_key]

            self._cache[input_hash] = CacheEntry(
                input_hash=input_hash,
                result=result,
                ttl_seconds=self.ttl_seconds,
            )

    # ------------------------------------------------------------------
    # 统计
    # ------------------------------------------------------------------

    @property
    def hit_rate(self) -> float:
        total = self._hit_count + self._miss_count
        if total == 0:
            return 0.0
        return self._hit_count / total

    def get_stats(self) -> Dict[str, Any]:
        return {
            "cache_size": len(self._cache),
            "hit_count": self._hit_count,
            "miss_count": self._miss_count,
            "hit_rate": f"{self.hit_rate:.1%}",
            "ttl_seconds": self.ttl_seconds,
        }
