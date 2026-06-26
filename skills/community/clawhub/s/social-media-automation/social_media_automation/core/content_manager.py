"""
Content management module for social media automation
"""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class MediaAttachment(BaseModel):
    """Media attachment model"""

    path: str
    media_type: str  # image, video, gif
    size: int = Field(..., ge=0)
    alt_text: str | None = None
    caption: str | None = None

    @field_validator("media_type")
    @classmethod
    def validate_media_type(cls, v: str) -> str:
        """Validate media type"""
        valid_types = ["image", "video", "gif"]
        if v not in valid_types:
            raise ValueError(f"Invalid media type. Must be one of: {valid_types}")
        return v

    @field_validator("path")
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Validate that file exists"""
        if not Path(v).exists():
            raise ValueError(f"Media file not found: {v}")
        return v


class Draft(BaseModel):
    """Draft post model"""

    id: int | None = None
    platform: str
    content: str
    media_attachments: list[MediaAttachment] = Field(default_factory=list)
    status: str = "draft"
    created_at: str
    updated_at: str
    scheduled_at: str | None = None

    @field_validator("platform")
    @classmethod
    def validate_platform(cls, v: str) -> str:
        """Validate platform"""
        valid_platforms = ["x", "twitter", "bluesky", "linkedin", "instagram"]
        if v.lower() not in valid_platforms:
            raise ValueError(f"Invalid platform. Must be one of: {valid_platforms}")
        return v.lower()

    def get_character_count(self) -> int:
        """Get character count for the platform"""
        return len(self.content)

    def exceeds_limit(self, platform: str) -> bool:
        """Check if content exceeds platform limit"""
        limits = {
            "x": 280,
            "twitter": 280,
            "bluesky": 300,
            "linkedin": 3000,
            "instagram": 2200,
        }
        limit = limits.get(platform, 280)
        return self.get_character_count() > limit

    def format_for_platform(self, platform: str) -> str:
        """Format content for specific platform"""
        # Platform-specific formatting rules
        formatted = self.content

        if platform in ["x", "twitter"]:
            # Twitter/X: Convert mentions to handle format
            import re

            formatted = re.sub(r"@(\w+)", r"@\1", formatted)

        elif platform == "linkedin":
            # LinkedIn: Allow longer content, add line breaks
            if len(formatted) > 2000:
                formatted = formatted[:2000] + "..."

        return formatted


class PlatformLimits(BaseModel):
    """Platform-specific limits"""

    max_characters: int
    max_media_count: int
    allowed_media_types: list[str]
    max_image_size_mb: float = 5.0
    max_video_size_mb: float = 512.0


class ContentManager:
    """Content management system"""

    PLATFORM_LIMITS = {
        "x": PlatformLimits(
            max_characters=280,
            max_media_count=4,
            allowed_media_types=["image", "video", "gif"],
            max_image_size_mb=5.0,
            max_video_size_mb=512.0,
        ),
        "twitter": PlatformLimits(
            max_characters=280,
            max_media_count=4,
            allowed_media_types=["image", "video", "gif"],
            max_image_size_mb=5.0,
            max_video_size_mb=512.0,
        ),
        "bluesky": PlatformLimits(
            max_characters=300,
            max_media_count=4,
            allowed_media_types=["image", "video"],
            max_image_size_mb=5.0,
            max_video_size_mb=512.0,
        ),
        "linkedin": PlatformLimits(
            max_characters=3000,
            max_media_count=9,
            allowed_media_types=["image", "video", "document"],
            max_image_size_mb=5.0,
            max_video_size_mb=512.0,
        ),
        "instagram": PlatformLimits(
            max_characters=2200,
            max_media_count=10,
            allowed_media_types=["image", "video"],
            max_image_size_mb=5.0,
            max_video_size_mb=512.0,
        ),
    }

    def __init__(self, db: Any) -> None:
        """Initialize content manager"""
        self.db = db

    def create_draft(
        self,
        platform: str,
        content: str,
        media_paths: list[str] | None = None,
        scheduled_at: str | None = None,
    ) -> int:
        """Create a new draft"""
        # Validate platform
        if platform not in self.PLATFORM_LIMITS:
            raise ValueError(f"Unsupported platform: {platform}")

        # Validate content
        draft = Draft(
            platform=platform,
            content=content,
            media_attachments=[],
            status="draft",
            created_at=self._get_timestamp(),
            updated_at=self._get_timestamp(),
            scheduled_at=scheduled_at,
        )

        # Check character limit
        if draft.exceeds_limit(platform):
            limit = self.PLATFORM_LIMITS[platform].max_characters
            raise ValueError(
                f"Content exceeds {platform} character limit ({limit} characters)"
            )

        # Validate media attachments
        if media_paths:
            for media_path in media_paths:
                media = self._validate_media(media_path, platform)
                draft.media_attachments.append(media)

            # Check media count limit
            media_limit = self.PLATFORM_LIMITS[platform].max_media_count
            if len(draft.media_attachments) > media_limit:
                raise ValueError(f"Too many media files. Max: {media_limit}")

        # Save to database
        import json

        post_id = self.db.save_post(
            platform=platform,
            content=content,
            status="draft",
            scheduled_at=scheduled_at,
        )

        # Save media attachments
        if draft.media_attachments:
            self._save_media_attachments(post_id, draft.media_attachments)

        return post_id

    def list_drafts(
        self, platform: str | None = None, limit: int = 20
    ) -> list[dict[str, Any]]:
        """List all drafts, optionally filtered by platform"""
        import sqlite3

        cursor = self.db.conn.cursor()

        if platform:
            cursor.execute(
                """
                SELECT * FROM posts
                WHERE status = 'draft' AND platform = ?
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (platform, limit),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM posts
                WHERE status = 'draft'
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (limit,),
            )

        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_draft(self, draft_id: int) -> dict[str, Any] | None:
        """Get a specific draft"""
        draft_data = self.db.get_post(draft_id)

        if not draft_data or draft_data["status"] != "draft":
            return None

        # Load media attachments
        draft_data["media_attachments"] = self._load_media_attachments(draft_id)

        return draft_data

    def update_draft(
        self,
        draft_id: int,
        content: str | None = None,
        media_paths: list[str] | None = None,
    ) -> bool:
        """Update a draft"""
        import sqlite3

        cursor = self.db.conn.cursor()

        # Get current draft
        draft_data = self.db.get_post(draft_id)
        if not draft_data or draft_data["status"] != "draft":
            return False

        platform = draft_data["platform"]

        # Update content if provided
        if content:
            # Validate character limit
            temp_draft = Draft(
                platform=platform,
                content=content,
                media_attachments=[],
                status="draft",
                created_at=draft_data["created_at"],
                updated_at=self._get_timestamp(),
            )

            if temp_draft.exceeds_limit(platform):
                limit = self.PLATFORM_LIMITS[platform].max_characters
                raise ValueError(
                    f"Content exceeds {platform} character limit ({limit} characters)"
                )

            cursor.execute(
                """
                UPDATE posts
                SET content = ?, updated_at = ?
                WHERE id = ?
            """,
                (content, self._get_timestamp(), draft_id),
            )

        # Update media if provided
        if media_paths is not None:
            # Clear existing media
            cursor.execute(
                """
                DELETE FROM media_attachments WHERE post_id = ?
            """,
                (draft_id,),
            )

            # Add new media
            for media_path in media_paths:
                media = self._validate_media(media_path, platform)
                self._save_media_attachments(draft_id, [media])

        self.db.conn.commit()
        return True

    def delete_draft(self, draft_id: int) -> bool:
        """Delete a draft"""
        import sqlite3

        cursor = self.db.conn.cursor()

        # Get draft
        draft_data = self.db.get_post(draft_id)
        if not draft_data or draft_data["status"] != "draft":
            return False

        # Delete media attachments
        cursor.execute(
            """
            DELETE FROM media_attachments WHERE post_id = ?
        """,
            (draft_id,),
        )

        # Delete draft
        cursor.execute(
            """
            DELETE FROM posts WHERE id = ?
        """,
            (draft_id,),
        )

        self.db.conn.commit()
        return True

    def _validate_media(self, media_path: str, platform: str) -> MediaAttachment:
        """Validate media attachment"""
        path = Path(media_path)

        if not path.exists():
            raise ValueError(f"Media file not found: {media_path}")

        # Get file size
        size = path.stat().st_size

        # Determine media type
        ext = path.suffix.lower()
        if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            media_type = "gif" if ext == ".gif" else "image"
        elif ext in [".mp4", ".mov", ".avi"]:
            media_type = "video"
        else:
            raise ValueError(f"Unsupported media format: {ext}")

        # Check platform limits
        limits = self.PLATFORM_LIMITS.get(platform)
        if not limits:
            raise ValueError(f"Unsupported platform: {platform}")

        if media_type not in limits.allowed_media_types:
            raise ValueError(
                f"{platform} does not support {media_type} attachments"
            )

        # Check size
        max_size_mb = (
            limits.max_image_size_mb if media_type == "image" else limits.max_video_size_mb
        )
        max_size_bytes = max_size_mb * 1024 * 1024

        if size > max_size_bytes:
            raise ValueError(
                f"Media file too large ({size / 1024 / 1024:.1f}MB). Max: {max_size_mb}MB"
            )

        return MediaAttachment(path=str(path), media_type=media_type, size=size)

    def _save_media_attachments(self, post_id: int, media_attachments: list[MediaAttachment]) -> None:
        """Save media attachments to database"""
        import json

        import sqlite3

        cursor = self.db.conn.cursor()

        for media in media_attachments:
            cursor.execute(
                """
                INSERT INTO media_attachments (post_id, path, media_type, size, alt_text, caption)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    post_id,
                    media.path,
                    media.media_type,
                    media.size,
                    media.alt_text,
                    media.caption,
                ),
            )

        self.db.conn.commit()

    def _load_media_attachments(self, post_id: int) -> list[dict[str, Any]]:
        """Load media attachments from database"""
        import sqlite3

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT path, media_type, size, alt_text, caption
            FROM media_attachments
            WHERE post_id = ?
        """,
            (post_id,),
        )

        rows = cursor.fetchall()
        return [
            {
                "path": row[0],
                "media_type": row[1],
                "size": row[2],
                "alt_text": row[3],
                "caption": row[4],
            }
            for row in rows
        ]

    def _row_to_dict(self, row: tuple) -> dict[str, Any]:
        """Convert database row to dictionary"""
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

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime

        return datetime.now().isoformat()
