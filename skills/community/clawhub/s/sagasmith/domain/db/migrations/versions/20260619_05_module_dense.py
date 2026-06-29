"""Add campaign-scoped dense retrieval chunks for modules.

Revision ID: 20260619_05
Revises: 20260619_04
"""

from __future__ import annotations

from alembic import op

from ... import models  # noqa: F401
from ...database import Base

revision = "20260619_05"
down_revision = "20260619_04"
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.tables["module_chunks"].create(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    Base.metadata.tables["module_chunks"].drop(bind=op.get_bind(), checkfirst=True)
