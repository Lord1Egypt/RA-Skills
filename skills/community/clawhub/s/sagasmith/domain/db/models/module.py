"""Module source metadata and scene indexes."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .common import TimestampMixin


class ModuleSource(TimestampMixin, Base):
    __tablename__ = "module_sources"
    __table_args__ = (
        UniqueConstraint("campaign_id", "name", name="uq_module_source_campaign_name"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String)
    source_path: Mapped[str] = mapped_column(String)
    checksum: Mapped[str | None] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class ModuleChapter(TimestampMixin, Base):
    __tablename__ = "module_chapters"
    __table_args__ = (
        UniqueConstraint("module_id", "chapter_key", name="uq_module_chapter_key"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    module_id: Mapped[str] = mapped_column(
        ForeignKey("module_sources.id", ondelete="CASCADE"), index=True
    )
    chapter_key: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String, default="")
    source_path: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text, default="")
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String, default="locked", index=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class SceneIndex(TimestampMixin, Base):
    __tablename__ = "scene_indexes"
    __table_args__ = (
        UniqueConstraint("chapter_id", "scene_key", name="uq_scene_index_key"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    chapter_id: Mapped[str] = mapped_column(
        ForeignKey("module_chapters.id", ondelete="CASCADE"), index=True
    )
    scene_key: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    start_line: Mapped[int] = mapped_column(Integer)
    end_line: Mapped[int] = mapped_column(Integer)
    headings: Mapped[list[str]] = mapped_column(JSON, default=list)
    keywords: Mapped[list[str]] = mapped_column(JSON, default=list)


class ModuleChunk(Base):
    """Retrieval-sized module content with an optional dense vector."""

    __tablename__ = "module_chunks"
    __table_args__ = (
        UniqueConstraint("chapter_id", "chunk_index", name="uq_module_chunk_index"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    module_id: Mapped[str] = mapped_column(
        ForeignKey("module_sources.id", ondelete="CASCADE"), index=True
    )
    chapter_id: Mapped[str] = mapped_column(
        ForeignKey("module_chapters.id", ondelete="CASCADE"), index=True
    )
    scene_id: Mapped[str | None] = mapped_column(
        ForeignKey("scene_indexes.id", ondelete="SET NULL"), index=True
    )
    embedding_model_id: Mapped[str | None] = mapped_column(
        ForeignKey("embedding_models.id", ondelete="SET NULL"), index=True
    )
    chunk_index: Mapped[int] = mapped_column(Integer)
    heading: Mapped[str] = mapped_column(String, default="", index=True)
    breadcrumb: Mapped[str] = mapped_column(Text, default="")
    start_line: Mapped[int] = mapped_column(Integer)
    end_line: Mapped[int] = mapped_column(Integer)
    char_start: Mapped[int] = mapped_column(Integer)
    char_end: Mapped[int] = mapped_column(Integer)
    page_start: Mapped[int | None] = mapped_column(Integer, index=True)
    page_end: Mapped[int | None] = mapped_column(Integer)
    chunk_type: Mapped[str] = mapped_column(String, default="narrative", index=True)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    content_hash: Mapped[str] = mapped_column(String, default="", index=True)
    chunk_text: Mapped[str] = mapped_column(Text)
    search_text: Mapped[str] = mapped_column(Text, default="")
    embedding_json: Mapped[list[float] | None] = mapped_column(JSON)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class SceneState(TimestampMixin, Base):
    __tablename__ = "scene_states"
    __table_args__ = (
        UniqueConstraint("campaign_id", "scene_id", name="uq_campaign_scene_state"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    scene_id: Mapped[str] = mapped_column(
        ForeignKey("scene_indexes.id", ondelete="CASCADE"), index=True
    )
    current_room: Mapped[str | None] = mapped_column(String)
    explored_percent: Mapped[int] = mapped_column(Integer, default=0)
    state_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    schema_version: Mapped[int] = mapped_column(Integer, default=1)
    state_version: Mapped[int] = mapped_column(Integer, default=1)
