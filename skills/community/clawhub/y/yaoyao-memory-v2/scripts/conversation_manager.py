#!/usr/bin/env python3
"""
conversation_manager.py - 对话管理器
管理多轮对话历史和上下文窗口
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional


MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CONVERSATION_DB = MEMORY_DIR / "conversations.db"


@dataclass
class Message:
    """消息"""
    role: str  # user/assistant/system
    content: str
    timestamp: str
    tokens: int = 0


@dataclass
class Conversation:
    """对话会话"""
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int
    total_tokens: int


class ConversationManager:
    """对话管理器"""
    
    def __init__(self):
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        CONVERSATION_DB.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(CONVERSATION_DB)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                role TEXT,
                content TEXT,
                timestamp TEXT,
                tokens INTEGER DEFAULT 0,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        conn.commit()
        conn.close()
    
    def create_conversation(self, title: str = "新对话") -> str:
        """创建新对话"""
        import uuid
        conv_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(CONVERSATION_DB)
        conn.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (conv_id, title, now, now)
        )
        conn.commit()
        conn.close()
        
        return conv_id
    
    def add_message(self, conv_id: str, role: str, content: str, tokens: int = 0):
        """添加消息"""
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(CONVERSATION_DB)
        conn.execute(
            "INSERT INTO messages (conversation_id, role, content, timestamp, tokens) VALUES (?, ?, ?, ?, ?)",
            (conv_id, role, content, now, tokens)
        )
        conn.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (now, conv_id)
        )
        conn.commit()
        conn.close()
    
    def get_conversation(self, conv_id: str, limit: int = 50) -> List[Message]:
        """获取对话消息"""
        conn = sqlite3.connect(CONVERSATION_DB)
        cursor = conn.execute(
            """SELECT role, content, timestamp, tokens FROM messages 
               WHERE conversation_id = ? ORDER BY timestamp DESC LIMIT ?""",
            (conv_id, limit)
        )
        messages = [
            Message(role=r, content=c, timestamp=t, tokens=tk)
            for r, c, t, tk in cursor.fetchall()
        ]
        conn.close()
        return list(reversed(messages))
    
    def get_conversations(self, limit: int = 20) -> List[Conversation]:
        """获取所有对话"""
        conn = sqlite3.connect(CONVERSATION_DB)
        cursor = conn.execute(
            """SELECT id, title, created_at, updated_at, 
                      (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) as msg_count,
                      (SELECT SUM(tokens) FROM messages WHERE conversation_id = c.id) as total_tokens
               FROM conversations c ORDER BY updated_at DESC LIMIT ?""",
            (limit,)
        )
        conversations = [
            Conversation(id=i, title=t, created_at=ca, updated_at=ua, message_count=mc, total_tokens=tt or 0)
            for i, t, ca, ua, mc, tt in cursor.fetchall()
        ]
        conn.close()
        return conversations
    
    def get_context_window(self, conv_id: str, max_tokens: int = 4000) -> str:
        """获取上下文字符串（限制token数）"""
        messages = self.get_conversation(conv_id, limit=100)
        
        context = []
        total_tokens = 0
        
        for msg in reversed(messages):
            # 粗略估算：中文约2字符=1token，英文约4字符=1token
            tokens = len(msg.content) // 2
            if total_tokens + tokens > max_tokens:
                break
            context.append(f"{msg.role}: {msg.content}")
            total_tokens += tokens
        
        return "\n".join(reversed(context))
    
    def delete_conversation(self, conv_id: str):
        """删除对话"""
        conn = sqlite3.connect(CONVERSATION_DB)
        conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
        conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
        conn.commit()
        conn.close()
    
    def summarize_old_conversations(self, days: int = 7) -> int:
        """总结旧对话（超过指定天数的）"""
        threshold = (datetime.now() - timedelta(days=days)).isoformat()
        
        conn = sqlite3.connect(CONVERSATION_DB)
        cursor = conn.execute(
            "SELECT id, title FROM conversations WHERE updated_at < ?",
            (threshold,)
        )
        old_convs = cursor.fetchall()
        conn.close()
        
        # 这里可以调用LLM来总结，但暂时只是返回数量
        return len(old_convs)


def main():
    import sys
    
    manager = ConversationManager()
    
    if len(sys.argv) < 2:
        print("""🦞 对话管理器
    
用法:
    conversation_manager.py list              # 列出所有对话
    conversation_manager.py new [标题]       # 创建新对话
    conversation_manager.py show <id>         # 显示对话内容
    conversation_manager.py context <id>      # 获取上下文字符串
    conversation_manager.py delete <id>       # 删除对话
    conversation_manager.py cleanup [天数]     # 清理旧对话""")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        convs = manager.get_conversations()
        print(f"\n📋 最近 {len(convs)} 个对话:\n")
        for c in convs:
            print(f"  [{c.id}] {c.title}")
            print(f"       消息: {c.message_count} | Token: {c.total_tokens}")
            print(f"       更新: {c.updated_at[:19]}")
            print()
    
    elif cmd == "new":
        title = sys.argv[2] if len(sys.argv) > 2 else "新对话"
        conv_id = manager.create_conversation(title)
        print(f"✅ 创建对话: [{conv_id}] {title}")
    
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("❌ 请提供对话ID")
            return
        conv_id = sys.argv[2]
        messages = manager.get_conversation(conv_id)
        print(f"\n📖 对话 [{conv_id}] ({len(messages)} 条消息):\n")
        for m in messages:
            print(f"  {m.role}: {m.content[:100]}...")
            print()
    
    elif cmd == "context":
        if len(sys.argv) < 3:
            print("❌ 请提供对话ID")
            return
        conv_id = sys.argv[2]
        context = manager.get_context_window(conv_id)
        print(f"\n📝 上下文字符串 (约{len(context)//2} token):\n")
        print(context[:500] + "..." if len(context) > 500 else context)
    
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("❌ 请提供对话ID")
            return
        conv_id = sys.argv[2]
        manager.delete_conversation(conv_id)
        print(f"✅ 已删除对话 [{conv_id}]")
    
    elif cmd == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        count = manager.summarize_old_conversations(days)
        print(f"📦 超过 {days} 天的对话: {count} 个")


if __name__ == "__main__":
    main()
