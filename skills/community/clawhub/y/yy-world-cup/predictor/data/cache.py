"""
缓存机制模块
为API请求提供本地缓存，避免重复请求，支持TTL过期
"""

import json
import time
import os
from pathlib import Path
from typing import Any, Optional


class FileCache:
    """基于文件系统的简单缓存实现"""

    def __init__(self, cache_dir: str = "data/cache", default_ttl: int = 3600):
        """
        Args:
            cache_dir: 缓存目录
            default_ttl: 默认过期时间（秒），默认1小时
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl = default_ttl

    def _get_cache_path(self, key: str) -> Path:
        """获取缓存文件路径，key中的特殊字符替换为下划线"""
        safe_key = "".join(c if c.isalnum() else "_" for c in key)
        return self.cache_dir / f"{safe_key}.json"

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        Returns:
            缓存值，如果不存在或已过期则返回None
        """
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # 检查是否过期
            timestamp = cache_data.get('timestamp', 0)
            ttl = cache_data.get('ttl', self.default_ttl)
            if time.time() - timestamp > ttl:
                # 过期则删除
                cache_path.unlink(missing_ok=True)
                return None

            return cache_data.get('value')
        except (json.JSONDecodeError, IOError, KeyError):
            # 损坏的缓存文件，删除
            cache_path.unlink(missing_ok=True)
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        设置缓存值
        Args:
            key: 缓存键
            value: 缓存值（必须可JSON序列化）
            ttl: 过期时间（秒），None则使用默认值
        """
        cache_path = self._get_cache_path(key)
        cache_data = {
            'timestamp': time.time(),
            'ttl': ttl or self.default_ttl,
            'value': value
        }

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except (TypeError, IOError) as e:
            # 序列化失败，跳过缓存
            print(f"缓存写入失败 {key}: {e}")

    def delete(self, key: str) -> None:
        """删除指定key的缓存"""
        cache_path = self._get_cache_path(key)
        cache_path.unlink(missing_ok=True)

    def clear(self) -> None:
        """清空所有缓存"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()

    def clear_expired(self) -> int:
        """清理过期缓存，返回清理数量"""
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                timestamp = cache_data.get('timestamp', 0)
                ttl = cache_data.get('ttl', self.default_ttl)
                if time.time() - timestamp > ttl:
                    cache_file.unlink()
                    count += 1
            except (json.JSONDecodeError, IOError, KeyError):
                cache_file.unlink(missing_ok=True)
                count += 1
        return count


# 全局缓存实例
_global_cache: Optional[FileCache] = None


def get_cache() -> FileCache:
    """获取全局缓存实例（单例）"""
    global _global_cache
    if _global_cache is None:
        _global_cache = FileCache()
    return _global_cache
