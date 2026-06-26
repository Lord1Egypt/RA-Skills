"""
存储后端抽象和实现
"""

import json
import time
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class StorageBackend(ABC):
    """存储后端抽象基类"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """获取值"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, expire: Optional[int] = None):
        """设置值，可选过期时间（秒）"""
        pass
    
    @abstractmethod
    def delete(self, key: str):
        """删除键"""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        pass
    
    @abstractmethod
    def hget(self, key: str, field: str) -> Optional[Any]:
        """获取哈希字段"""
        pass
    
    @abstractmethod
    def hset(self, key: str, field: str, value: Any):
        """设置哈希字段"""
        pass
    
    @abstractmethod
    def hgetall(self, key: str) -> Dict[str, Any]:
        """获取所有哈希字段"""
        pass
    
    @abstractmethod
    def setnx(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        设置值（仅当键不存在时）
        用于防重放等原子操作
        
        Returns:
            bool: 是否设置成功
        """
        pass


class MemoryStorage(StorageBackend):
    """内存存储实现（单进程）"""
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._hash_data: Dict[str, Dict[str, Any]] = {}
        self._expire: Dict[str, float] = {}
    
    def _cleanup_expired(self):
        """清理过期键"""
        now = time.time()
        expired = [k for k, v in self._expire.items() if v < now]
        for k in expired:
            self._data.pop(k, None)
            self._hash_data.pop(k, None)
            self._expire.pop(k, None)
    
    def get(self, key: str) -> Optional[Any]:
        self._cleanup_expired()
        value = self._data.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: Any, expire: Optional[int] = None):
        self._data[key] = json.dumps(value)
        if expire:
            self._expire[key] = time.time() + expire
    
    def delete(self, key: str):
        self._data.pop(key, None)
        self._hash_data.pop(key, None)
        self._expire.pop(key, None)
    
    def exists(self, key: str) -> bool:
        self._cleanup_expired()
        return key in self._data or key in self._hash_data
    
    def hget(self, key: str, field: str) -> Optional[Any]:
        self._cleanup_expired()
        value = self._hash_data.get(key, {}).get(field)
        return json.loads(value) if value else None
    
    def hset(self, key: str, field: str, value: Any):
        if key not in self._hash_data:
            self._hash_data[key] = {}
        self._hash_data[key][field] = json.dumps(value)
    
    def hgetall(self, key: str) -> Dict[str, Any]:
        self._cleanup_expired()
        data = self._hash_data.get(key, {})
        return {k: json.loads(v) for k, v in data.items()}
    
    def setnx(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        if self.exists(key):
            return False
        self.set(key, value, expire)
        return True


class RedisStorage(StorageBackend):
    """Redis 存储实现"""
    
    def __init__(self):
        import redis
        settings = get_settings()
        
        try:
            self._redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
            self._redis.ping()
            logger.info("✅ Redis connected")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        value = self._redis.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: Any, expire: Optional[int] = None):
        data = json.dumps(value)
        if expire:
            self._redis.setex(key, expire, data)
        else:
            self._redis.set(key, data)
    
    def delete(self, key: str):
        self._redis.delete(key)
    
    def exists(self, key: str) -> bool:
        return self._redis.exists(key) > 0
    
    def hget(self, key: str, field: str) -> Optional[Any]:
        value = self._redis.hget(key, field)
        return json.loads(value) if value else None
    
    def hset(self, key: str, field: str, value: Any):
        self._redis.hset(key, field, json.dumps(value))
    
    def hgetall(self, key: str) -> Dict[str, Any]:
        data = self._redis.hgetall(key)
        return {k: json.loads(v) for k, v in data.items()}
    
    def setnx(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        data = json.dumps(value)
        result = self._redis.set(key, data, nx=True, ex=expire)
        return bool(result)


def create_storage_backend() -> StorageBackend:
    """
    创建存储后端
    优先使用 Redis，如果不可用则回退到内存存储
    """
    try:
        return RedisStorage()
    except Exception as e:
        logger.warning(f"⚠️  Falling back to memory storage: {e}")
        return MemoryStorage()
