"""
Tests for ContentManager
"""

import pytest
from datetime import datetime

from social_media_automation.core.content_manager import ContentManager
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
def content_manager(db):
    """Create a ContentManager instance"""
    return ContentManager(db)


def test_content_manager_initialization(db):
    """Test ContentManager initialization"""
    manager = ContentManager(db)

    assert manager.db == db
