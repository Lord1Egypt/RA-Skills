"""Hierarchical rule corpus, structured compendium, and embedding metadata."""

from __future__ import annotations

from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .common import TimestampMixin


class RuleSet(TimestampMixin, Base):
    """One isolated game-system release, such as D&D 5e SRD 5.2.1."""

    __tablename__ = "rule_sets"
    __table_args__ = (
        UniqueConstraint(
            "game_system", "edition", "release", "locale", name="uq_rule_set_release"
        ),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    game_system: Mapped[str] = mapped_column(String, index=True)
    edition: Mapped[str] = mapped_column(String, index=True)
    release: Mapped[str] = mapped_column(String, index=True)
    locale: Mapped[str] = mapped_column(String, default="en", index=True)
    status: Mapped[str] = mapped_column(String, default="active", index=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class RulePublication(TimestampMixin, Base):
    """A core book, supplement, errata set, or homebrew publication."""

    __tablename__ = "rule_publications"
    __table_args__ = (
        UniqueConstraint("rule_set_id", "slug", name="uq_rule_publication_slug"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    rule_set_id: Mapped[str] = mapped_column(
        ForeignKey("rule_sets.id", ondelete="CASCADE"), index=True
    )
    parent_publication_id: Mapped[str | None] = mapped_column(
        ForeignKey("rule_publications.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String, index=True)
    slug: Mapped[str] = mapped_column(String)
    publication_type: Mapped[str] = mapped_column(String, default="core", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    license: Mapped[str | None] = mapped_column(String)
    effective_date: Mapped[str | None] = mapped_column(String)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class EmbeddingModel(TimestampMixin, Base):
    """Embedding provenance for reproducible dense indexes."""

    __tablename__ = "embedding_models"
    __table_args__ = (
        UniqueConstraint("provider", "model_name", "dimensions", name="uq_embedding_model"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    provider: Mapped[str] = mapped_column(String, default="sentence-transformers")
    model_name: Mapped[str] = mapped_column(String, index=True)
    dimensions: Mapped[int] = mapped_column(Integer)
    distance_metric: Mapped[str] = mapped_column(String, default="cosine")
    content_template_version: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)


class RuleSource(TimestampMixin, Base):
    """A physical source document within a publication."""

    __tablename__ = "rule_sources"
    __table_args__ = (UniqueConstraint("source_path", name="uq_rule_source_path"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    rule_set_id: Mapped[str | None] = mapped_column(
        ForeignKey("rule_sets.id", ondelete="CASCADE"), index=True
    )
    publication_id: Mapped[str | None] = mapped_column(
        ForeignKey("rule_publications.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String)
    source_path: Mapped[str] = mapped_column(String)
    source_type: Mapped[str] = mapped_column(String, default="markdown", index=True)
    system_version: Mapped[str | None] = mapped_column(String)
    locale: Mapped[str] = mapped_column(String, default="en", index=True)
    checksum: Mapped[str | None] = mapped_column(String)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class RuleSection(Base):
    """A node in the publication heading tree."""

    __tablename__ = "rule_sections"
    __table_args__ = (
        UniqueConstraint("source_id", "path", name="uq_rule_section_path"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_id: Mapped[str] = mapped_column(
        ForeignKey("rule_sources.id", ondelete="CASCADE"), index=True
    )
    publication_id: Mapped[str] = mapped_column(
        ForeignKey("rule_publications.id", ondelete="CASCADE"), index=True
    )
    parent_id: Mapped[str | None] = mapped_column(
        ForeignKey("rule_sections.id", ondelete="CASCADE"), index=True
    )
    section_type: Mapped[str] = mapped_column(String, default="section", index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    slug: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    heading_path: Mapped[list[str]] = mapped_column(JSON, default=list)
    depth: Mapped[int] = mapped_column(Integer)
    order_index: Mapped[int] = mapped_column(Integer)
    start_line: Mapped[int | None] = mapped_column(Integer)
    end_line: Mapped[int | None] = mapped_column(Integer)
    char_start: Mapped[int | None] = mapped_column(Integer)
    char_end: Mapped[int | None] = mapped_column(Integer)


class RuleChunk(Base):
    """A retrieval-sized leaf with stable source positions and optional dense vector."""

    __tablename__ = "rule_chunks"
    __table_args__ = (
        UniqueConstraint("source_id", "chunk_index", name="uq_rule_chunk_index"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    source_id: Mapped[str] = mapped_column(
        ForeignKey("rule_sources.id", ondelete="CASCADE"), index=True
    )
    section_id: Mapped[str | None] = mapped_column(
        ForeignKey("rule_sections.id", ondelete="CASCADE"), index=True
    )
    embedding_model_id: Mapped[str | None] = mapped_column(
        ForeignKey("embedding_models.id", ondelete="SET NULL"), index=True
    )
    chunk_index: Mapped[int] = mapped_column(Integer)
    heading: Mapped[str | None] = mapped_column(String, index=True)
    breadcrumb: Mapped[str] = mapped_column(Text, default="")
    start_line: Mapped[int | None] = mapped_column(Integer)
    end_line: Mapped[int | None] = mapped_column(Integer)
    char_start: Mapped[int | None] = mapped_column(Integer)
    char_end: Mapped[int | None] = mapped_column(Integer)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    content_hash: Mapped[str] = mapped_column(String, default="", index=True)
    chunk_text: Mapped[str] = mapped_column(Text)
    search_text: Mapped[str] = mapped_column(Text, default="")
    embedding_json: Mapped[list[float] | None] = mapped_column(JSON)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class CompendiumEntry(TimestampMixin, Base):
    """A structured spell, item, monster, condition, feat, or other named rule."""

    __tablename__ = "compendium_entries"
    __table_args__ = (
        UniqueConstraint("entry_type", "name", "system_version", name="uq_compendium_entry"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    rule_set_id: Mapped[str | None] = mapped_column(
        ForeignKey("rule_sets.id", ondelete="CASCADE"), index=True
    )
    publication_id: Mapped[str | None] = mapped_column(
        ForeignKey("rule_publications.id", ondelete="CASCADE"), index=True
    )
    section_id: Mapped[str | None] = mapped_column(
        ForeignKey("rule_sections.id", ondelete="SET NULL"), index=True
    )
    supersedes_entry_id: Mapped[str | None] = mapped_column(
        ForeignKey("compendium_entries.id", ondelete="SET NULL"), index=True
    )
    entry_type: Mapped[str] = mapped_column(String, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list)
    data_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    source: Mapped[str | None] = mapped_column(String)
    system_version: Mapped[str | None] = mapped_column(String)


class CampaignRuleProfile(TimestampMixin, Base):
    """The isolated rule release selected by one campaign."""

    __tablename__ = "campaign_rule_profiles"
    __table_args__ = (UniqueConstraint("campaign_id", name="uq_campaign_rule_profile"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    rule_set_id: Mapped[str] = mapped_column(
        ForeignKey("rule_sets.id", ondelete="RESTRICT"), index=True
    )
    locale: Mapped[str] = mapped_column(String, default="en")


class CampaignRulePublication(Base):
    """A publication enabled for a campaign profile."""

    __tablename__ = "campaign_rule_publications"
    __table_args__ = (
        UniqueConstraint("profile_id", "publication_id", name="uq_campaign_rule_publication"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    profile_id: Mapped[str] = mapped_column(
        ForeignKey("campaign_rule_profiles.id", ondelete="CASCADE"), index=True
    )
    publication_id: Mapped[str] = mapped_column(
        ForeignKey("rule_publications.id", ondelete="CASCADE"), index=True
    )
    priority: Mapped[int] = mapped_column(Integer, default=0)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
