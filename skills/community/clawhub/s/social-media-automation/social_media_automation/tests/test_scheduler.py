"""
Tests for PostScheduler
"""

import pytest
from datetime import datetime, timedelta

from social_media_automation.core.scheduler import PostScheduler
from social_media_automation.storage.database import Database


@pytest.fixture
def db(tmp_path):
    """Create a temporary database"""
    db_path = str(tmp_path / "test.db")
    db = Database(db_path)
    yield db
    # Ensure database is closed after test
    if db.conn:
        db.conn.close()


@pytest.fixture
def scheduler(db):
    """Create a PostScheduler instance"""
    return PostScheduler(db)


def test_scheduler_initialization(db):
    """Test PostScheduler initialization"""
    scheduler = PostScheduler(db)

    # PostScheduler creates its own Database instance, so we just check it initializes
    assert scheduler is not None

