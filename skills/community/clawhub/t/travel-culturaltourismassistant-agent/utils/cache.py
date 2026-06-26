# -*- coding: utf-8 -*-
"""
缓存管理模块
"""
import json
import sqlite3
import time
from typing import Any, Optional
from pathlib import Path
from loguru import logger

class CacheManager:
    """
    SQLite 缓存管理器
    """
    
    def __init__(self, default_ttl: int = 86400):
        """
        初始化缓存管理器
        :param default_ttl: 默认缓存时长（秒），默认24小时
        """
        self.default_ttl = default_ttl
        self.db_path = Path.home() / ".openclaw" / "skills" / "travel-ai" / "cache.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    expire_at INTEGER NOT NULL,
                    created_at INTEGER NOT NULL
                )
            ''')
            
            # 创建过期索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_cache_expire ON cache(expire_at)
            ''')
            
            conn.commit()
            conn.close()
            
            logger.debug(f"缓存数据库初始化完成：{self.db_path}")
        except Exception as e:
            logger.error(f"缓存数据库初始化失败：{str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取缓存
        :param key: 缓存键
        :param default: 不存在时返回的默认值
        :return: 缓存值
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = int(time.time())
            cursor.execute('''
                SELECT value FROM cache 
                WHERE key = ? AND expire_at > ?
            ''', (key, now))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                value = json.loads(result[0])
                logger.debug(f"命中缓存：{key}")
                return value
            
            return default
            
        except Exception as e:
            logger.error(f"获取缓存失败：{str(e)}")
            return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        设置缓存
        :param key: 缓存键
        :param value: 缓存值（必须可序列化为JSON）
        :param ttl: 缓存时长（秒），默认使用default_ttl
        :return: 是否设置成功
        """
        try:
            ttl = ttl if ttl is not None else self.default_ttl
            now = int(time.time())
            expire_at = now + ttl
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 序列化值
            value_json = json.dumps(value, ensure_ascii=False)
            
            cursor.execute('''
                REPLACE INTO cache (key, value, expire_at, created_at)
                VALUES (?, ?, ?, ?)
            ''', (key, value_json, expire_at, now))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"设置缓存：{key}，过期时间：{ttl}秒")
            return True
            
        except Exception as e:
            logger.error(f"设置缓存失败：{str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        :param key: 缓存键
        :return: 是否删除成功
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM cache WHERE key = ?', (key,))
            conn.commit()
            
            affected = cursor.rowcount
            conn.close()
            
            if affected > 0:
                logger.debug(f"删除缓存：{key}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"删除缓存失败：{str(e)}")
            return False
    
    def clear_expired(self) -> int:
        """
        清理过期缓存
        :return: 清理的缓存数量
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = int(time.time())
            cursor.execute('DELETE FROM cache WHERE expire_at <= ?', (now,))
            conn.commit()
            
            deleted = cursor.rowcount
            conn.close()
            
            if deleted > 0:
                logger.info(f"清理了 {deleted} 条过期缓存")
            
            return deleted
            
        except Exception as e:
            logger.error(f"清理过期缓存失败：{str(e)}")
            return 0
    
    def clear_all(self) -> int:
        """
        清空所有缓存
        :return: 清空的缓存数量
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM cache')
            conn.commit()
            
            deleted = cursor.rowcount
            conn.close()
            
            logger.info(f"清空了 {deleted} 条缓存")
            return deleted
            
        except Exception as e:
            logger.error(f"清空缓存失败：{str(e)}")
            return 0
    
    def get_stats(self) -> dict:
        """
        获取缓存统计信息
        :return: 统计信息字典
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 总缓存数
            cursor.execute('SELECT COUNT(*) FROM cache')
            total = cursor.fetchone()[0]
            
            # 过期缓存数
            now = int(time.time())
            cursor.execute('SELECT COUNT(*) FROM cache WHERE expire_at <= ?', (now,))
            expired = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total": total,
                "expired": expired,
                "active": total - expired,
                "db_path": str(self.db_path)
            }
            
        except Exception as e:
            logger.error(f"获取缓存统计失败：{str(e)}")
            return {}
