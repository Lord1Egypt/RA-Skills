"""
Tests for Database
"""

import pytest
from datetime import datetime

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


def test_database_creation(db):
    """Test database creation"""
    assert db.db_path.exists()


def test_save_post(db):
    """Test saving a post"""
    post_id = db.save_post(
        platform="x",
        content="Test content",
        status="draft",
    )

    assert post_id is not None
    assert post_id > 0


def test_get_post(db):
    """Test getting a post by ID"""
    post_id = db.save_post(
        platform="x",
        content="Test content",
        status="draft",
    )

    post = db.get_post(post_id)

    assert post is not None
    assert post["platform"] == "x"
    assert post["content"] == "Test content"
    assert post["status"] == "draft"


def test_get_nonexistent_post(db):
    """Test getting a non-existent post"""
    post = db.get_post(999999)
    assert post is None


def test_save_post_with_scheduled_time(db):
    """Test saving a post with scheduled time"""
    scheduled_time = datetime(2026, 3, 15, 9, 0, 0)

    post_id = db.save_post(
        platform="x",
        content="Scheduled content",
        scheduled_at=scheduled_time,
        status="scheduled",
    )

    post = db.get_post(post_id)

    assert post is not None
    assert post["scheduled_at"] == scheduled_time.isoformat()


def test_update_post_status(db):
    """Test updating post status"""
    post_id = db.save_post(
        platform="x",
        content="Test content",
        status="draft",
    )

    success = db.update_post_status(post_id, "posted")

    assert success is True

    post = db.get_post(post_id)
    assert post["status"] == "posted"


def test_update_nonexistent_post_status(db):
    """Test updating status of non-existent post"""
    success = db.update_post_status(999999, "posted")
    assert success is False


def test_get_scheduled_posts(db):
    """Test getting scheduled posts"""
    scheduled_time1 = datetime(2026, 3, 15, 9, 0, 0)
    scheduled_time2 = datetime(2026, 3, 15, 10, 0, 0)

    db.save_post(
        platform="x",
        content="Post 1",
        scheduled_at=scheduled_time1,
        status="scheduled",
    )
    db.save_post(
        platform="x",
        content="Post 2",
        scheduled_at=scheduled_time2,
        status="scheduled",
    )
    db.save_post(
        platform="x",
        content="Draft post",
        status="draft",
    )

    scheduled_posts = db.get_scheduled_posts()

    assert len(scheduled_posts) == 2
    assert all(post["status"] == "scheduled" for post in scheduled_posts)


def test_get_scheduled_posts_with_limit(db):
    """Test getting scheduled posts with limit"""
    for i in range(10):
        db.save_post(
            platform="x",
            content=f"Post {i}",
            scheduled_at=datetime(2026, 3, 15, i, 0, 0),
            status="scheduled",
        )

    scheduled_posts = db.get_scheduled_posts(limit=5)

    assert len(scheduled_posts) == 5
