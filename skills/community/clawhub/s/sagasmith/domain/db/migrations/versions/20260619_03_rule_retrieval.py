"""Add hierarchical rule retrieval and BGE-M3 dense index support.

Revision ID: 20260619_03
Revises: 20260619_02
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

from ... import models  # noqa: F401
from ...database import Base

revision = "20260619_03"
down_revision = "20260619_02"
branch_labels = None
depends_on = None


def _columns(table: str) -> set[str]:
    return {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table)}


def _indexes(table: str) -> set[str]:
    return {index["name"] for index in sa.inspect(op.get_bind()).get_indexes(table)}


def _add_column(table: str, column: sa.Column) -> None:
    if column.name not in _columns(table):
        op.add_column(table, column)


def _add_index(table: str, name: str, columns: list[str]) -> None:
    if name not in _indexes(table):
        op.create_index(name, table, columns, unique=False)


def upgrade() -> None:
    bind = op.get_bind()

    # The original baseline migration creates current metadata on fresh databases.
    # checkfirst keeps this migration valid for both fresh and existing v2 databases.
    for table_name in (
        "rule_sets",
        "rule_publications",
        "embedding_models",
        "rule_sections",
        "campaign_rule_profiles",
        "campaign_rule_publications",
    ):
        Base.metadata.tables[table_name].create(bind=bind, checkfirst=True)

    for column in (
        sa.Column("rule_set_id", sa.String(), nullable=True),
        sa.Column("publication_id", sa.String(), nullable=True),
        sa.Column("source_type", sa.String(), nullable=False, server_default="markdown"),
        sa.Column("locale", sa.String(), nullable=False, server_default="en"),
    ):
        _add_column("rule_sources", column)
    _add_index("rule_sources", "ix_rule_sources_rule_set_id", ["rule_set_id"])
    _add_index("rule_sources", "ix_rule_sources_publication_id", ["publication_id"])
    _add_index("rule_sources", "ix_rule_sources_source_type", ["source_type"])
    _add_index("rule_sources", "ix_rule_sources_locale", ["locale"])

    for column in (
        sa.Column("section_id", sa.String(), nullable=True),
        sa.Column("embedding_model_id", sa.String(), nullable=True),
        sa.Column("breadcrumb", sa.Text(), nullable=False, server_default=""),
        sa.Column("token_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("content_hash", sa.String(), nullable=False, server_default=""),
        sa.Column("search_text", sa.Text(), nullable=False, server_default=""),
    ):
        _add_column("rule_chunks", column)
    _add_index("rule_chunks", "ix_rule_chunks_section_id", ["section_id"])
    _add_index("rule_chunks", "ix_rule_chunks_embedding_model_id", ["embedding_model_id"])
    _add_index("rule_chunks", "ix_rule_chunks_content_hash", ["content_hash"])

    for column in (
        sa.Column("rule_set_id", sa.String(), nullable=True),
        sa.Column("publication_id", sa.String(), nullable=True),
        sa.Column("section_id", sa.String(), nullable=True),
        sa.Column("supersedes_entry_id", sa.String(), nullable=True),
        sa.Column("aliases", sa.JSON(), nullable=False, server_default="[]"),
    ):
        _add_column("compendium_entries", column)
    _add_index("compendium_entries", "ix_compendium_entries_rule_set_id", ["rule_set_id"])
    _add_index(
        "compendium_entries", "ix_compendium_entries_publication_id", ["publication_id"]
    )
    _add_index("compendium_entries", "ix_compendium_entries_section_id", ["section_id"])
    _add_index(
        "compendium_entries", "ix_compendium_entries_supersedes_entry_id", ["supersedes_entry_id"]
    )

    if bind.dialect.name == "sqlite":
        op.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS rule_chunks_fts USING fts5(
                chunk_id UNINDEXED,
                heading,
                breadcrumb,
                chunk_text,
                tokenize='unicode61'
            )
            """
        )
        op.execute("DELETE FROM rule_chunks_fts")
        op.execute(
            """
            INSERT INTO rule_chunks_fts(chunk_id, heading, breadcrumb, chunk_text)
            SELECT id, COALESCE(heading, ''), COALESCE(breadcrumb, ''), chunk_text
            FROM rule_chunks
            """
        )
        op.execute(
            """
            CREATE TRIGGER IF NOT EXISTS rule_chunks_fts_insert AFTER INSERT ON rule_chunks BEGIN
                INSERT INTO rule_chunks_fts(chunk_id, heading, breadcrumb, chunk_text)
                VALUES (new.id, COALESCE(new.heading, ''), COALESCE(new.breadcrumb, ''), new.chunk_text);
            END
            """
        )
        op.execute(
            """
            CREATE TRIGGER IF NOT EXISTS rule_chunks_fts_delete AFTER DELETE ON rule_chunks BEGIN
                DELETE FROM rule_chunks_fts WHERE chunk_id = old.id;
            END
            """
        )
        op.execute(
            """
            CREATE TRIGGER IF NOT EXISTS rule_chunks_fts_update
            AFTER UPDATE OF heading, breadcrumb, chunk_text ON rule_chunks BEGIN
                DELETE FROM rule_chunks_fts WHERE chunk_id = old.id;
                INSERT INTO rule_chunks_fts(chunk_id, heading, breadcrumb, chunk_text)
                VALUES (new.id, COALESCE(new.heading, ''), COALESCE(new.breadcrumb, ''), new.chunk_text);
            END
            """
        )
    elif bind.dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")
        op.execute(
            "ALTER TABLE rule_chunks ADD COLUMN IF NOT EXISTS embedding_vector vector(1024)"
        )
        op.execute(
            "ALTER TABLE rule_chunks ADD COLUMN IF NOT EXISTS search_vector tsvector"
        )
        op.execute(
            """
            UPDATE rule_chunks SET search_vector =
              to_tsvector('simple', coalesce(heading, '') || ' ' ||
                                    coalesce(breadcrumb, '') || ' ' || chunk_text)
            """
        )
        op.execute(
            "CREATE INDEX IF NOT EXISTS idx_rule_chunks_search_vector "
            "ON rule_chunks USING gin(search_vector)"
        )
        op.execute(
            "CREATE INDEX IF NOT EXISTS idx_rule_chunks_embedding_hnsw "
            "ON rule_chunks USING hnsw (embedding_vector vector_cosine_ops)"
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        op.execute("DROP TRIGGER IF EXISTS rule_chunks_fts_update")
        op.execute("DROP TRIGGER IF EXISTS rule_chunks_fts_delete")
        op.execute("DROP TRIGGER IF EXISTS rule_chunks_fts_insert")
        op.execute("DROP TABLE IF EXISTS rule_chunks_fts")
    elif bind.dialect.name == "postgresql":
        op.execute("DROP INDEX IF EXISTS idx_rule_chunks_embedding_hnsw")
        op.execute("DROP INDEX IF EXISTS idx_rule_chunks_search_vector")
        op.execute("ALTER TABLE rule_chunks DROP COLUMN IF EXISTS search_vector")
        op.execute("ALTER TABLE rule_chunks DROP COLUMN IF EXISTS embedding_vector")

    for table_name in (
        "campaign_rule_publications",
        "campaign_rule_profiles",
        "rule_sections",
        "embedding_models",
        "rule_publications",
        "rule_sets",
    ):
        Base.metadata.tables[table_name].drop(bind=bind, checkfirst=True)
