"""
Template storage for social media automation
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class Template(BaseModel):
    """Template model"""

    id: int | None = None
    name: str
    content: str
    platform: str
    variables: list[str] = Field(default_factory=list)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class TemplateStore:
    """SQLite database manager for templates"""

    def __init__(self, db_path: str | None = None) -> None:
        """Initialize template store connection"""
        if db_path is None:
            from social_media_automation.config import Config

            db_path = Config.load().db_path

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self) -> None:
        """Create template tables"""
        cursor = self.conn.cursor()

        # Templates table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                platform TEXT NOT NULL,
                variables TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """
        )

        self.conn.commit()

    def save_template(
        self,
        name: str,
        content: str,
        platform: str,
        variables: list[str] | None = None,
    ) -> int:
        """Save a template"""
        cursor = self.conn.cursor()
        now = datetime.now()

        # Extract variables from content ({{variable}} format)
        if variables is None:
            variables = self._extract_variables(content)

        cursor.execute(
            """
            INSERT INTO templates (name, content, platform, variables, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                name,
                content,
                platform,
                json.dumps(variables),
                now.isoformat(),
                now.isoformat(),
            ),
        )

        self.conn.commit()
        return cursor.lastrowid

    def get_template(self, template_id: int) -> dict[str, Any] | None:
        """Get a template by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM templates WHERE id = ?", (template_id,))
        row = cursor.fetchone()

        if row:
            return {
                "id": row[0],
                "name": row[1],
                "content": row[2],
                "platform": row[3],
                "variables": json.loads(row[4]) if row[4] else [],
                "created_at": row[5],
                "updated_at": row[6],
            }
        return None

    def get_template_by_name(self, name: str) -> dict[str, Any] | None:
        """Get a template by name"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM templates WHERE name = ?", (name,))
        row = cursor.fetchone()

        if row:
            return {
                "id": row[0],
                "name": row[1],
                "content": row[2],
                "platform": row[3],
                "variables": json.loads(row[4]) if row[4] else [],
                "created_at": row[5],
                "updated_at": row[6],
            }
        return None

    def list_templates(self, platform: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        """List all templates"""
        cursor = self.conn.cursor()

        if platform:
            cursor.execute(
                """
                SELECT * FROM templates
                WHERE platform = ?
                ORDER BY updated_at DESC
                LIMIT ?
            """,
                (platform, limit),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM templates
                ORDER BY updated_at DESC
                LIMIT ?
            """,
                (limit,),
            )

        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "content": row[2],
                "platform": row[3],
                "variables": json.loads(row[4]) if row[4] else [],
                "created_at": row[5],
                "updated_at": row[6],
            }
            for row in rows
        ]

    def update_template(
        self,
        template_id: int,
        name: str | None = None,
        content: str | None = None,
        platform: str | None = None,
        variables: list[str] | None = None,
    ) -> bool:
        """Update a template"""
        cursor = self.conn.cursor()

        # Get current values
        current = self.get_template(template_id)
        if not current:
            return False

        # Update fields
        name = name or current["name"]
        content = content or current["content"]
        platform = platform or current["platform"]

        # Update variables if content changed
        if content != current["content"] and variables is None:
            variables = self._extract_variables(content)
        elif variables is None:
            variables = current["variables"]

        cursor.execute(
            """
            UPDATE templates
            SET name = ?, content = ?, platform = ?, variables = ?, updated_at = ?
            WHERE id = ?
        """,
            (
                name,
                content,
                platform,
                json.dumps(variables),
                datetime.now().isoformat(),
                template_id,
            ),
        )

        self.conn.commit()
        return cursor.rowcount > 0

    def delete_template(self, template_id: int) -> bool:
        """Delete a template"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM templates WHERE id = ?", (template_id,))

        self.conn.commit()
        return cursor.rowcount > 0

    def apply_template(self, template_id: int, variables: dict[str, str]) -> str:
        """Apply variables to template"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")

        content = template["content"]

        # Replace variables
        for var_name, var_value in variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            content = content.replace(placeholder, var_value)

        return content

    def _extract_variables(self, content: str) -> list[str]:
        """Extract variables from content ({{variable}} format)"""
        import re

        pattern = r"\{\{([^}]+)\}\}"
        matches = re.findall(pattern, content)
        return list(set([m.strip() for m in matches]))

    def close(self) -> None:
        """Close database connection"""
        self.conn.close()
