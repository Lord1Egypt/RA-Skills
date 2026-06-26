"""
SQLite database for Resume/ATS Optimization
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class Resume(BaseModel):
    """Resume model"""

    id: int | None = None
    file_path: str
    content: str | None = None
    keywords: list[str] | None = None
    ats_score: int | None = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class JobDescription(BaseModel):
    """Job description model"""

    id: int | None = None
    file_path: str
    content: str | None = None
    keywords: list[str] | None = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Database:
    """SQLite database manager"""

    def __init__(self, db_path: str | None = None) -> None:
        """Initialize database connection"""
        if db_path is None:
            from resume_ats.config import Config

            db_path = Config.load().db_path

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self) -> None:
        """Create database tables"""
        cursor = self.conn.cursor()

        # Resumes table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,
                content TEXT,
                keywords TEXT,
                ats_score INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """
        )

        # Job descriptions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS job_descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,
                content TEXT,
                keywords TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """
        )

        self.conn.commit()

    def save_resume(
        self,
        file_path: str,
        content: str | None = None,
        keywords: list[str] | None = None,
        ats_score: int | None = None,
    ) -> int:
        """Save a resume to database"""
        cursor = self.conn.cursor()
        now = datetime.now()

        cursor.execute(
            """
            INSERT INTO resumes (file_path, content, keywords, ats_score, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                file_path,
                content,
                json.dumps(keywords) if keywords else None,
                ats_score,
                now.isoformat(),
                now.isoformat(),
            ),
        )

        self.conn.commit()
        return cursor.lastrowid

    def get_resume(self, file_path: str) -> dict[str, Any] | None:
        """Get a resume by file path"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM resumes WHERE file_path = ?", (file_path,))
        row = cursor.fetchone()

        if row:
            return {
                "id": row[0],
                "file_path": row[1],
                "content": row[2],
                "keywords": json.loads(row[3]) if row[3] else None,
                "ats_score": row[4],
                "created_at": row[5],
                "updated_at": row[6],
            }
        return None

    def save_job_description(
        self,
        file_path: str,
        content: str | None = None,
        keywords: list[str] | None = None,
    ) -> int:
        """Save a job description to database"""
        cursor = self.conn.cursor()
        now = datetime.now()

        cursor.execute(
            """
            INSERT INTO job_descriptions (file_path, content, keywords, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                file_path,
                content,
                json.dumps(keywords) if keywords else None,
                now.isoformat(),
                now.isoformat(),
            ),
        )

        self.conn.commit()
        return cursor.lastrowid

    def get_job_description(self, file_path: str) -> dict[str, Any] | None:
        """Get a job description by file path"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM job_descriptions WHERE file_path = ?", (file_path,))
        row = cursor.fetchone()

        if row:
            return {
                "id": row[0],
                "file_path": row[1],
                "content": row[2],
                "keywords": json.loads(row[3]) if row[3] else None,
                "created_at": row[4],
                "updated_at": row[5],
            }
        return None

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
