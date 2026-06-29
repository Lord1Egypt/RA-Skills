"""Add page provenance and semantic type to module chunks.

Revision ID: 20260620_06
Revises: 20260619_05
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260620_06"
down_revision = "20260619_05"
branch_labels = None
depends_on = None


def _columns() -> set[str]:
    return {
        column["name"]
        for column in sa.inspect(op.get_bind()).get_columns("module_chunks")
    }


def upgrade() -> None:
    columns = _columns()
    additions = (
        sa.Column("page_start", sa.Integer(), nullable=True),
        sa.Column("page_end", sa.Integer(), nullable=True),
        sa.Column(
            "chunk_type",
            sa.String(),
            nullable=False,
            server_default="narrative",
        ),
    )
    for column in additions:
        if column.name not in columns:
            op.add_column("module_chunks", column)
    indexes = {
        index["name"]
        for index in sa.inspect(op.get_bind()).get_indexes("module_chunks")
    }
    if "ix_module_chunks_page_start" not in indexes:
        op.create_index(
            "ix_module_chunks_page_start", "module_chunks", ["page_start"]
        )
    if "ix_module_chunks_chunk_type" not in indexes:
        op.create_index(
            "ix_module_chunks_chunk_type", "module_chunks", ["chunk_type"]
        )


def downgrade() -> None:
    indexes = {
        index["name"]
        for index in sa.inspect(op.get_bind()).get_indexes("module_chunks")
    }
    for name in ("ix_module_chunks_chunk_type", "ix_module_chunks_page_start"):
        if name in indexes:
            op.drop_index(name, table_name="module_chunks")
    with op.batch_alter_table("module_chunks") as batch:
        for name in ("chunk_type", "page_end", "page_start"):
            if name in _columns():
                batch.drop_column(name)
