"""
数据库模块 - 邮件追踪和去重

v2 重构：
- 新增字段: is_analyzed, retry_count, last_error, reason, summary
- 废除字段: is_summarized, is_urgent (改用 reason 字段判断)
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path


class MailTracker:
    """邮件追踪数据库"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            
            # 邮件记录表 (v2 重构)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provider TEXT NOT NULL,
                    email_account TEXT NOT NULL,
                    uid TEXT NOT NULL,
                    message_id TEXT,
                    subject TEXT,
                    sender TEXT,
                    received_at TEXT,
                    local_path TEXT,
                    -- 新增字段 (v2)
                    is_analyzed INTEGER DEFAULT 0,  -- 0=未分析/分析失败, 1=分析成功
                    retry_count INTEGER DEFAULT 0,   -- 已重试次数，达到3时停止重试
                    last_error TEXT,                -- 最近一次错误信息（可为 NULL）
                    reason TEXT,                    -- AI 判断理由
                    summary TEXT,                   -- AI 摘要（分析失败时存 "[分析失败]"）
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(provider, email_account, uid, message_id)
                )
            ''')
            
            # Telegram 发送记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS telegram_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    type TEXT NOT NULL,
                    chat_id TEXT,
                    message TEXT,
                    related_emails TEXT,
                    mail_count INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            
            # 执行迁移
            self._migrate_v2(cursor)
    
    def _migrate_v2(self, cursor):
        """v2 迁移：为旧数据库添加新字段"""
        # 检查当前表结构
        cursor.execute("PRAGMA table_info(emails)")
        columns = {row[1] for row in cursor.fetchall()}
        
        # 新增字段列表（v2 新增字段）
        new_fields = {
            'is_analyzed': 'INTEGER DEFAULT 0',
            'retry_count': 'INTEGER DEFAULT 0',
            'last_error': 'TEXT',
            'reason': 'TEXT',
            'summary': 'TEXT'
        }
        
        for field, field_type in new_fields.items():
            if field not in columns:
                cursor.execute(f'ALTER TABLE emails ADD COLUMN {field} {field_type}')
                print(f"  [迁移] 添加字段: {field}")
        
        # 重新获取 columns 集合（添加新字段后）
        cursor.execute("PRAGMA table_info(emails)")
        columns = {row[1] for row in cursor.fetchall()}
        
        # 为兼容旧 skill（smart-email）而保留的字段
        # 虽然逻辑上已废除，但旧代码仍依赖这些列
        legacy_fields = {
            'is_urgent': 'INTEGER DEFAULT 0',
            'is_summarized': 'INTEGER DEFAULT 0'
        }
        
        for field, field_type in legacy_fields.items():
            if field not in columns:
                cursor.execute(f'ALTER TABLE emails ADD COLUMN {field} {field_type}')
                print(f"  [迁移] 添加兼容字段: {field}")
        
        # 重新获取 columns 集合（添加兼容字段后）
        cursor.execute("PRAGMA table_info(emails)")
        columns = {row[1] for row in cursor.fetchall()}
        
        # 迁移 is_urgent 数据到 reason 字段（仅当 is_urgent 列存在时）
        # 注意：is_urgent 已废除，但 reason 字段用于存放判断理由
        # 如果 reason 为空但 is_urgent=1，说明是旧数据，填充默认值
        if 'is_urgent' in columns:
            cursor.execute('''
                UPDATE emails 
                SET is_analyzed = 1, reason = '邮件标记为紧急(旧数据迁移)'
                WHERE is_urgent = 1 AND (reason IS NULL OR reason = '')
            ''')
        
        # 迁移 is_summarized 数据（已废除，仅当 is_summarized 列存在时）
        # 如果 summary 为空且 is_summarized=1，复制 subject 作为 summary
        if 'is_summarized' in columns:
            cursor.execute('''
                UPDATE emails 
                SET summary = subject
                WHERE summary IS NULL AND is_summarized = 1
            ''')
        
        conn = cursor.connection
        conn.commit()
    
    def is_email_exists(self, provider: str, email_account: str, uid: str, message_id: str = None) -> bool:
        """检查邮件是否已存在"""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            
            if message_id:
                cursor.execute('''
                    SELECT 1 FROM emails 
                    WHERE provider = ? AND email_account = ? AND (uid = ? OR message_id = ?)
                    LIMIT 1
                ''', (provider, email_account, uid, message_id))
            else:
                cursor.execute('''
                    SELECT 1 FROM emails 
                    WHERE provider = ? AND email_account = ? AND uid = ?
                    LIMIT 1
                ''', (provider, email_account, uid))
            
            return cursor.fetchone() is not None
    
    def add_email(self, provider: str, email_account: str, uid: str, 
                  message_id: str = None, subject: str = None, 
                  sender: str = None, received_at: str = None,
                  local_path: str = None) -> int:
        """添加邮件记录（默认 is_analyzed=0, retry_count=0）"""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO emails 
                (provider, email_account, uid, message_id, subject, sender, received_at, local_path, is_analyzed, retry_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
            ''', (provider, email_account, uid, message_id, subject, sender, 
                  received_at, local_path))
            conn.commit()
            return cursor.lastrowid
    
    def get_email_by_id(self, email_id: int) -> dict:
        """根据 ID 获取邮件"""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM emails WHERE id = ?', (email_id,))
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def log_telegram_message(self, msg_type: str, chat_id: str, message: str,
                            related_emails: list = None, mail_count: int = 0):
        """记录 Telegram 消息发送"""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO telegram_logs (type, chat_id, message, related_emails, mail_count)
                VALUES (?, ?, ?, ?, ?)
            ''', (msg_type, chat_id, message, 
                  json.dumps(related_emails) if related_emails else None,
                  mail_count))
            conn.commit()
    
    def get_stats(self) -> dict:
        """获取统计信息（v2 适配）"""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            
            # 总邮件数
            cursor.execute('SELECT COUNT(*) FROM emails')
            total = cursor.fetchone()[0]
            
            # 已分析邮件数（分析成功）
            cursor.execute('SELECT COUNT(*) FROM emails WHERE is_analyzed = 1')
            analyzed = cursor.fetchone()[0]
            
            # 待分析邮件数（从未尝试或正在重试）
            cursor.execute('SELECT COUNT(*) FROM emails WHERE is_analyzed = 0 AND retry_count < 3')
            pending = cursor.fetchone()[0]
            
            # 重试失败邮件数（retry_count >= 3）
            cursor.execute('SELECT COUNT(*) FROM emails WHERE is_analyzed = 0 AND retry_count >= 3')
            failed = cursor.fetchone()[0]
            
            # 有紧急标记的邮件数（reason 字段包含"紧急"）
            cursor.execute("SELECT COUNT(*) FROM emails WHERE is_analyzed = 1 AND reason LIKE '%紧急%'")
            urgent = cursor.fetchone()[0]
            
            # Telegram 发送次数
            cursor.execute('SELECT COUNT(*) FROM telegram_logs')
            telegram_sent = cursor.fetchone()[0]
            
            return {
                "total_emails": total,
                "analyzed_emails": analyzed,
                "pending_emails": pending,
                "failed_emails": failed,
                "urgent_emails": urgent,
                "telegram_sent": telegram_sent
            }
    
    def update_email_analysis(self, email_id: int, is_urgent: bool = False):
        """更新邮件分析结果（标记为已分析）v1兼容方法"""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE emails 
                SET is_analyzed = 1, is_urgent = ?
                WHERE id = ?
            ''', (1 if is_urgent else 0, email_id))
            conn.commit()
    
    # ========== v2 新方法 ==========
    
    def get_pending_analysis_emails(self, limit: int = 20, since: str = None) -> list:
        """
        获取待分析的邮件（is_analyzed=0 且 retry_count<3）
        按 received_at 升序排列，取最早的

        Args:
            limit: 返回邮件数量限制
            since: 只返回 received_at >= since 的邮件（ISO格式时间字符串）

        Returns:
            邮件记录列表
        """
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()

            if since:
                cursor.execute('''
                    SELECT * FROM emails
                    WHERE is_analyzed = 0 AND retry_count < 3 AND received_at >= ?
                    ORDER BY received_at ASC
                    LIMIT ?
                ''', (since, limit))
            else:
                cursor.execute('''
                    SELECT * FROM emails
                    WHERE is_analyzed = 0 AND retry_count < 3
                    ORDER BY received_at ASC
                    LIMIT ?
                ''', (limit,))

            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_analyzed_emails(self, since: str = None) -> list:
        """
        获取已分析的邮件（is_analyzed=1）
        用于 Digest 阶段

        Args:
            since: 只返回 received_at >= since 的邮件

        Returns:
            邮件记录列表
        """
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()

            if since:
                cursor.execute('''
                    SELECT * FROM emails
                    WHERE is_analyzed = 1 AND received_at >= ?
                    ORDER BY received_at ASC
                ''', (since,))
            else:
                cursor.execute('''
                    SELECT * FROM emails
                    WHERE is_analyzed = 1
                    ORDER BY received_at ASC
                ''')

            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def update_analysis_result(self, email_id: int, is_urgent: bool, reason: str, summary: str):
        """
        更新邮件分析结果（v2 新方法）
        写入 is_analyzed=1, reason, summary

        Args:
            email_id: 邮件记录ID
            is_urgent: 是否紧急
            reason: AI 判断理由
            summary: AI 摘要
        """
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE emails 
                SET is_analyzed = 1, reason = ?, summary = ?
                WHERE id = ?
            ''', (reason, summary, email_id))
            conn.commit()
    
    def increment_retry_count(self, email_id: int, last_error: str):
        """
        递增邮件重试次数（v2 新方法）
        用于分析失败时记录错误并递增重试计数

        Args:
            email_id: 邮件记录ID
            last_error: 最近一次错误信息
        """
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE emails 
                SET retry_count = retry_count + 1, last_error = ?
                WHERE id = ?
            ''', (last_error, email_id))
            conn.commit()
    
    def mark_analysis_failed(self, email_id: int, last_error: str):
        """
        标记邮件分析失败（v2 新方法）
        达到重试上限后调用，写入 summary="[分析失败]"

        Args:
            email_id: 邮件记录ID
            last_error: 最后一次错误信息
        """
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE emails 
                SET summary = '[分析失败]', last_error = ?, retry_count = 3
                WHERE id = ?
            ''', (last_error, email_id))
            conn.commit()
    
    def get_email_by_local_path(self, local_path: str) -> dict:
        """根据本地路径获取邮件记录"""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM emails WHERE local_path = ?', (local_path,))
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
