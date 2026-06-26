"""
轻量级Pub/Sub实现，支持Redis和内存队列
"""
import json
import asyncio
import threading
from typing import Any, Callable, Dict, List, Optional, Union
import redis.asyncio as redis
from dataclasses import dataclass, field
from enum import Enum


class PubSubBackend(Enum):
    """Pub/Sub后端类型"""
    MEMORY = "memory"
    REDIS = "redis"


@dataclass
class Message:
    """消息对象"""
    channel: str
    data: Dict[str, Any]
    timestamp: float = field(default_factory=lambda: asyncio.get_event_loop().time())
    message_id: str = field(default_factory=lambda: f"msg_{id(object())}")


class PubSubCoordinator:
    """Pub/Sub协调器"""
    
    def __init__(self, backend: PubSubBackend = PubSubBackend.MEMORY, 
                 redis_url: Optional[str] = None):
        """
        初始化Pub/Sub协调器
        
        Args:
            backend: 后端类型，memory或redis
            redis_url: Redis连接URL，当backend=redis时必填
        """
        self.backend = backend
        self.redis_url = redis_url
        self.redis_client = None
        self.redis_pubsub = None
        
        # 内存后端数据结构
        self._channels: Dict[str, List[Callable]] = {}
        self._message_queue: Dict[str, List[Message]] = {}
        self._lock = threading.RLock()
        
        # 初始化Redis连接
        if backend == PubSubBackend.REDIS:
            if not redis_url:
                raise ValueError("Redis URL is required when using Redis backend")
            self._init_redis()
    
    def _init_redis(self):
        """初始化Redis连接"""
        try:
            self.redis_client = redis.from_url(self.redis_url)
            self.redis_pubsub = self.redis_client.pubsub()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {e}")
    
    async def publish(self, channel: str, data: Dict[str, Any]) -> bool:
        """
        发布消息到指定频道
        
        Args:
            channel: 频道名称
            data: 消息数据
            
        Returns:
            bool: 发布是否成功
        """
        try:
            if self.backend == PubSubBackend.REDIS:
                return await self._publish_redis(channel, data)
            else:
                return await self._publish_memory(channel, data)
        except Exception as e:
            print(f"Error publishing message: {e}")
            return False
    
    async def _publish_redis(self, channel: str, data: Dict[str, Any]) -> bool:
        """Redis后端发布消息"""
        try:
            message = json.dumps(data)
            await self.redis_client.publish(channel, message)
            return True
        except Exception as e:
            print(f"Redis publish error: {e}")
            return False
    
    async def _publish_memory(self, channel: str, data: Dict[str, Any]) -> bool:
        """内存后端发布消息"""
        with self._lock:
            message = Message(channel=channel, data=data)
            
            # 存储消息到队列
            if channel not in self._message_queue:
                self._message_queue[channel] = []
            self._message_queue[channel].append(message)
            
            # 通知订阅者
            if channel in self._channels:
                for callback in self._channels[channel]:
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(message)
                        else:
                            callback(message)
                    except Exception as e:
                        print(f"Error in subscriber callback: {e}")
            
            return True
    
    def subscribe(self, channel: str, callback: Callable) -> bool:
        """
        订阅频道消息
        
        Args:
            channel: 频道名称
            callback: 回调函数，接收Message对象
            
        Returns:
            bool: 订阅是否成功
        """
        with self._lock:
            if channel not in self._channels:
                self._channels[channel] = []
            
            # 避免重复订阅
            if callback not in self._channels[channel]:
                self._channels[channel].append(callback)
                return True
            return False
    
    def unsubscribe(self, channel: str, callback: Callable) -> bool:
        """
        取消订阅
        
        Args:
            channel: 频道名称
            callback: 要移除的回调函数
            
        Returns:
            bool: 取消订阅是否成功
        """
        with self._lock:
            if channel in self._channels and callback in self._channels[channel]:
                self._channels[channel].remove(callback)
                
                # 清理空频道
                if not self._channels[channel]:
                    del self._channels[channel]
                
                return True
            return False
    
    def get_subscriber_count(self, channel: str) -> int:
        """
        获取指定频道的订阅者数量
        
        Args:
            channel: 频道名称
            
        Returns:
            int: 订阅者数量
        """
        with self._lock:
            return len(self._channels.get(channel, []))
    
    def get_channels(self) -> List[str]:
        """
        获取所有活跃频道
        
        Returns:
            List[str]: 频道列表
        """
        with self._lock:
            return list(self._channels.keys())
    
    async def get_messages(self, channel: str, limit: int = 100) -> List[Message]:
        """
        获取指定频道的消息历史
        
        Args:
            channel: 频道名称
            limit: 最大消息数量
            
        Returns:
            List[Message]: 消息列表
        """
        with self._lock:
            if channel in self._message_queue:
                messages = self._message_queue[channel][-limit:]
                return messages.copy()
            return []
    
    async def close(self):
        """关闭连接"""
        if self.backend == PubSubBackend.REDIS and self.redis_client:
            await self.redis_client.close()
            if self.redis_pubsub:
                await self.redis_pubsub.close()


# 全局协调器实例
_global_coordinator: Optional[PubSubCoordinator] = None


def get_global_coordinator(backend: PubSubBackend = PubSubBackend.MEMORY,
                          redis_url: Optional[str] = None) -> PubSubCoordinator:
    """
    获取全局协调器实例（单例模式）
    
    Args:
        backend: 后端类型
        redis_url: Redis连接URL
        
    Returns:
        PubSubCoordinator: 全局协调器实例
    """
    global _global_coordinator
    
    if _global_coordinator is None:
        _global_coordinator = PubSubCoordinator(backend, redis_url)
    
    return _global_coordinator


async def publish_message(channel: str, data: Dict[str, Any]) -> bool:
    """使用全局协调器发布消息"""
    coordinator = get_global_coordinator()
    return await coordinator.publish(channel, data)


def subscribe_to_channel(channel: str, callback: Callable) -> bool:
    """使用全局协调器订阅频道"""
    coordinator = get_global_coordinator()
    return coordinator.subscribe(channel, callback)