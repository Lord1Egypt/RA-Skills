from __future__ import annotations
"""
cache_manager.py - 智能缓存管理器

功能：
1. 缓存常见计算结果（如记忆检索、上下文构建）
2. 缓存LLM调用结果
3. 缓存文件处理结果
4. 缓存向量嵌入
5. 缓存主题分析结果

使用方式：
    from cache_manager import CacheManager
    cache = CacheManager()
    
    # 缓存结果
    cache.set("recall:用户偏好", results, ttl=3600)
    
    # 获取缓存
    results = cache.get("recall:用户偏好")
"""

import os
import json
import time
import logging
import hashlib
import hmac
import threading
from datetime import datetime, timedelta
from collections import OrderedDict

logger = logging.getLogger(__name__)

_CACHE_HMAC_KEY = hashlib.sha256(b"agent_memory_cache_v83").digest()
_MAX_VALUE_SIZE = 512 * 1024


class CacheManager:
    """智能缓存管理器"""
    
    def __init__(self, cache_dir: str = None, max_size: int = 1000, default_ttl: int = 3600):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存文件存储目录（可选）
            max_size: 内存缓存最大条目数
            default_ttl: 默认缓存过期时间（秒）
        """
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), "cache")
        self.max_size = max_size
        self.default_ttl = default_ttl
        
        # 内存缓存（LRU）
        self.memory_cache = OrderedDict()
        # 缓存元数据
        self.cache_metadata = {}
        # 线程锁
        self.lock = threading.RLock()
        
        # 确保缓存目录存在
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()

    def _compute_hmac(self, data: bytes) -> str:
        return hmac.new(_CACHE_HMAC_KEY, data, hashlib.sha256).hexdigest()
    
    def _get_cache_file(self, key: str) -> str:
        """获取缓存文件路径"""
        cache_key = self._get_cache_key(key)
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def set(self, key: str, value: any, ttl: int = None) -> bool:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），None表示使用默认值
        
        Returns:
            bool: 是否设置成功
        """
        try:
            ttl = ttl or self.default_ttl
            expires_at = time.time() + ttl

            value_json = json.dumps(value, ensure_ascii=False)
            if len(value_json) > _MAX_VALUE_SIZE:
                return False

            cache_item = {
                "value": value,
                "expires_at": expires_at,
                "created_at": time.time()
            }

            item_bytes = json.dumps(cache_item, sort_keys=True, ensure_ascii=False).encode()
            cache_item["_hmac"] = self._compute_hmac(item_bytes)

            with self.lock:
                if len(self.memory_cache) >= self.max_size:
                    self.memory_cache.popitem(last=False)

                self.memory_cache[key] = cache_item
                self.cache_metadata[key] = {
                    "expires_at": expires_at,
                    "created_at": time.time()
                }

            cache_file = self._get_cache_file(key)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_item, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"设置缓存失败: {e}")
            return False
    
    def get(self, key: str) -> any:
        """
        获取缓存
        
        Args:
            key: 缓存键
        
        Returns:
            any: 缓存值，如果不存在或已过期则返回None
        """
        try:
            with self.lock:
                # 检查内存缓存
                if key in self.memory_cache:
                    cache_item = self.memory_cache[key]
                    if time.time() < cache_item["expires_at"]:
                        # 刷新访问时间（LRU）
                        self.memory_cache.move_to_end(key)
                        return cache_item["value"]
                    else:
                        # 缓存已过期
                        del self.memory_cache[key]
                        del self.cache_metadata[key]
                
                cache_file = self._get_cache_file(key)
                if os.path.exists(cache_file):
                    with open(cache_file, "r", encoding="utf-8") as f:
                        cache_item = json.load(f)

                    stored_hmac = cache_item.pop("_hmac", None)
                    if stored_hmac:
                        item_bytes = json.dumps(cache_item, sort_keys=True, ensure_ascii=False).encode()
                        expected_hmac = self._compute_hmac(item_bytes)
                        if not hmac.compare_digest(stored_hmac, expected_hmac):
                            os.remove(cache_file)
                            return None

                    if time.time() < cache_item["expires_at"]:
                        # 加载到内存缓存
                        if len(self.memory_cache) >= self.max_size:
                            self.memory_cache.popitem(last=False)
                        self.memory_cache[key] = cache_item
                        self.cache_metadata[key] = {
                            "expires_at": cache_item["expires_at"],
                            "created_at": cache_item["created_at"]
                        }
                        return cache_item["value"]
                    else:
                        # 缓存已过期，删除文件
                        os.remove(cache_file)
                
            return None
        except Exception as e:
            print(f"获取缓存失败: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        
        Args:
            key: 缓存键
        
        Returns:
            bool: 是否删除成功
        """
        try:
            with self.lock:
                # 从内存缓存中删除
                if key in self.memory_cache:
                    del self.memory_cache[key]
                if key in self.cache_metadata:
                    del self.cache_metadata[key]
                
                # 从文件缓存中删除
                cache_file = self._get_cache_file(key)
                if os.path.exists(cache_file):
                    os.remove(cache_file)
                
            return True
        except Exception as e:
            logger.warning("删除缓存失败: %s", e)
            return False
    
    def clear(self) -> bool:
        """
        清空所有缓存
        
        Returns:
            bool: 是否清空成功
        """
        try:
            with self.lock:
                # 清空内存缓存
                self.memory_cache.clear()
                self.cache_metadata.clear()
                
                # 清空文件缓存
                for file in os.listdir(self.cache_dir):
                    if file.endswith(".json"):
                        os.remove(os.path.join(self.cache_dir, file))
                
            return True
        except Exception as e:
            print(f"清空缓存失败: {e}")
            return False
    
    def get_stats(self) -> dict:
        try:
            file_list = os.listdir(self.cache_dir)
            file_size = len([f for f in file_list if f.endswith(".json")])
        except Exception as e:
            logger.debug("cache_manager: stats listdir failed: %s", e)
            file_size = 0

        with self.lock:
            memory_size = len(self.memory_cache)
            expired_count = 0
            current_time = time.time()
            for key, metadata in self.cache_metadata.items():
                if current_time >= metadata["expires_at"]:
                    expired_count += 1

            return {
                "memory_cache_size": memory_size,
                "file_cache_size": file_size,
                "total_size": memory_size + file_size,
                "expired_count": expired_count,
                "max_size": self.max_size,
                "default_ttl": self.default_ttl
            }
    
    def cleanup(self) -> int:
        """
        清理过期缓存
        
        Returns:
            int: 清理的缓存数量
        """
        cleaned_count = 0
        current_time = time.time()
        
        with self.lock:
            # 清理内存缓存
            expired_keys = []
            for key, cache_item in self.memory_cache.items():
                if current_time >= cache_item["expires_at"]:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.memory_cache[key]
                if key in self.cache_metadata:
                    del self.cache_metadata[key]
                cleaned_count += 1
            
            # 清理文件缓存
            for file in os.listdir(self.cache_dir):
                if file.endswith(".json"):
                    cache_file = os.path.join(self.cache_dir, file)
                    try:
                        with open(cache_file, "r", encoding="utf-8") as f:
                            cache_item = json.load(f)
                        if current_time >= cache_item["expires_at"]:
                            os.remove(cache_file)
                            cleaned_count += 1
                    except Exception as e:
                        logger.debug("cache_manager: corrupt cache file: %s", e)
        
        return cleaned_count
    
    def set_recall_cache(self, query: str, results: list, ttl: int = 3600) -> bool:
        """
        设置记忆检索缓存
        
        Args:
            query: 检索查询
            results: 检索结果
            ttl: 过期时间（秒）
        
        Returns:
            bool: 是否设置成功
        """
        key = f"recall:{query}"
        return self.set(key, results, ttl)
    
    def get_recall_cache(self, query: str) -> list:
        """
        获取记忆检索缓存
        
        Args:
            query: 检索查询
        
        Returns:
            list: 检索结果，如果不存在或已过期则返回None
        """
        key = f"recall:{query}"
        return self.get(key)
    
    def set_context_cache(self, query: str, context: str, ttl: int = 3600) -> bool:
        """
        设置上下文构建缓存
        
        Args:
            query: 查询
            context: 构建的上下文
            ttl: 过期时间（秒）
        
        Returns:
            bool: 是否设置成功
        """
        key = f"context:{query}"
        return self.set(key, context, ttl)
    
    def get_context_cache(self, query: str) -> str:
        """
        获取上下文构建缓存
        
        Args:
            query: 查询
        
        Returns:
            str: 构建的上下文，如果不存在或已过期则返回None
        """
        key = f"context:{query}"
        return self.get(key)
    
    def set_llm_cache(self, prompt: str, response: str, ttl: int = 7200) -> bool:
        """
        设置LLM调用缓存
        
        Args:
            prompt: 提示词
            response: LLM响应
            ttl: 过期时间（秒）
        
        Returns:
            bool: 是否设置成功
        """
        key = f"llm:{hashlib.md5(prompt.encode()).hexdigest()}"
        return self.set(key, response, ttl)
    
    def get_llm_cache(self, prompt: str) -> str:
        """
        获取LLM调用缓存
        
        Args:
            prompt: 提示词
        
        Returns:
            str: LLM响应，如果不存在或已过期则返回None
        """
        key = f"llm:{hashlib.md5(prompt.encode()).hexdigest()}"
        return self.get(key)
    
    def set_file_cache(self, file_path: str, result: dict, ttl: int = 86400) -> bool:
        """
        设置文件处理缓存
        
        Args:
            file_path: 文件路径
            result: 处理结果
            ttl: 过期时间（秒）
        
        Returns:
            bool: 是否设置成功
        """
        key = f"file:{file_path}"
        return self.set(key, result, ttl)
    
    def get_file_cache(self, file_path: str) -> dict:
        """
        获取文件处理缓存
        
        Args:
            file_path: 文件路径
        
        Returns:
            dict: 处理结果，如果不存在或已过期则返回None
        """
        key = f"file:{file_path}"
        return self.get(key)
    
    def set_embedding_cache(self, text: str, embedding: list, ttl: int = 86400) -> bool:
        """
        设置向量嵌入缓存
        
        Args:
            text: 文本
            embedding: 向量嵌入
            ttl: 过期时间（秒）
        
        Returns:
            bool: 是否设置成功
        """
        key = f"embedding:{hashlib.md5(text.encode()).hexdigest()}"
        return self.set(key, embedding, ttl)
    
    def get_embedding_cache(self, text: str) -> list:
        """
        获取向量嵌入缓存
        
        Args:
            text: 文本
        
        Returns:
            list: 向量嵌入，如果不存在或已过期则返回None
        """
        key = f"embedding:{hashlib.md5(text.encode()).hexdigest()}"
        return self.get(key)


# 全局缓存实例
_cache_manager = None

def get_cache_manager() -> CacheManager:
    """
    获取全局缓存管理器实例
    
    Returns:
        CacheManager: 缓存管理器实例
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager
