#!/usr/bin/env python3
"""
简化版线程安全存储系统
"""

import json
import os
import sqlite3
import threading
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class SimpleStorage:
    """简化版线程安全存储"""
    
    def __init__(self, db_path: str = "wework_simple.db"):
        self.db_path = db_path
        self.thread_local = threading.local()
        self._init_database()
    
    def _get_connection(self):
        """获取当前线程的数据库连接"""
        if not hasattr(self.thread_local, 'conn'):
            self.thread_local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.thread_local.cursor = self.thread_local.conn.cursor()
        return self.thread_local.conn, self.thread_local.cursor
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = conn.cursor()
        
        # 创建消息表（简化版）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                msg_id TEXT UNIQUE NOT NULL,
                msg_type TEXT NOT NULL,
                from_user TEXT NOT NULL,
                to_users TEXT,
                room_id TEXT,
                content TEXT,
                timestamp INTEGER NOT NULL,
                received_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_from_user ON messages(from_user)')
        
        conn.commit()
        conn.close()
        logger.info("数据库初始化完成")
    
    def save_message(self, message_data: Dict[str, Any]) -> bool:
        """保存消息"""
        conn, cursor = self._get_connection()
        
        try:
            msg_id = message_data.get('msg_id', f"auto_{datetime.now().timestamp()}")
            msg_type = message_data.get('type', 'unknown')
            from_user = message_data.get('from', '')
            to_users = json.dumps(message_data.get('to', []))
            room_id = message_data.get('room', '')
            content = message_data.get('content', '')
            timestamp = message_data.get('time', int(datetime.now().timestamp()))
            
            # 构建元数据
            metadata = {
                'original_data': message_data,
                'parsed_time': datetime.now().isoformat()
            }
            
            cursor.execute('''
                INSERT OR REPLACE INTO messages 
                (msg_id, msg_type, from_user, to_users, room_id, content, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (msg_id, msg_type, from_user, to_users, room_id, content, timestamp, json.dumps(metadata)))
            
            conn.commit()
            logger.info(f"消息保存成功: {msg_id} ({msg_type})")
            return True
            
        except Exception as e:
            logger.error(f"保存消息失败: {e}")
            conn.rollback()
            return False
    
    def query_messages(self, 
                      start_time: Optional[int] = None,
                      end_time: Optional[int] = None,
                      from_user: Optional[str] = None,
                      room_id: Optional[str] = None,
                      msg_type: Optional[str] = None,
                      limit: int = 100,
                      offset: int = 0) -> List[Dict[str, Any]]:
        """查询消息"""
        conn, cursor = self._get_connection()
        
        try:
            query = "SELECT * FROM messages WHERE 1=1"
            params = []
            
            if start_time:
                query += " AND timestamp >= ?"
                params.append(start_time)
            
            if end_time:
                query += " AND timestamp <= ?"
                params.append(end_time)
            
            if from_user:
                query += " AND from_user = ?"
                params.append(from_user)
            
            if room_id:
                query += " AND room_id = ?"
                params.append(room_id)
            
            if msg_type:
                query += " AND msg_type = ?"
                params.append(msg_type)
            
            query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            
            messages = []
            for row in rows:
                message = dict(zip(column_names, row))
                
                # 解析JSON字段
                if message.get('to_users'):
                    message['to_users'] = json.loads(message['to_users'])
                
                if message.get('metadata'):
                    message['metadata'] = json.loads(message['metadata'])
                
                messages.append(message)
            
            return messages
            
        except Exception as e:
            logger.error(f"查询消息失败: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        conn, cursor = self._get_connection()
        
        try:
            stats = {}
            
            # 消息总数
            cursor.execute('SELECT COUNT(*) FROM messages')
            stats['total_messages'] = cursor.fetchone()[0]
            
            # 按类型统计
            cursor.execute('SELECT msg_type, COUNT(*) FROM messages GROUP BY msg_type')
            stats['message_types'] = dict(cursor.fetchall())
            
            # 用户数
            cursor.execute('SELECT COUNT(DISTINCT from_user) FROM messages')
            stats['total_users'] = cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {}