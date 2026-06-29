"""Create the dnd-dm-skill-aligned v2 schema.

Revision ID: 20260619_01
Revises:
"""

from __future__ import annotations

from alembic import op

from ... import models  # noqa: F401
from ...database import Base

revision = "20260619_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
