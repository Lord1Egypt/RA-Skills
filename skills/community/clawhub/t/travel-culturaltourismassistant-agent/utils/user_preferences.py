# -*- coding: utf-8 -*-
"""
用户偏好管理模块，集成 self-improving-agent 机制
"""
import json
import sqlite3
import time
from typing import Any, List, Dict, Optional
from pathlib import Path
from loguru import logger

class UserPreferenceManager:
    """
    用户偏好管理器，记录和分析用户使用习惯
    """
    
    def __init__(self):
        """初始化用户偏好管理器"""
        self.db_path = Path.home() / ".openclaw" / "skills" / "travel-ai" / "preferences.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 用户基础信息表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    created_at INTEGER NOT NULL,
                    last_active_at INTEGER NOT NULL,
                    total_queries INTEGER DEFAULT 0
                )
            ''')
            
            # 用户偏好记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    preference_key TEXT NOT NULL,
                    preference_value TEXT NOT NULL,
                    count INTEGER DEFAULT 1,
                    last_used_at INTEGER NOT NULL,
                    UNIQUE(user_id, preference_key, preference_value)
                )
            ''')
            
            # 用户查询历史表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    command TEXT NOT NULL,
                    args TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    success INTEGER DEFAULT 1
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_preferences_user ON preferences(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_user ON query_history(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_time ON query_history(timestamp)')
            
            conn.commit()
            conn.close()
            
            logger.debug("用户偏好数据库初始化完成")
        except Exception as e:
            logger.error(f"用户偏好数据库初始化失败：{str(e)}")
    
    def _ensure_user_exists(self, user_id: str) -> None:
        """确保用户存在，不存在则创建"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = int(time.time())
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, created_at, last_active_at)
                VALUES (?, ?, ?)
            ''', (user_id, now, now))
            
            # 更新最后活跃时间
            cursor.execute('''
                UPDATE users 
                SET last_active_at = ?, total_queries = total_queries + 1
                WHERE user_id = ?
            ''', (now, user_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"确保用户存在失败：{str(e)}")
    
    def record_preference(self, user_id: str, preference_key: str, preference_value: Any) -> bool:
        """
        记录用户偏好
        :param user_id: 用户ID
        :param preference_key: 偏好类型，如：recent_cities, travel_preferences, attraction_categories等
        :param preference_value: 偏好值，可以是字符串、列表等可JSON序列化的类型
        :return: 是否记录成功
        """
        try:
            # 确保用户存在
            self._ensure_user_exists(user_id)
            
            # 序列化值
            if isinstance(preference_value, list):
                value_str = json.dumps(preference_value, ensure_ascii=False)
            else:
                value_str = str(preference_value)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = int(time.time())
            
            # 插入或更新偏好记录
            cursor.execute('''
                INSERT INTO preferences (user_id, preference_key, preference_value, count, last_used_at)
                VALUES (?, ?, ?, 1, ?)
                ON CONFLICT(user_id, preference_key, preference_value)
                DO UPDATE SET count = count + 1, last_used_at = ?
            ''', (user_id, preference_key, value_str, now, now))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"记录用户偏好：{user_id} - {preference_key} = {preference_value}")
            return True
            
        except Exception as e:
            logger.error(f"记录用户偏好失败：{str(e)}")
            return False
    
    def get_preferences(self, user_id: str, preference_key: str, limit: int = 5) -> List[Any]:
        """
        获取用户的偏好列表，按使用频率排序
        :param user_id: 用户ID
        :param preference_key: 偏好类型
        :param limit: 返回数量，默认5个
        :return: 偏好值列表
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT preference_value, count FROM preferences
                WHERE user_id = ? AND preference_key = ?
                ORDER BY count DESC, last_used_at DESC
                LIMIT ?
            ''', (user_id, preference_key, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            preferences = []
            for value_str, count in results:
                try:
                    # 尝试解析JSON
                    value = json.loads(value_str)
                except json.JSONDecodeError:
                    value = value_str
                preferences.append(value)
            
            logger.debug(f"获取用户偏好：{user_id} - {preference_key} = {preferences}")
            return preferences
            
        except Exception as e:
            logger.error(f"获取用户偏好失败：{str(e)}")
            return []
    
    def get_most_frequent(self, user_id: str, preference_key: str, default: Any = None) -> Any:
        """
        获取用户最常用的偏好值
        :param user_id: 用户ID
        :param preference_key: 偏好类型
        :param default: 不存在时的默认值
        :return: 最常用的偏好值
        """
        preferences = self.get_preferences(user_id, preference_key, limit=1)
        return preferences[0] if preferences else default
    
    def record_query(self, user_id: str, command: str, args: List[str], success: bool = True) -> bool:
        """
        记录用户查询历史
        :param user_id: 用户ID
        :param command: 执行的命令
        :param args: 命令参数
        :param success: 是否执行成功
        :return: 是否记录成功
        """
        try:
            # 确保用户存在
            self._ensure_user_exists(user_id)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = int(time.time())
            args_str = json.dumps(args, ensure_ascii=False)
            
            cursor.execute('''
                INSERT INTO query_history (user_id, command, args, timestamp, success)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, command, args_str, now, 1 if success else 0))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"记录用户查询：{user_id} - {command} {args}")
            return True
            
        except Exception as e:
            logger.error(f"记录用户查询失败：{str(e)}")
            return False
    
    def get_recent_queries(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取用户最近的查询历史
        :param user_id: 用户ID
        :param limit: 返回数量，默认10条
        :return: 查询历史列表
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT command, args, timestamp, success FROM query_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            history = []
            for command, args_str, timestamp, success in results:
                try:
                    args = json.loads(args_str)
                except json.JSONDecodeError:
                    args = []
                
                history.append({
                    "command": command,
                    "args": args,
                    "timestamp": timestamp,
                    "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)),
                    "success": success == 1
                })
            
            return history
            
        except Exception as e:
            logger.error(f"获取用户查询历史失败：{str(e)}")
            return []
    
    def get_user_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        获取用户统计信息
        :param user_id: 用户ID
        :return: 统计信息字典
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 获取用户基础信息
            cursor.execute('''
                SELECT created_at, last_active_at, total_queries FROM users
                WHERE user_id = ?
            ''', (user_id,))
            
            user_info = cursor.fetchone()
            if not user_info:
                return None
            
            created_at, last_active_at, total_queries = user_info
            
            # 获取查询成功率
            cursor.execute('''
                SELECT COUNT(*) FROM query_history
                WHERE user_id = ? AND success = 1
            ''', (user_id,))
            success_count = cursor.fetchone()[0]
            
            success_rate = (success_count / total_queries * 100) if total_queries > 0 else 0
            
            # 获取最常使用的命令
            cursor.execute('''
                SELECT command, COUNT(*) as count FROM query_history
                WHERE user_id = ?
                GROUP BY command
                ORDER BY count DESC
                LIMIT 1
            ''', (user_id,))
            favorite_command = cursor.fetchone()
            favorite_command = favorite_command[0] if favorite_command else None
            
            # 获取最常搜索的城市
            recent_cities = self.get_preferences(user_id, "recent_cities", limit=3)
            
            conn.close()
            
            return {
                "user_id": user_id,
                "created_at": created_at,
                "created_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_at)),
                "last_active_at": last_active_at,
                "last_active_datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_active_at)),
                "total_queries": total_queries,
                "success_count": success_count,
                "success_rate": f"{success_rate:.1f}%",
                "favorite_command": favorite_command,
                "recent_cities": recent_cities
            }
            
        except Exception as e:
            logger.error(f"获取用户统计信息失败：{str(e)}")
            return None
    
    def delete_user_data(self, user_id: str) -> bool:
        """
        删除用户的所有数据（符合隐私要求）
        :param user_id: 用户ID
        :return: 是否删除成功
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 删除用户所有数据
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM preferences WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM query_history WHERE user_id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"删除用户数据：{user_id}")
            return True
            
        except Exception as e:
            logger.error(f"删除用户数据失败：{str(e)}")
            return False
