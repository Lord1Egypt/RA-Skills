#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
session_unified.py — 统一会话管理（v2.6）

合并原 scheduler.py（外呼调度）与 session_manager.py（被动接收）为双向子系统：
1. 统一会话表（会话ID/方向/状态/上下文/用户ID/创建时间）
2. 状态机复用（state_machine.py 的 CallStateMachine）
3. 记录与统计同源（call_record_subsystem.py）
4. 消除双份维护

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-24)
"""

import json
import time
import sqlite3
import logging
import os
import re
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from enum import Enum

logger = logging.getLogger(__name__)


# ==========================================
# 配置
# ==========================================

DB_PATH = os.path.join(os.path.expanduser("~"), ".wecom_voice", "sessions.db")


# ==========================================
# 会话方向枚举
# ==========================================

class SessionDirection(Enum):
    """会话方向"""
    INBOUND = "inbound"     # 被动接收（用户呼入/发消息）
    OUTBOUND = "outbound"   # 主动外呼（系统发起）
    VOICEMAIL = "voicemail" # 语音留言


class SessionStatus(Enum):
    """会话状态"""
    ACTIVE = "active"           # 进行中
    WAITING = "waiting"         # 等待用户输入
    CONFIRMING = "confirming"   # 二次确认中
    IVR = "ivr"                 # IVR 菜单中
    TRANSFERRED = "transferred" # 已转人工
    COMPLETED = "completed"     # 正常结束
    TIMEOUT = "timeout"         # 超时结束
    FAILED = "failed"           # 失败


# ==========================================
# 会话记录
# ==========================================

class SessionRecord:
    """单条会话记录"""

    def __init__(self, session_id: str, userid: str, direction: str,
                 status: str = "active", context: Dict = None,
                 created_at: str = None, updated_at: str = None,
                 id: int = None, chat_id: str = "", speaker_userid: str = "",
                 speaker_role: str = ""):
        self.id = id
        self.session_id = session_id
        self.userid = userid
        self.direction = direction
        self.status = status
        self.context = context or {}
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        # v2.9 群聊维度：chat_id 为空表示单聊；speaker_* 记录群内发言者身份
        self.chat_id = chat_id
        self.speaker_userid = speaker_userid
        self.speaker_role = speaker_role

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "userid": self.userid,
            "direction": self.direction,
            "status": self.status,
            "context": self.context,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "chat_id": self.chat_id,
            "speaker_userid": self.speaker_userid,
            "speaker_role": self.speaker_role,
        }


# ==========================================
# 数据库管理
# ==========================================

class SessionDB:
    """统一会话数据库管理"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL UNIQUE,
                    userid TEXT NOT NULL,
                    direction TEXT NOT NULL DEFAULT 'inbound',
                    status TEXT NOT NULL DEFAULT 'active',
                    context TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    chat_id TEXT DEFAULT ''
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_userid
                ON sessions(userid)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_status
                ON sessions(status)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_direction
                ON sessions(direction)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_created
                ON sessions(created_at)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_chat_id
                ON sessions(chat_id)
            """)
            # 兼容旧库：补充 chat_id 列（v2.9 群聊维度）
            self._ensure_column(conn, "sessions", "chat_id", "TEXT DEFAULT ''")

    @staticmethod
    def _ensure_column(conn, table: str, column: str, ddl: str):
        """兼容旧库：若列不存在则追加（v2.9 群聊维度）"""
        try:
            cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
            if column not in cols:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}")
        except Exception as e:
            logger.warning(f"补充列失败 {table}.{column}: {e}")

    def insert_session(self, session: SessionRecord) -> bool:
        """插入新会话"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO sessions (session_id, userid, direction, status, context, created_at, updated_at, chat_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session.session_id, session.userid, session.direction,
                    session.status, json.dumps(session.context, ensure_ascii=False),
                    session.created_at, session.updated_at, session.chat_id or ""
                ))
            return True
        except sqlite3.IntegrityError:
            return False

    def get_active_group_session(self, chat_id: str) -> Optional[SessionRecord]:
        """获取群聊活跃会话（以 chat_id 为主键维度，群内共享上下文）"""
        if not chat_id:
            return None
        threshold = (datetime.now() - timedelta(minutes=5)).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM sessions WHERE chat_id = ? AND updated_at > ? AND status IN ('active', 'waiting', 'confirming', 'ivr') ORDER BY updated_at DESC LIMIT 1",
                (chat_id, threshold)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_record(row)
        return None

    def update_session(self, session_id: str, **kwargs) -> bool:
        """更新会话"""
        if not kwargs:
            return False
        kwargs["updated_at"] = datetime.now().isoformat()
        if "context" in kwargs and isinstance(kwargs["context"], dict):
            kwargs["context"] = json.dumps(kwargs["context"], ensure_ascii=False)
        set_clause = ", ".join(f"{k} = ?" for k in kwargs.keys())
        values = list(kwargs.values()) + [session_id]
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(f"UPDATE sessions SET {set_clause} WHERE session_id = ?", values)
            return True
        except Exception as e:
            logger.warning(f"更新会话失败: {e}")
            return False

    def get_session(self, session_id: str) -> Optional[SessionRecord]:
        """查询单条会话"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_record(row)
        return None

    def get_active_session(self, userid: str) -> Optional[SessionRecord]:
        """获取用户活跃会话（最近5分钟内更新的）"""
        threshold = (datetime.now() - timedelta(minutes=5)).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM sessions WHERE userid = ? AND updated_at > ? AND status IN ('active', 'waiting', 'confirming', 'ivr') ORDER BY updated_at DESC LIMIT 1",
                (userid, threshold)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_record(row)
        return None

    def get_sessions_by_date(self, date_str: str) -> List[SessionRecord]:
        """查询某天所有会话"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM sessions WHERE created_at LIKE ? ORDER BY created_at DESC",
                (f"{date_str}%",)
            )
            return [self._row_to_record(row) for row in cursor.fetchall()]

    def get_sessions_by_direction(self, direction: str) -> List[SessionRecord]:
        """按方向查询会话"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM sessions WHERE direction = ? ORDER BY created_at DESC",
                (direction,)
            )
            return [self._row_to_record(row) for row in cursor.fetchall()]

    def count_sessions(self, direction: str = None, status: str = None) -> int:
        """统计会话数量"""
        with sqlite3.connect(self.db_path) as conn:
            where_clause = ""
            params = []
            conditions = []
            if direction:
                conditions.append("direction = ?")
                params.append(direction)
            if status:
                conditions.append("status = ?")
                params.append(status)
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
            row = conn.execute(f"SELECT COUNT(*) FROM sessions {where_clause}", params).fetchone()
            return row[0]

    def cleanup_expired(self, timeout_minutes: int = 30) -> int:
        """清理过期会话"""
        threshold = (datetime.now() - timedelta(minutes=timeout_minutes)).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE sessions SET status = 'timeout' WHERE updated_at < ? AND status IN ('active', 'waiting', 'confirming', 'ivr')",
                (threshold,)
            )
            return cursor.rowcount

    def _row_to_record(self, row) -> SessionRecord:
        """数据库行转 SessionRecord"""
        context = {}
        try:
            context = json.loads(row["context"]) if row["context"] else {}
        except (json.JSONDecodeError, TypeError):
            pass
        keys = row.keys()
        chat_id = row["chat_id"] if "chat_id" in keys else ""
        return SessionRecord(
            id=row["id"],
            session_id=row["session_id"],
            userid=row["userid"],
            direction=row["direction"],
            status=row["status"],
            context=context,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            chat_id=chat_id,
        )


# ==========================================
# 统一会话管理器
# ==========================================

class UnifiedSessionManager:
    """
    统一会话管理器
    
    合并外呼调度与被动接收为双向子系统：
    - 入站会话：用户发语音/文本 → 创建/恢复会话 → 意图路由 → 处理
    - 出站会话：调度器触发 → 创建会话 → 外呼 → 交互 → 结束
    - 统一上下文：每轮实体、意图、状态共享
    - 统一统计：所有会话数据同源
    
    使用方式：
        mgr = UnifiedSessionManager()
        
        # 入站
        session = mgr.get_or_create_session("user_123", "inbound")
        mgr.update_context("session_001", {"person": "张三"})
        
        # 出站
        session = mgr.create_outbound_session("13800138000", "预约确认")
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db = SessionDB(db_path)
        self._lock = threading.Lock()
        logger.info("统一会话管理器已初始化")

    # === 会话生命周期 ===

    def get_or_create_session(self, userid: str, direction: str = "inbound",
                               context: Dict = None, chat_type: str = "single",
                               chat_id: str = None, speaker_userid: str = "",
                               speaker_role: str = "") -> SessionRecord:
        """
        获取或创建会话

        如果用户有活跃会话则恢复，否则创建新会话。
        v2.9 新增群聊维度：chat_type=group 时以 chat_id 为主键维度（群内共享上下文）。

        Args:
            userid: 用户ID（群聊时为发言者 userid）
            direction: 方向（inbound/outbound/voicemail）
            context: 初始上下文
            chat_type: 会话类型（single/group）
            chat_id: 群聊ID（群聊时必填，作为群维度主键）
            speaker_userid: 发言者 userid（群聊）
            speaker_role: 发言者角色（member/admin/unknown）

        Returns:
            SessionRecord: 会话记录
        """
        if chat_type == "group" and chat_id:
            active = self.db.get_active_group_session(chat_id)
            # 群维度：userid 字段用 chat_id，避免与单聊 userid 碰撞
            effective_userid = chat_id
        else:
            active = self.db.get_active_session(userid)
            effective_userid = userid

        if active:
            # 更新活跃时间
            self.db.update_session(active.session_id)
            merged = {**active.context, **(context or {})}
            # 群聊每轮刷新发言者身份，保证身份上下文最新
            if chat_type == "group":
                merged.update({
                    "chat_type": "group",
                    "chat_id": chat_id,
                    "speaker_userid": speaker_userid,
                    "speaker_role": speaker_role,
                })
                active.speaker_userid = speaker_userid
                active.speaker_role = speaker_role
            self.db.update_session(active.session_id, context=merged)
            active.context = merged
            return active

        # 创建新会话
        return self.create_session(
            effective_userid, direction, context, chat_type=chat_type, chat_id=chat_id,
            speaker_userid=speaker_userid, speaker_role=speaker_role,
        )

    def create_session(self, userid: str, direction: str = "inbound",
                        context: Dict = None, chat_type: str = "single",
                        chat_id: str = None, speaker_userid: str = "",
                        speaker_role: str = "") -> SessionRecord:
        """
        创建新会话

        Args:
            userid: 用户ID（群聊时为发言者 userid）
            direction: 方向
            context: 初始上下文
            chat_type: 会话类型（single/group）
            chat_id: 群聊ID
            speaker_userid: 发言者 userid
            speaker_role: 发言者角色

        Returns:
            SessionRecord: 新会话记录
        """
        # 群聊以 chat_id 生成会话ID，单聊用 userid
        seed = chat_id if (chat_type == "group" and chat_id) else userid
        session_id = self._generate_session_id(seed)
        ctx = dict(context or {})
        if chat_type == "group":
            ctx.update({
                "chat_type": "group",
                "chat_id": chat_id,
                "speaker_userid": speaker_userid,
                "speaker_role": speaker_role,
            })
        session = SessionRecord(
            session_id=session_id,
            userid=userid,
            direction=direction,
            status="active",
            context=ctx,
            chat_id=chat_id or "",
            speaker_userid=speaker_userid,
            speaker_role=speaker_role,
        )
        self.db.insert_session(session)
        logger.info(f"创建会话: {session_id}, 用户: {userid}, 方向: {direction}, 类型: {chat_type}")
        return session

    def create_outbound_session(self, target: str, script: str = "") -> SessionRecord:
        """
        创建外呼会话
        
        Args:
            target: 被叫方（手机号/用户ID）
            script: 外呼话术
            
        Returns:
            SessionRecord: 外呼会话记录
        """
        context = {
            "script": script,
            "call_start": datetime.now().isoformat(),
        }
        return self.create_session(target, "outbound", context)

    def update_context(self, session_id: str, context: Dict) -> bool:
        """
        更新会话上下文（合并而非覆盖）
        
        Args:
            session_id: 会话ID
            context: 要合并的上下文
            
        Returns:
            bool: 成功返回 True
        """
        session = self.db.get_session(session_id)
        if not session:
            return False
        merged = {**session.context, **context}
        return self.db.update_session(session_id, context=merged)

    def update_status(self, session_id: str, status: str) -> bool:
        """
        更新会话状态
        
        Args:
            session_id: 会话ID
            status: 新状态
            
        Returns:
            bool: 成功返回 True
        """
        return self.db.update_session(session_id, status=status)

    def end_session(self, session_id: str, reason: str = "completed") -> bool:
        """
        结束会话
        
        Args:
            session_id: 会话ID
            reason: 结束原因（completed/timeout/failed）
            
        Returns:
            bool: 成功返回 True
        """
        return self.db.update_session(session_id, status=reason)

    def transfer_to_human(self, session_id: str) -> bool:
        """
        转接人工
        
        Args:
            session_id: 会话ID
            
        Returns:
            bool: 成功返回 True
        """
        return self.db.update_session(session_id, status="transferred")

    # === 查询 ===

    def get_session(self, session_id: str) -> Optional[SessionRecord]:
        """获取会话"""
        return self.db.get_session(session_id)

    def get_active_session(self, userid: str) -> Optional[SessionRecord]:
        """获取用户活跃会话"""
        return self.db.get_active_session(userid)

    def get_today_sessions(self) -> List[SessionRecord]:
        """获取今日会话"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        return self.db.get_sessions_by_date(date_str)

    def get_sessions_by_direction(self, direction: str) -> List[SessionRecord]:
        """按方向获取会话"""
        return self.db.get_sessions_by_direction(direction)

    # === 统计 ===

    def get_stats(self, period: str = "day") -> Dict:
        """
        获取统计数据
        
        Args:
            period: 统计周期（day/week/month）
            
        Returns:
            dict: 统计数据
        """
        start_date, end_date = self._get_date_range(period)
        sessions = self.db.get_sessions_by_date(start_date.strftime("%Y-%m-%d"))

        # 如果是一天的数据，直接统计
        if period == "day":
            total = len(sessions)
            inbound = len([s for s in sessions if s.direction == "inbound"])
            outbound = len([s for s in sessions if s.direction == "outbound"])
            voicemail = len([s for s in sessions if s.direction == "voicemail"])
            completed = len([s for s in sessions if s.status == "completed"])
            timeout = len([s for s in sessions if s.status == "timeout"])
            transferred = len([s for s in sessions if s.status == "transferred"])
            
            return {
                "period": period,
                "date_range": f"{start_date.strftime('%Y-%m-%d')}",
                "total": total,
                "inbound": inbound,
                "outbound": outbound,
                "voicemail": voicemail,
                "completed": completed,
                "timeout": timeout,
                "transferred": transferred,
                "completion_rate": completed / total if total > 0 else 0,
            }
        
        # 更长时间范围需要查询所有然后过滤
        all_sessions = []
        with sqlite3.connect(self.db.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM sessions WHERE created_at >= ? AND created_at <= ? ORDER BY created_at",
                (start_date.isoformat(), end_date.isoformat())
            )
            all_sessions = [self.db._row_to_record(row) for row in cursor.fetchall()]

        total = len(all_sessions)
        inbound = len([s for s in all_sessions if s.direction == "inbound"])
        outbound = len([s for s in all_sessions if s.direction == "outbound"])
        voicemail = len([s for s in all_sessions if s.direction == "voicemail"])
        completed = len([s for s in all_sessions if s.status == "completed"])
        timeout = len([s for s in all_sessions if s.status == "timeout"])
        transferred = len([s for s in all_sessions if s.status == "transferred"])

        return {
            "period": period,
            "date_range": f"{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}",
            "total": total,
            "inbound": inbound,
            "outbound": outbound,
            "voicemail": voicemail,
            "completed": completed,
            "timeout": timeout,
            "transferred": transferred,
            "completion_rate": completed / total if total > 0 else 0,
        }

    def render_stats(self, period: str = "day") -> str:
        """渲染统计看板"""
        stats = self.get_stats(period)
        if stats["total"] == 0:
            return f"\n📊 {stats['date_range']}: 暂无会话记录\n"
        
        lines = [
            "", "=" * 60,
            "📊 会话统计看板",
            "=" * 60,
            f"时间范围: {stats['date_range']}",
            f"总会话数: {stats['total']}",
            f"  入站: {stats['inbound']}",
            f"  出站: {stats['outbound']}",
            f"  留言: {stats['voicemail']}",
            f"  完成: {stats['completed']}",
            f"  超时: {stats['timeout']}",
            f"  转人工: {stats['transferred']}",
            f"  完成率: {stats['completion_rate']*100:.1f}%",
            "=" * 60,
        ]
        return "\n".join(lines)

    # === 维护 ===

    def cleanup_expired(self, timeout_minutes: int = 30) -> int:
        """清理过期会话"""
        count = self.db.cleanup_expired(timeout_minutes)
        if count > 0:
            logger.info(f"清理 {count} 个过期会话")
        return count

    # === 内部方法 ===

    def _generate_session_id(self, userid: str) -> str:
        """生成会话ID"""
        ts = int(time.time() * 1000)
        raw = f"{userid}_{ts}"
        import hashlib
        return hashlib.md5(raw.encode()).hexdigest()[:16]

    def _get_date_range(self, period: str) -> tuple:
        """获取日期范围"""
        now = datetime.now()
        end_date = now
        if period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == "year":
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0)
        else:  # day
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start_date, end_date


# ==========================================
# 便捷函数
# ==========================================

def get_or_create_session(userid: str, direction: str = "inbound") -> SessionRecord:
    """便捷函数：获取或创建会话"""
    mgr = UnifiedSessionManager()
    return mgr.get_or_create_session(userid, direction)


def get_session_stats(period: str = "day") -> Dict:
    """便捷函数：获取统计"""
    mgr = UnifiedSessionManager()
    return mgr.get_stats(period)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行统一会话管理自测"""
    import tempfile
    print("=" * 60)
    print("统一会话管理 — 自测模式")
    print("=" * 60)

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_db = f.name

    try:
        mgr = UnifiedSessionManager(db_path=temp_db)

        # 测试 1: 创建入站会话
        print("\n[测试 1] 创建入站会话")
        session = mgr.create_session("user_123", "inbound", {"source": "wechat"})
        assert session.session_id is not None
        assert session.direction == "inbound"
        print(f"  会话ID: {session.session_id}")
        print("✅ 创建入站会话通过")

        # 测试 2: 获取或创建（恢复）
        print("\n[测试 2] 获取或创建（恢复活跃会话）")
        session2 = mgr.get_or_create_session("user_123", "inbound")
        assert session2.session_id == session.session_id
        print(f"  恢复会话: {session2.session_id}")
        print("✅ 获取或创建通过")

        # 测试 3: 创建外呼会话
        print("\n[测试 3] 创建外呼会话")
        outbound = mgr.create_outbound_session("13800138000", "预约确认")
        assert outbound.direction == "outbound"
        assert outbound.context.get("script") == "预约确认"
        print(f"  外呼会话: {outbound.session_id}")
        print("✅ 创建外呼会话通过")

        # 测试 4: 更新上下文
        print("\n[测试 4] 更新上下文")
        mgr.update_context(session.session_id, {"person": "张三", "intent": "query_weather"})
        updated = mgr.get_session(session.session_id)
        assert updated.context.get("person") == "张三"
        assert updated.context.get("intent") == "query_weather"
        print(f"  上下文: {updated.context}")
        print("✅ 更新上下文通过")

        # 测试 5: 更新状态
        print("\n[测试 5] 更新状态")
        mgr.update_status(session.session_id, "waiting")
        updated = mgr.get_session(session.session_id)
        assert updated.status == "waiting"
        print("✅ 更新状态通过")

        # 测试 6: 结束会话
        print("\n[测试 6] 结束会话")
        mgr.end_session(session.session_id, "completed")
        updated = mgr.get_session(session.session_id)
        assert updated.status == "completed"
        print("✅ 结束会话通过")

        # 测试 7: 统计
        print("\n[测试 7] 统计")
        stats = mgr.get_stats("day")
        print(f"  统计: {stats}")
        assert stats["total"] >= 2
        assert stats["inbound"] >= 1
        assert stats["outbound"] >= 1
        print("✅ 统计通过")

        # 测试 8: 按方向查询
        print("\n[测试 8] 按方向查询")
        inbound_sessions = mgr.get_sessions_by_direction("inbound")
        outbound_sessions = mgr.get_sessions_by_direction("outbound")
        print(f"  入站: {len(inbound_sessions)}, 出站: {len(outbound_sessions)}")
        assert len(inbound_sessions) >= 1
        assert len(outbound_sessions) >= 1
        print("✅ 按方向查询通过")

        print(f"\n{'='*60}")
        print("所有自测通过 ✓")
        print("=" * 60)

    finally:
        try:
            os.unlink(temp_db)
        except OSError:
            pass


if __name__ == "__main__":
    run_self_test()
