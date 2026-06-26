"""聊天上下文管理器 — 基于 SQLite 存储对话历史和商品信息"""

import sqlite3
import os
import json
import logging
from datetime import datetime

logger = logging.getLogger('xianyu-monitor')


class ChatContextManager:
    def __init__(self, max_history=100, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'data', 'chat_history.db')
        self.max_history = max_history
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            item_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            chat_id TEXT
        )''')

        cursor.execute("PRAGMA table_info(messages)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'chat_id' not in columns:
            cursor.execute('ALTER TABLE messages ADD COLUMN chat_id TEXT')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_item ON messages (user_id, item_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_id ON messages (chat_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON messages (timestamp)')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_bargain_counts (
            chat_id TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            price REAL,
            description TEXT,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        conn.commit()
        conn.close()
        logger.info(f"数据库初始化完成: {self.db_path}")

    def save_item_info(self, item_id, item_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            price = float(item_data.get('soldPrice', 0))
            description = item_data.get('desc', '')
            data_json = json.dumps(item_data, ensure_ascii=False)
            now = datetime.now().isoformat()
            cursor.execute(
                """INSERT INTO items (item_id, data, price, description, last_updated)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(item_id)
                DO UPDATE SET data = ?, price = ?, description = ?, last_updated = ?""",
                (item_id, data_json, price, description, now,
                 data_json, price, description, now)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"保存商品信息出错: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_item_info(self, item_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT data FROM items WHERE item_id = ?", (item_id,))
            result = cursor.fetchone()
            return json.loads(result[0]) if result else None
        except Exception as e:
            logger.error(f"获取商品信息出错: {e}")
            return None
        finally:
            conn.close()

    def add_message_by_chat(self, chat_id, user_id, item_id, role, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO messages (user_id, item_id, role, content, timestamp, chat_id) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, item_id, role, content, datetime.now().isoformat(), chat_id)
            )
            cursor.execute(
                "SELECT id FROM messages WHERE chat_id = ? ORDER BY timestamp DESC LIMIT ?, 1",
                (chat_id, self.max_history)
            )
            oldest = cursor.fetchone()
            if oldest:
                cursor.execute("DELETE FROM messages WHERE chat_id = ? AND id < ?", (chat_id, oldest[0]))
            conn.commit()
        except Exception as e:
            logger.error(f"添加消息出错: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_context_by_chat(self, chat_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY timestamp ASC LIMIT ?",
                (chat_id, self.max_history)
            )
            messages = [{"role": role, "content": content} for role, content in cursor.fetchall()]
            bargain_count = self.get_bargain_count_by_chat(chat_id)
            if bargain_count > 0:
                messages.append({"role": "system", "content": f"议价次数: {bargain_count}"})
            return messages
        except Exception as e:
            logger.error(f"获取对话历史出错: {e}")
            return []
        finally:
            conn.close()

    def increment_bargain_count_by_chat(self, chat_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            now = datetime.now().isoformat()
            cursor.execute(
                """INSERT INTO chat_bargain_counts (chat_id, count, last_updated)
                VALUES (?, 1, ?)
                ON CONFLICT(chat_id)
                DO UPDATE SET count = count + 1, last_updated = ?""",
                (chat_id, now, now)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"增加议价次数出错: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_bargain_count_by_chat(self, chat_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT count FROM chat_bargain_counts WHERE chat_id = ?", (chat_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"获取议价次数出错: {e}")
            return 0
        finally:
            conn.close()
