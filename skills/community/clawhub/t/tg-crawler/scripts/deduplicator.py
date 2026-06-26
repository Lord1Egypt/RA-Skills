"""
去重模块 - Bloom Filter 快速去重 + 数据库精确去重
"""
import logging
import time
from collections import OrderedDict

logger = logging.getLogger(__name__)


class Deduplicator:
    """
    两级去重：
    1. 内存 LRU 缓存（快速过滤最近 N 条）
    2. 数据库唯一键约束（精确去重）
    """

    def __init__(self, cache_size: int = 10000):
        self._cache: OrderedDict[str, float] = OrderedDict()
        self.cache_size = cache_size
        self._hit_count = 0
        self._total_count = 0

    def _make_key(self, chat_id: int, msg_id: int) -> str:
        return f"{chat_id}:{msg_id}"

    def exists(self, chat_id: int, msg_id: int) -> bool:
        """
        检查消息是否已处理（内存缓存层）

        Returns:
            True 表示已存在，应跳过
        """
        self._total_count += 1
        key = self._make_key(chat_id, msg_id)

        if key in self._cache:
            # 命中 → 移到末尾（LRU）
            self._cache.move_to_end(key)
            self._hit_count += 1
            return True

        # 未命中 → 加入缓存
        self._cache[key] = time.time()
        if len(self._cache) > self.cache_size:
            self._cache.popitem(last=False)  # 淘汰最旧的

        return False

    def add(self, chat_id: int, msg_id: int):
        """手动将消息标记为已处理"""
        key = self._make_key(chat_id, msg_id)
        self._cache[key] = time.time()
        if len(self._cache) > self.cache_size:
            self._cache.popitem(last=False)

    def stats(self) -> dict:
        """返回去重统计"""
        return {
            "cache_size": len(self._cache),
            "total_checked": self._total_count,
            "cache_hits": self._hit_count,
            "hit_rate": f"{self._hit_count / max(self._total_count, 1) * 100:.1f}%",
        }
