#!/usr/bin/env python3
"""
发送者信息缓存管理器
用于避免频繁调用 get_sender() 导致的 Flood Wait
"""

import asyncio
import logging
from typing import Optional, Dict, Tuple
from telethon import TelegramClient
from telethon.errors import FloodWaitError

logger = logging.getLogger(__name__)


class SenderCache:
    """发送者信息缓存，减少 API 调用"""
    
    def __init__(self, client: TelegramClient, max_cache_size: int = 10000):
        self.client = client
        self._cache: Dict[int, Tuple[Optional[str], Optional[str]]] = {}
        self._pending: set = set()  # 待获取的 sender_id
        self._max_size = max_cache_size
        self._lock = asyncio.Lock()
        
    def get(self, sender_id: Optional[int]) -> Tuple[Optional[str], Optional[str]]:
        """
        从缓存获取发送者信息
        返回: (sender_username, sender_name)
        """
        if not sender_id:
            return None, None
            
        # 内存缓存命中
        if sender_id in self._cache:
            return self._cache[sender_id]
            
        # 标记为待获取
        self._pending.add(sender_id)
        return None, None
        
    async def fetch_pending(self, batch_size: int = 50, delay: float = 2.0):
        """
        批量获取待处理的发送者信息
        分批处理，每批之间延迟，避免 Flood Wait
        """
        if not self._pending:
            return
            
        async with self._lock:
            pending_list = list(self._pending)[:batch_size]
            self._pending = self._pending - set(pending_list)
            
        for sender_id in pending_list:
            try:
                # 再次检查缓存（可能其他任务已获取）
                if sender_id in self._cache:
                    continue
                    
                sender = await self.client.get_entity(sender_id)
                if sender:
                    username = getattr(sender, 'username', None)
                    name = (
                        getattr(sender, 'first_name', '')
                        + (' ' + getattr(sender, 'last_name', '') if getattr(sender, 'last_name', None) else '')
                    ).strip() or None
                    
                    self._cache[sender_id] = (username, name)
                    logger.debug(f"获取发送者信息: {sender_id} -> @{username}")
                    
                    # 每个请求后短暂延迟
                    await asyncio.sleep(0.5)
                    
            except FloodWaitError as e:
                logger.warning(f"获取发送者 {sender_id} Flood Wait {e.seconds}s, 重新入队")
                # 重新入队，等待后再试
                self._pending.add(sender_id)
                await asyncio.sleep(e.seconds + 2)
            except Exception as e:
                logger.debug(f"获取发送者 {sender_id} 失败: {e}")
                self._cache[sender_id] = (None, None)
                
        # 批次间延迟
        if self._pending:
            await asyncio.sleep(delay)
            
    async def fetch_all_pending(self, batch_size: int = 50, batch_delay: float = 3.0):
        """获取所有待处理的发送者信息"""
        while self._pending:
            await self.fetch_pending(batch_size, batch_delay)
            
    def get_cache_stats(self) -> Dict:
        """获取缓存统计"""
        return {
            'cached': len(self._cache),
            'pending': len(self._pending),
            'hit_rate': self._calculate_hit_rate()
        }
        
    def _calculate_hit_rate(self) -> float:
        """计算缓存命中率（简化版）"""
        total = len(self._cache) + len(self._pending)
        if total == 0:
            return 0.0
        return len(self._cache) / total
        
    def pending_count(self) -> int:
        """返回待获取数量"""
        return len(self._pending)

    def has_pending(self) -> bool:
        """是否有待获取的发送者"""
        return len(self._pending) > 0

    def mark_pending(self, sender_id: int):
        """标记为待获取"""
        if sender_id and sender_id not in self._cache:
            self._pending.add(sender_id)

    def get_all_cached(self) -> Dict[int, Tuple[Optional[str], Optional[str]]]:
        """返回所有已缓存的发送者信息（浅拷贝）"""
        return dict(self._cache)

    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self._pending.clear()
