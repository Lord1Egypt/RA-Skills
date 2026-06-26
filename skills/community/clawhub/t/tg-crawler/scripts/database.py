"""
数据库模块 - SQLite 异步存储，管理消息和媒体记录
"""
import os
import json
import logging
import aiosqlite

logger = logging.getLogger(__name__)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msg_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    chat_title TEXT,
    chat_username TEXT,
    sender_id INTEGER,
    sender_username TEXT,
    sender_name TEXT,
    text TEXT,
    media_type TEXT,
    media_path TEXT,
    msg_date TIMESTAMP,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    matched_keywords TEXT,
    UNIQUE(chat_id, msg_id)
);

CREATE INDEX IF NOT EXISTS idx_messages_date ON messages(msg_date);
CREATE INDEX IF NOT EXISTS idx_messages_chat ON messages(chat_id);
CREATE INDEX IF NOT EXISTS idx_messages_keywords ON messages(matched_keywords);
CREATE INDEX IF NOT EXISTS idx_messages_collected_at ON messages(collected_at);

CREATE TABLE IF NOT EXISTS channel_progress (
    chat_identifier TEXT PRIMARY KEY,
    chat_title TEXT,
    last_msg_id INTEGER,
    last_msg_date TIMESTAMP,
    status TEXT DEFAULT 'done',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS media_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msg_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    media_type TEXT,
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(chat_id, msg_id)
);

CREATE INDEX IF NOT EXISTS idx_media_files_created ON media_files(created_at);
"""


class Database:
    """异步 SQLite 数据库操作"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: aiosqlite.Connection | None = None

    async def init(self):
        """初始化数据库连接和表结构"""
        os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row
        await self.conn.executescript(SCHEMA_SQL)
        await self.conn.commit()
        logger.info(f"数据库已初始化: {self.db_path}")

    async def close(self):
        """关闭数据库连接"""
        if self.conn:
            await self.conn.close()
            logger.info("数据库连接已关闭")

    async def record_media(self, msg_id: int, chat_id: int, file_path: str, media_type: str | None = None, file_size: int | None = None):
        """记录媒体文件信息（用于后续清理追踪）
        
        ⚠️ 仅在没有 save_message 时独立调用（如手动补录媒体）。
        通常 save_message 会在同一事务中自动写入 media_files。
        """
        await self.conn.execute(
            """INSERT OR REPLACE INTO media_files (msg_id, chat_id, file_path, media_type, file_size)
               VALUES (?, ?, ?, ?, ?)""",
            (msg_id, chat_id, file_path, media_type, file_size),
        )
        await self.conn.commit()

    # ═══════════════════════════════════════════════════════════
    # 数据保留策略 (Retention)
    # ═══════════════════════════════════════════════════════════

    async def retain_messages(self, retention_days: int) -> tuple[int, list[str]]:
        """
        删除超过保留天数的消息，同时返回待删除的媒体文件路径。

        Args:
            retention_days: 保留天数，0 或负数表示不清理

        Returns:
            (deleted_count, media_paths_to_remove)
        """
        if retention_days <= 0:
            return 0, []

        # 先查出待删除消息关联的媒体文件路径
        rows = await self.conn.execute_fetchall(
            """SELECT media_path FROM messages
               WHERE media_path IS NOT NULL
                 AND collected_at < datetime('now', ?)""",
            (f'-{retention_days} days',),
        )
        media_paths = [r["media_path"] for r in rows if r["media_path"]]

        # 清理 media_files 表
        await self.conn.execute(
            """DELETE FROM media_files WHERE msg_id IN (
                   SELECT msg_id FROM messages
                   WHERE collected_at < datetime('now', ?)
               )""",
            (f'-{retention_days} days',),
        )

        # 删除过期消息
        cursor = await self.conn.execute(
            "SELECT COUNT(*) as c FROM messages WHERE collected_at < datetime('now', ?)",
            (f'-{retention_days} days',),
        )
        count_row = await cursor.fetchone()
        expired_before = count_row["c"] if count_row else 0

        if expired_before == 0:
            return 0, []

        await self.conn.execute(
            "DELETE FROM messages WHERE collected_at < datetime('now', ?)",
            (f'-{retention_days} days',),
        )
        await self.conn.commit()

        logger.info(f"🧹 数据保留: 清理 {expired_before} 条过期消息 (>{retention_days}天)")
        return expired_before, media_paths

    async def retain_channel_progress(self, retention_days: int) -> int:
        """
        清理超过保留天数的断点续传记录（status='done' 且久未更新）

        Returns:
            清理的记录数
        """
        if retention_days <= 0:
            return 0

        cursor = await self.conn.execute(
            "SELECT COUNT(*) as c FROM channel_progress WHERE updated_at < datetime('now', ?)",
            (f'-{retention_days} days',),
        )
        count_row = await cursor.fetchone()
        count = count_row["c"] if count_row else 0

        if count == 0:
            return 0

        await self.conn.execute(
            "DELETE FROM channel_progress WHERE updated_at < datetime('now', ?)",
            (f'-{retention_days} days',),
        )
        await self.conn.commit()

        if count > 0:
            logger.info(f"🧹 断点记录: 清理 {count} 条过期记录 (>{retention_days}天)")
        return count

    async def vacuum(self):
        """回收数据库空间 (VACUUM)。小库自动跳过。"""
        try:
            size_before = await self.get_db_size()
            if size_before < 10 * 1024 * 1024:  # <10MB 跳过
                logger.debug(f"数据库 {size_before/1024:.0f}KB，跳过 VACUUM")
                return
            logger.info("🔄 数据库 VACUUM 开始...")
            await self.conn.execute("VACUUM")
            size_after = await self.get_db_size()
            logger.info(f"✅ 数据库 VACUUM 完成 ({size_before/1024/1024:.1f}MB → {size_after/1024/1024:.1f}MB)")
        except Exception as e:
            logger.warning(f"VACUUM 失败 (可忽略): {e}")

    async def get_db_size(self) -> int:
        """获取数据库文件大小 (bytes)"""
        import os
        try:
            return os.path.getsize(self.db_path)
        except OSError:
            return 0

    async def get_table_counts(self) -> dict:
        """获取各表行数统计"""
        result = {}
        for table in ("messages", "channel_progress", "media_files"):
            cursor = await self.conn.execute(f"SELECT COUNT(*) as c FROM {table}")
            row = await cursor.fetchone()
            result[table] = row["c"] if row else 0
        return result

    async def message_exists(self, chat_id: int, msg_id: int) -> bool:
        """检查消息是否已存在（去重）"""
        cursor = await self.conn.execute(
            "SELECT 1 FROM messages WHERE chat_id = ? AND msg_id = ?",
            (chat_id, msg_id),
        )
        row = await cursor.fetchone()
        return row is not None

    async def save_message(
        self,
        msg_id: int,
        chat_id: int,
        chat_title: str | None = None,
        chat_username: str | None = None,
        sender_id: int | None = None,
        sender_username: str | None = None,
        sender_name: str | None = None,
        text: str | None = None,
        media_type: str | None = None,
        media_path: str | None = None,
        msg_date: str | None = None,
        matched_keywords: list[str] | None = None,
    ) -> bool:
        """
        保存一条消息到数据库

        使用 INSERT OR IGNORE 保证原子去重，避免 check-then-insert 竞态。

        Returns:
            True 表示新插入，False 表示已存在（跳过）
        """
        keywords_json = json.dumps(matched_keywords, ensure_ascii=False) if matched_keywords else None

        cursor = await self.conn.execute(
            """INSERT OR IGNORE INTO messages
               (msg_id, chat_id, chat_title, chat_username,
                sender_id, sender_username, sender_name,
                text, media_type, media_path,
                msg_date, matched_keywords)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (msg_id, chat_id, chat_title, chat_username,
             sender_id, sender_username, sender_name,
             text, media_type, media_path,
             msg_date, keywords_json),
        )

        inserted = cursor.rowcount > 0

        # 同事务记录 media_files（保证 retention cleanup 可追踪）
        if inserted and media_path:
            await self.conn.execute(
                """INSERT OR REPLACE INTO media_files (msg_id, chat_id, file_path, media_type)
                   VALUES (?, ?, ?, ?)""",
                (msg_id, chat_id, media_path, media_type),
            )

        await self.conn.commit()
        return inserted

    async def get_stats(self) -> dict:
        """获取采集统计信息"""
        total = await self.conn.execute_fetchall("SELECT COUNT(*) as c FROM messages")
        by_chat = await self.conn.execute_fetchall(
            "SELECT chat_title, chat_username, COUNT(*) as c FROM messages GROUP BY chat_id ORDER BY c DESC"
        )
        return {
            "total_messages": total[0][0] if total else 0,
            "by_chat": [{"title": r[0], "username": r[1], "count": r[2]} for r in by_chat],
        }

    # ═══════════════════════════════════════════════════════════
    # 断点续传：频道回溯进度管理
    # ═══════════════════════════════════════════════════════════

    async def get_progress(self, chat_identifier: str) -> dict | None:
        """获取单个频道的回溯进度"""
        row = await self.conn.execute_fetchall(
            "SELECT * FROM channel_progress WHERE chat_identifier = ?",
            (chat_identifier,),
        )
        if row:
            r = row[0]
            return {
                "chat_identifier": r["chat_identifier"],
                "chat_title": r["chat_title"],
                "last_msg_id": r["last_msg_id"],
                "last_msg_date": r["last_msg_date"],
                "status": r["status"],
                "updated_at": r["updated_at"],
            }
        return None

    async def get_all_progress(self) -> dict[str, dict]:
        """获取所有频道回溯进度 (用于判断哪些频道已完成)"""
        rows = await self.conn.execute_fetchall(
            "SELECT * FROM channel_progress"
        )
        result = {}
        for r in rows:
            result[r["chat_identifier"]] = {
                "chat_identifier": r["chat_identifier"],
                "chat_title": r["chat_title"],
                "last_msg_id": r["last_msg_id"],
                "last_msg_date": r["last_msg_date"],
                "status": r["status"],
                "updated_at": r["updated_at"],
            }
        return result

    async def set_progress(
        self,
        chat_identifier: str,
        chat_title: str | None = None,
        last_msg_id: int | None = None,
        last_msg_date: str | None = None,
        status: str = "done",
    ):
        """记录/更新频道回溯进度"""
        await self.conn.execute(
            """INSERT OR REPLACE INTO channel_progress
               (chat_identifier, chat_title, last_msg_id, last_msg_date, status, updated_at)
               VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (chat_identifier, chat_title, last_msg_id, last_msg_date, status),
        )
        await self.conn.commit()

    async def clear_progress(self, chat_identifier: str | None = None):
        """清除频道回溯进度（chat_identifier=None 时清空全部）"""
        if chat_identifier:
            await self.conn.execute(
                "DELETE FROM channel_progress WHERE chat_identifier = ?",
                (chat_identifier,),
            )
        else:
            await self.conn.execute("DELETE FROM channel_progress")
        await self.conn.commit()

    # ═══════════════════════════════════════════════════════════
    # 发送者信息异步补充（防 Flood Wait）
    # ═══════════════════════════════════════════════════════════

    async def update_sender_info(
        self,
        chat_id: int,
        msg_id: int,
        sender_username: str | None,
        sender_name: str | None,
    ):
        """
        单条更新消息的发送者信息（延迟补充用）
        """
        await self.conn.execute(
            "UPDATE messages SET sender_username = ?, sender_name = ? WHERE chat_id = ? AND msg_id = ?",
            (sender_username, sender_name, chat_id, msg_id),
        )

    async def update_senders_batch(
        self,
        cache: "SenderCache",
    ) -> int:
        """
        批量更新所有消息中 sender_id 对应的发送者信息
        从 SenderCache 中获取缓存数据
        """
        updated = 0
        all_cached = cache.get_all_cached()
        if not all_cached:
            return 0

        # 查询所有缺乏 sender 信息的消息
        rows = await self.conn.execute_fetchall(
            "SELECT id, chat_id, msg_id, sender_id FROM messages WHERE (sender_username IS NULL OR sender_name IS NULL) AND sender_id IS NOT NULL"
        )
        for r in rows:
            sid = r["sender_id"]
            if sid in all_cached:
                username, name = all_cached[sid]
                if username or name:
                    await self.conn.execute(
                        "UPDATE messages SET sender_username = ?, sender_name = ? WHERE id = ?",
                        (username, name, r["id"]),
                    )
                    updated += 1

        if updated > 0:
            await self.conn.commit()
            logger.info(f"🔄 补充发送者信息: {updated} 条消息已更新")
        return updated

    async def get_pending_count(self, identifiers: list[str]) -> int:
        """计算还有多少个频道待回溯（不在 channel_progress 中）"""
        done = await self.get_all_progress()
        return sum(1 for ident in identifiers if ident not in done)

    async def get_pending_identifiers(self, identifiers: list[str]) -> list[str]:
        """返回尚未完成回溯的频道列表"""
        done = await self.get_all_progress()
        return [ident for ident in identifiers if ident not in done]

    # ═══════════════════════════════════════════════════════════
    # 数据导出
    # ═══════════════════════════════════════════════════════════

    async def export_messages(
        self,
        output_path: str,
        format: str = "csv",
        since: str | None = None,
        until: str | None = None,
        chat_usernames: list[str] | None = None,
    ) -> int:
        """
        导出消息到文件。返回导出条数。

        Args:
            output_path: 输出文件路径
            format: csv / json / markdown
            since: 起始日期 (YYYY-MM-DD)
            until: 截止日期 (YYYY-MM-DD)
            chat_usernames: 限定频道列表
        """
        if format not in ("csv", "json", "markdown"):
            raise ValueError(f"不支持的导出格式: {format}")

        # 构建查询
        query = "SELECT * FROM messages WHERE 1=1"
        params: list = []

        if since:
            query += " AND msg_date >= ?"
            params.append(since)
        if until:
            query += " AND msg_date <= ?"
            params.append(until + " 23:59:59")
        if chat_usernames:
            placeholders = ",".join("?" for _ in chat_usernames)
            query += f" AND chat_username IN ({placeholders})"
            params.extend(chat_usernames)

        query += " ORDER BY msg_date DESC"

        rows = await self.conn.execute_fetchall(query, params)

        if not rows:
            logger.info(f"无数据可导出")
            return 0

        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

        if format == "csv":
            count = self._export_csv(rows, output_path)
        elif format == "json":
            count = self._export_json(rows, output_path)
        else:
            count = self._export_markdown(rows, output_path)

        logger.info(f"导出完成: {count} 条 → {output_path}")
        return count

    @staticmethod
    def _export_csv(rows, path: str) -> int:
        import csv
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            headers = ["id", "msg_id", "chat_id", "chat_title", "chat_username",
                       "sender_id", "sender_username", "sender_name",
                       "text", "media_type", "msg_date", "matched_keywords", "collected_at"]
            writer.writerow(headers)
            count = 0
            for r in rows:
                writer.writerow([
                    r["id"], r["msg_id"], r["chat_id"],
                    r["chat_title"], r["chat_username"],
                    r["sender_id"], r["sender_username"], r["sender_name"],
                    r["text"], r["media_type"], r["msg_date"], r["matched_keywords"], r["collected_at"]
                ])
                count += 1
        return count

    @staticmethod
    def _export_json(rows, path: str) -> int:
        count = 0
        with open(path, 'w', encoding='utf-8') as f:
            f.write('[\n')
            for i, r in enumerate(rows):
                record = {
                    "id": r["id"],
                    "msg_id": r["msg_id"],
                    "chat_id": r["chat_id"],
                    "chat_title": r["chat_title"],
                    "chat_username": r["chat_username"],
                    "sender_id": r["sender_id"],
                    "sender_username": r["sender_username"],
                    "sender_name": r["sender_name"],
                    "text": r["text"],
                    "media_type": r["media_type"],
                    "msg_date": r["msg_date"],
                    "matched_keywords": json.loads(r["matched_keywords"]) if r["matched_keywords"] else [],
                    "collected_at": r["collected_at"],
                }
                f.write(json.dumps(record, ensure_ascii=False, indent=2))
                if i < len(rows) - 1:
                    f.write(',\n')
                else:
                    f.write('\n')
                count += 1
            f.write(']\n')
        return count

    @staticmethod
    def _export_markdown(rows, path: str) -> int:
        count = 0
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# TG 爬虫消息导出\n\n")
            f.write(f"> 📅 导出时间: {rows[0]['collected_at'] or 'N/A'}\n\n")
            f.write("---\n\n")
            current_chat = None
            for r in rows:
                chat = r["chat_title"] or r["chat_username"] or "未知频道"
                if chat != current_chat:
                    current_chat = chat
                    f.write(f"## {chat}\n\n")
                date_str = r["msg_date"][:19] if r["msg_date"] else ""
                kw = json.loads(r["matched_keywords"]) if r["matched_keywords"] else []
                kw_str = f" `[{', '.join(kw)}]`" if kw else ""
                f.write(f"- **{date_str}**{kw_str}\n")
                f.write(f"  > {r['text']}\n\n")
                count += 1
        return count
