"""Store imported module chapter content outside snapshots.

Revision ID: 20260619_04
Revises: 20260619_03
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260619_04"
down_revision = "20260619_03"
branch_labels = None
depends_on = None


def upgrade() -> None:
    columns = {
        column["name"]
        for column in sa.inspect(op.get_bind()).get_columns("module_chapters")
    }
    if "content" not in columns:
        op.add_column(
            "module_chapters",
            sa.Column("content", sa.Text(), nullable=False, server_default=""),
        )


def downgrade() -> None:
    columns = {
        column["name"]
        for column in sa.inspect(op.get_bind()).get_columns("module_chapters")
    }
    if "content" in columns:
        with op.batch_alter_table("module_chapters") as batch:
            batch.drop_column("content")
