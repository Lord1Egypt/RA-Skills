"""
SQLite database for social media automation
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class Post(BaseModel):
    """Post model"""

    id: int | None = None
    platform: str
    content: str
    post_id: str | None = None
    scheduled_at: datetime | None = None
    status: str = "draft"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Database:
    """SQLite database manager"""

    def __init__(self, db_path: str | None = None) -> None:
        """Initialize database connection"""
        if db_path is None:
            from social_media_automation.config import Config

            db_path = Config.load().db_path

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self) -> None:
        """Create database tables"""
        cursor = self.conn.cursor()

        # Posts table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                content TEXT NOT NULL,
                post_id TEXT,
                scheduled_at TEXT,
                status TEXT DEFAULT 'draft',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """
        )

        # Media attachments table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS media_attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                path TEXT NOT NULL,
                media_type TEXT NOT NULL,
                size INTEGER NOT NULL,
                alt_text TEXT,
                caption TEXT,
                FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
            )
        """
        )

        self.conn.commit()

    def save_post(
        self,
        platform: str,
        content: str,
        post_id: str | None = None,
        scheduled_at: datetime | None = None,
        status: str = "draft",
    ) -> int:
        """Save a post to database"""
        cursor = self.conn.cursor()
        now = datetime.now()

        cursor.execute(
            """
            INSERT INTO posts (platform, content, post_id, scheduled_at, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                platform,
                content,
                post_id,
                scheduled_at.isoformat() if scheduled_at else None,
                status,
                now.isoformat(),
                now.isoformat(),
            ),
        )

        self.conn.commit()
        return cursor.lastrowid

    def get_post(self, post_id: int) -> dict[str, Any] | None:
        """Get a post by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        row = cursor.fetchone()

        if row:
            return {
                "id": row[0],
                "platform": row[1],
                "content": row[2],
                "post_id": row[3],
                "scheduled_at": row[4],
                "status": row[5],
                "created_at": row[6],
                "updated_at": row[7],
            }
        return None

    def get_scheduled_posts(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get all scheduled posts"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM posts
            WHERE status = 'scheduled'
            ORDER BY scheduled_at ASC
            LIMIT ?
        """,
            (limit,),
        )

        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "platform": row[1],
                "content": row[2],
                "post_id": row[3],
                "scheduled_at": row[4],
                "status": row[5],
                "created_at": row[6],
                "updated_at": row[7],
            }
            for row in rows
        ]

    def update_post_status(self, post_id: int, status: str) -> bool:
        """Update post status"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE posts SET status = ?, updated_at = ?
            WHERE id = ?
        """,
            (status, datetime.now().isoformat(), post_id),
        )

        self.conn.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
