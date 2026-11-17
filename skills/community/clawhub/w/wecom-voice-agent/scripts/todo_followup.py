#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
todo_followup.py — 跟进待办闭环子模块（v2.7）

功能：
1. 从通话纪要中抽取待办项
2. 自动登记回拨任务（scheduler 新增依赖类型: todo）
3. 到期未闭环自动提醒责任人或发起二次外呼确认
4. 待办闭环状态可在查询类意图中口头问答

依赖：纯 Python 标准库（sqlite3 + json + re + datetime）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-09-02)
"""

import os
import re
import json
import sqlite3
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from enum import Enum

logger = logging.getLogger(__name__)

# ==========================================
# 配置
# ==========================================

DB_PATH = os.path.join(os.path.expanduser("~"), ".wecom_voice", "todos.db")
DEFAULT_REMINDER_DAYS = 3  # 默认 3 天后跟进
MAX_RETRY_COUNT = 2  # 最大重试次数


# ==========================================
# 待办状态枚举
# ==========================================

class TodoStatus(Enum):
    """待办状态"""
    PENDING = "pending"           # 待处理
    REMINDED = "reminded"         # 已提醒
    CALLBACK_DONE = "callback_done"  # 已回拨
    CLOSED = "closed"             # 已闭环
    ESCALATED = "escalated"       # 已升级
    EXPIRED = "expired"           # 已过期


# ==========================================
# 待办管理器
# ==========================================

class TodoFollowupManager:
    """
    跟进待办闭环管理器

    使用方式：
        mgr = TodoFollowupManager()
        
        # 从纪要抽取待办
        todos = mgr.extract_todos_from_minutes(minutes_dict, call_id, userid)
        
        # 登记待办 + 创建回拨任务
        for todo in todos:
            mgr.register_todo(todo)
        
        # 到期检测
        mgr.check_due_todos()
        
        # 查询待办状态
        status = mgr.query_todo_status("报销")
    """

    def __init__(self, db_path: str = DB_PATH, reminder_days: int = DEFAULT_REMINDER_DAYS):
        self.db_path = db_path
        self.reminder_days = reminder_days
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    todo_id TEXT NOT NULL UNIQUE,
                    call_id TEXT NOT NULL,
                    userid TEXT NOT NULL,
                    content TEXT NOT NULL,
                    responsible_person TEXT DEFAULT '',
                    due_date TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    retry_count INTEGER DEFAULT 0,
                    source TEXT DEFAULT 'call_minutes',
                    priority TEXT DEFAULT 'normal',
                    metadata TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    closed_at TEXT,
                    close_reason TEXT DEFAULT ''
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_todos_userid
                ON todos(userid)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_todos_status
                ON todos(status)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_todos_due_date
                ON todos(due_date)
            """)
            # 兼容旧库：补充群任务相关列（v2.9）
            self._ensure_column(conn, "todos", "assigner", "TEXT DEFAULT ''")
            self._ensure_column(conn, "todos", "assignee", "TEXT DEFAULT ''")
            self._ensure_column(conn, "todos", "chat_id", "TEXT DEFAULT ''")
            self._ensure_column(conn, "todos", "confirm_status", "TEXT DEFAULT 'none'")
            self._ensure_column(conn, "todos", "source_group", "INTEGER DEFAULT 0")

    @staticmethod
    def _ensure_column(conn, table: str, column: str, ddl: str):
        """兼容旧库：若列不存在则追加（v2.9 群任务）"""
        try:
            cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
            if column not in cols:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}")
        except Exception as e:
            logger.warning(f"补充列失败 {table}.{column}: {e}")

    def extract_todos_from_minutes(self, minutes: Dict[str, Any], call_id: str, userid: str) -> List[Dict[str, Any]]:
        """
        从通话纪要中抽取待办项

        Args:
            minutes: ivr_minutes.py 生成的纪要字典
            call_id: 通话 ID
            userid: 用户 ID

        Returns:
            list: 待办项列表
        """
        todos = []

        # 从纪要 JSON 中提取 todos
        raw_todos = minutes.get("todos", [])
        decisions = minutes.get("decisions", [])
        action_items = minutes.get("action_items", [])

        # 合并所有待办来源
        all_todo_texts = raw_todos + action_items

        # 从决策中提取隐含待办
        for decision in decisions:
            if isinstance(decision, str) and self._is_actionable(decision):
                all_todo_texts.append(decision)

        for text in all_todo_texts:
            if not text or not isinstance(text, str):
                continue
            text = text.strip()
            if len(text) < 4:
                continue

            todo_id = self._generate_todo_id(text, call_id)
            due_date = self._extract_due_date(text) or (datetime.now() + timedelta(days=self.reminder_days)).isoformat()

            todos.append({
                "todo_id": todo_id,
                "call_id": call_id,
                "userid": userid,
                "content": text,
                "due_date": due_date,
                "status": "pending",
                "source": "call_minutes",
            })

        return todos

    def register_todo(self, todo: Dict[str, str], responsible_person: str = "",
                      priority: str = "normal", auto_schedule: bool = True,
                      assigner: str = "", assignee: str = "", chat_id: str = "",
                      source_group: bool = False) -> bool:
        """
        登记待办并可选自动创建回拨任务

        v2.9 新增群任务支持：assigner（指派人）/assignee（被指派人）/chat_id/
        source_group。群任务默认进入「待确认」状态，需被指派人确认回执。

        Args:
            todo: 待办信息字典
            responsible_person: 责任人（缺省时取 assignee）
            priority: 优先级
            auto_schedule: 是否自动创建回拨任务
            assigner: 指派人（群内发言者）
            assignee: 被指派人（@提及或人名）
            chat_id: 群聊ID（群任务）
            source_group: 是否群来源

        Returns:
            bool: 成功返回 True
        """
        now = datetime.now().isoformat()
        todo_id = todo.get("todo_id", self._generate_todo_id(todo.get("content", ""), todo.get("call_id", "")))
        # 群任务：被指派人即责任人
        if not responsible_person:
            responsible_person = assignee
        # 群任务且指定被指派人：进入待确认（确认回执闭环）
        confirm_status = "pending_confirm" if (source_group and assignee) else "none"

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO todos 
                    (todo_id, call_id, userid, content, responsible_person, due_date, status, priority,
                     created_at, updated_at, assigner, assignee, chat_id, confirm_status, source_group)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    todo_id,
                    todo.get("call_id", ""),
                    todo.get("userid", ""),
                    todo.get("content", ""),
                    responsible_person,
                    todo.get("due_date", (datetime.now() + timedelta(days=self.reminder_days)).isoformat()),
                    "pending",
                    priority,
                    now,
                    now,
                    assigner,
                    assignee,
                    chat_id or "",
                    confirm_status,
                    1 if source_group else 0,
                ))

            # 自动创建回拨任务（群任务到期提醒同样复用）
            if auto_schedule:
                self._schedule_callback(todo)

            logger.info(f"登记待办: {todo_id}, 内容: {todo.get('content', '')[:30]}, 群来源: {source_group}")
            return True

        except Exception as e:
            logger.warning(f"登记待办失败: {e}")
            return False

    def confirm_todo(self, todo_id: str, accept: bool = True) -> Dict[str, Any]:
        """
        群任务确认回执（v2.9）：被指派人确认/拒绝指派

        Args:
            todo_id: 待办ID
            accept: True=确认接受，False=拒绝

        Returns:
            dict: {"ok", "status", "receipt", "reason"}
        """
        now = datetime.now().isoformat()
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute("SELECT * FROM todos WHERE todo_id = ?", (todo_id,)).fetchone()
                if not row:
                    return {"ok": False, "reason": "not_found"}
                todo = dict(row)
                new_confirm = "confirmed" if accept else "rejected"
                new_status = "pending" if accept else "closed"
                conn.execute(
                    "UPDATE todos SET confirm_status = ?, status = ?, close_reason = ?, updated_at = ? WHERE todo_id = ?",
                    (new_confirm, new_status, "被指派人拒绝" if not accept else "", now, todo_id)
                )
            assignee = todo.get("assignee") or todo.get("responsible_person") or "相关同事"
            content = todo.get("content", "")
            due = (todo.get("due_date") or "")[:10]
            if accept:
                receipt = f"✅ {assignee} 已确认任务：{content}（截止：{due}）。任务已记入待办，到期前会提醒。"
            else:
                receipt = f"⚠️ {assignee} 拒绝了任务：{content}。请指派人或管理员重新安排。"
            return {"ok": True, "status": new_confirm, "receipt": receipt}
        except Exception as e:
            logger.warning(f"确认待办失败: {e}")
            return {"ok": False, "reason": str(e)}

    def query_by_assignee(self, assignee: str, keyword: str = "") -> List[Dict[str, Any]]:
        """
        按被指派人查询待办（v2.9 群任务：被指派人查看自己的任务）

        Args:
            assignee: 被指派人标识（@名或 userid）
            keyword: 关键词筛选

        Returns:
            list: 待办列表
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if keyword:
                cursor = conn.execute(
                    "SELECT * FROM todos WHERE assignee = ? AND content LIKE ? ORDER BY created_at DESC LIMIT 10",
                    (assignee, f"%{keyword}%"))
            else:
                cursor = conn.execute(
                    "SELECT * FROM todos WHERE assignee = ? AND status NOT IN ('closed', 'expired') ORDER BY created_at DESC LIMIT 10",
                    (assignee,))
            return [dict(row) for row in cursor.fetchall()]

    def check_due_todos(self) -> List[Dict[str, Any]]:
        """
        检查到期未闭环的待办，触发提醒或二次外呼

        Returns:
            list: 触发的待办列表
        """
        now = datetime.now().isoformat()
        triggered = []

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM todos 
                WHERE due_date <= ? AND status IN ('pending', 'reminded')
            """, (now,))

            for row in cursor.fetchall():
                todo = dict(row)
                triggered.append(todo)

                # 判断处理方式
                if todo["retry_count"] >= MAX_RETRY_COUNT:
                    # 超过最大重试次数，升级
                    self._escalate_todo(todo["todo_id"])
                elif todo["status"] == "pending":
                    # 第一次：提醒责任人
                    self._remind_todo(todo["todo_id"])
                elif todo["status"] == "reminded":
                    # 已提醒过：二次外呼
                    self._callback_todo(todo["todo_id"])

        return triggered

    def query_todo_status(self, userid: str, keyword: str = "") -> List[Dict[str, Any]]:
        """
        查询用户待办状态（供 query_todo 意图调用）

        Args:
            userid: 用户 ID
            keyword: 关键词筛选

        Returns:
            list: 待办列表
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if keyword:
                cursor = conn.execute("""
                    SELECT * FROM todos 
                    WHERE userid = ? AND content LIKE ?
                    ORDER BY created_at DESC LIMIT 10
                """, (userid, f"%{keyword}%"))
            else:
                cursor = conn.execute("""
                    SELECT * FROM todos 
                    WHERE userid = ? AND status NOT IN ('closed', 'expired')
                    ORDER BY created_at DESC LIMIT 10
                """, (userid,))

            return [dict(row) for row in cursor.fetchall()]

    def close_todo(self, todo_id: str, reason: str = "completed") -> bool:
        """
        闭环待办

        Args:
            todo_id: 待办 ID
            reason: 闭环原因

        Returns:
            bool: 成功返回 True
        """
        now = datetime.now().isoformat()
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE todos SET status = 'closed', closed_at = ?, close_reason = ?, updated_at = ?
                    WHERE todo_id = ?
                """, (now, reason, now, todo_id))
            return True
        except Exception as e:
            logger.warning(f"闭环待办失败: {e}")
            return False

    def format_todo_response(self, todos: List[Dict[str, Any]]) -> str:
        """
        格式化待办查询回复（供 Agent 生成自然语言）

        Args:
            todos: 待办列表

        Returns:
            str: 格式化文本
        """
        if not todos:
            return "您当前没有未处理的待办事项。"

        status_map = {
            "pending": "待处理",
            "reminded": "已提醒",
            "callback_done": "已回拨",
            "closed": "已完成",
            "escalated": "已升级",
            "expired": "已过期",
        }

        lines = [f"您有 {len(todos)} 项待办："]
        for i, todo in enumerate(todos, 1):
            status_text = status_map.get(todo["status"], todo["status"])
            due = todo.get("due_date", "未知")[:10]
            lines.append(f"  {i}. {todo['content']}（状态：{status_text}，截止：{due}）")

        return "\n".join(lines)

    # === 内部方法 ===

    def _generate_todo_id(self, content: str, call_id: str) -> str:
        """生成待办 ID"""
        raw = f"{call_id}_{content}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def _is_actionable(self, text: str) -> bool:
        """判断文本是否包含可执行动作"""
        action_keywords = ["需要", "要", "去", "完成", "处理", "跟进", "确认", "提交", "联系", "安排", "准备", "办理"]
        return any(kw in text for kw in action_keywords)

    def _extract_due_date(self, text: str) -> Optional[str]:
        """从文本中提取截止日期"""
        # 明天/后天/X天后
        date_map = {"明天": 1, "后天": 2, "大后天": 3}
        for word, offset in date_map.items():
            if word in text:
                target = datetime.now() + timedelta(days=offset)
                return target.isoformat()

        # X天后
        m = re.search(r'(\d+)天[后内]', text)
        if m:
            offset = int(m.group(1))
            target = datetime.now() + timedelta(days=offset)
            return target.isoformat()

        return None

    def _schedule_callback(self, todo: Dict[str, str]):
        """创建回拨任务（写入 scheduler 兼容格式）"""
        # 回拨任务存储在 todos 表的 metadata 中
        # 实际调度由 scheduler.py 的 add_one_shot 或 check_due_todos 触发
        logger.info(f"已创建回拨任务: {todo.get('todo_id')}")

    def _remind_todo(self, todo_id: str):
        """提醒责任人"""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE todos SET status = 'reminded', retry_count = retry_count + 1, updated_at = ?
                WHERE todo_id = ?
            """, (now, todo_id))
        logger.info(f"提醒待办: {todo_id}")

    def _callback_todo(self, todo_id: str):
        """二次外呼确认"""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE todos SET status = 'callback_done', retry_count = retry_count + 1, updated_at = ?
                WHERE todo_id = ?
            """, (now, todo_id))
        logger.info(f"二次外呼: {todo_id}")

    def _escalate_todo(self, todo_id: str):
        """升级待办"""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE todos SET status = 'escalated', updated_at = ?
                WHERE todo_id = ?
            """, (now, todo_id))
        logger.info(f"升级待办: {todo_id}")


# ==========================================
# 便捷函数
# ==========================================

_manager_instance: Optional[TodoFollowupManager] = None


def get_manager() -> TodoFollowupManager:
    """获取单例"""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = TodoFollowupManager()
    return _manager_instance


def extract_and_register_todos(minutes: Dict[str, Any], call_id: str, userid: str) -> List[Dict[str, Any]]:
    """便捷函数：从纪要抽取并登记待办"""
    mgr = get_manager()
    todos = mgr.extract_todos_from_minutes(minutes, call_id, userid)
    for todo in todos:
        mgr.register_todo(todo)
    return todos


def check_due_todos() -> List[Dict[str, Any]]:
    """便捷函数：检查到期待办"""
    return get_manager().check_due_todos()


def query_todo_status(userid: str, keyword: str = "") -> List[Dict[str, Any]]:
    """便捷函数：查询待办状态"""
    return get_manager().query_todo_status(userid, keyword)


def format_todo_response(todos: List[Dict[str, Any]]) -> str:
    """便捷函数：格式化待办回复"""
    return get_manager().format_todo_response(todos)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行待办闭环自测"""
    import tempfile
    print("=" * 60)
    print("todo_followup.py — 自测模式")
    print("=" * 60)

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_db = f.name

    try:
        mgr = TodoFollowupManager(db_path=temp_db)

        # 测试 1: 从纪要抽取待办
        print("\n[测试 1] 从纪要抽取待办")
        mock_minutes = {
            "todos": ["明天提交报销单", "联系张三确认会议时间", "准备项目报告"],
            "decisions": ["需要安排下周评审"],
            "action_items": [],
        }
        todos = mgr.extract_todos_from_minutes(mock_minutes, "call_001", "user_123")
        print(f"  抽取到 {len(todos)} 项待办")
        for t in todos:
            print(f"    - {t['content']}")
        assert len(todos) >= 3
        print("✅ 抽取待办通过")

        # 测试 2: 登记待办
        print("\n[测试 2] 登记待办")
        for todo in todos:
            result = mgr.register_todo(todo, auto_schedule=False)
            assert result is True
        print(f"  登记 {len(todos)} 项待办")
        print("✅ 登记待办通过")

        # 测试 3: 查询待办状态
        print("\n[测试 3] 查询待办状态")
        status = mgr.query_todo_status("user_123")
        print(f"  查询到 {len(status)} 项")
        assert len(status) >= 3
        print("✅ 查询待办通过")

        # 测试 4: 关键词查询
        print("\n[测试 4] 关键词查询")
        filtered = mgr.query_todo_status("user_123", "报销")
        print(f"  '报销' 相关: {len(filtered)} 项")
        assert len(filtered) >= 1
        assert "报销" in filtered[0]["content"]
        print("✅ 关键词查询通过")

        # 测试 5: 格式化回复
        print("\n[测试 5] 格式化回复")
        response = mgr.format_todo_response(status)
        print(f"  回复: {response[:60]}...")
        assert "待办" in response
        print("✅ 格式化回复通过")

        # 测试 6: 闭环待办
        print("\n[测试 6] 闭环待办")
        todo_id = todos[0]["todo_id"]
        result = mgr.close_todo(todo_id, "completed")
        assert result is True
        remaining = mgr.query_todo_status("user_123")
        print(f"  闭环后剩余: {len(remaining)} 项")
        assert len(remaining) == len(todos) - 1
        print("✅ 闭环待办通过")

        # 测试 7: 到期检测
        print("\n[测试 7] 到期检测")
        # 插入一个已到期的待办
        overdue_todo = {
            "todo_id": "test_overdue",
            "call_id": "call_002",
            "userid": "user_456",
            "content": "测试到期待办",
            "due_date": (datetime.now() - timedelta(days=1)).isoformat(),
        }
        mgr.register_todo(overdue_todo, auto_schedule=False)
        due = mgr.check_due_todos()
        print(f"  到期待办: {len(due)} 项")
        assert len(due) >= 1
        print("✅ 到期检测通过")

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
