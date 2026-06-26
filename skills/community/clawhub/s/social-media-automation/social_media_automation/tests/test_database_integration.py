"""
Additional database integration tests
"""

import pytest
from datetime import datetime, timedelta

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


def test_multiple_post_operations(db):
    """Test multiple post operations"""
    # Create multiple posts
    post_ids = []
    for i in range(10):
        post_id = db.save_post(
            platform="x",
            content=f"Post {i}",
            status="draft",
        )
        post_ids.append(post_id)

    # Get all posts
    for post_id in post_ids:
        post = db.get_post(post_id)
        assert post is not None
        assert post["content"] == f"Post {post_id - 1}"


def test_post_status_transitions(db):
    """Test post status transitions"""
    # Create post
    post_id = db.save_post(platform="x", content="Test", status="draft")

    # Draft -> scheduled
    db.update_post_status(post_id, "scheduled")
    post = db.get_post(post_id)
    assert post["status"] == "scheduled"

    # Scheduled -> posted
    db.update_post_status(post_id, "posted")
    post = db.get_post(post_id)
    assert post["status"] == "posted"


def test_post_with_metadata(db):
    """Test saving and retrieving post with metadata"""
    scheduled_time = datetime.now() + timedelta(hours=1)

    post_id = db.save_post(
        platform="x",
        content="Test content",
        post_id="1234567890",
        scheduled_at=scheduled_time,
        status="scheduled",
    )

    post = db.get_post(post_id)

    assert post is not None
    assert post["post_id"] == "1234567890"
    assert post["scheduled_at"] == scheduled_time.isoformat()
    assert post["status"] == "scheduled"
