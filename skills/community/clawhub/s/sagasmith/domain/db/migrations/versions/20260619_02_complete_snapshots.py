"""Add complete snapshot metadata to campaign saves.

Revision ID: 20260619_02
Revises: 20260619_01
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260619_02"
down_revision = "20260619_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("campaign_saves")}
    indexes = {index["name"] for index in inspector.get_indexes("campaign_saves")}

    # The v2 baseline migration historically used current metadata. Fresh databases
    # may therefore already contain these columns before this incremental revision.
    if "snapshot_format" not in columns:
        op.add_column(
            "campaign_saves",
            sa.Column(
                "snapshot_format",
                sa.String(),
                nullable=False,
                server_default="dnd-campaign-snapshot",
            ),
        )
    if "snapshot_hash" not in columns:
        op.add_column(
            "campaign_saves",
            sa.Column("snapshot_hash", sa.String(), nullable=False, server_default=""),
        )
    if "created_by" not in columns:
        op.add_column(
            "campaign_saves", sa.Column("created_by", sa.String(), nullable=True)
        )
    if "ix_campaign_saves_created_by" not in indexes:
        op.create_index(
            "ix_campaign_saves_created_by",
            "campaign_saves",
            ["created_by"],
            unique=False,
        )
    op.execute(sa.text("UPDATE campaign_saves SET schema_version = 2"))


def downgrade() -> None:
    with op.batch_alter_table("campaign_saves") as batch:
        batch.drop_index("ix_campaign_saves_created_by")
        batch.drop_column("created_by")
        batch.drop_column("snapshot_hash")
        batch.drop_column("snapshot_format")
