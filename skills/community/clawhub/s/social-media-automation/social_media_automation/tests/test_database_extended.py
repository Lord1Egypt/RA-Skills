"""
Additional unit tests for database operations
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


def test_get_drafts_by_platform(db):
    """Test getting drafts filtered by platform"""
    # Create posts for different platforms
    db.save_post(platform="x", content="Twitter post", status="draft")
    db.save_post(platform="bluesky", content="Bluesky post", status="draft")
    db.save_post(platform="x", content="Another Twitter post", status="draft")

    # Get all posts and filter by platform
    posts = db.get_scheduled_posts()
    twitter_posts = [p for p in posts if p["platform"] == "x"]

    # Should have 2 Twitter posts
    assert len(twitter_posts) == 2


def test_update_multiple_post_statuses(db):
    """Test updating multiple post statuses"""
    post_id1 = db.save_post(platform="x", content="Post 1", status="draft")
    post_id2 = db.save_post(platform="x", content="Post 2", status="draft")
    post_id3 = db.save_post(platform="x", content="Post 3", status="draft")

    # Update first two
    db.update_post_status(post_id1, "posted")
    db.update_post_status(post_id2, "posted")

    # Check results
    post1 = db.get_post(post_id1)
    post2 = db.get_post(post_id2)
    post3 = db.get_post(post_id3)

    assert post1["status"] == "posted"
    assert post2["status"] == "posted"
    assert post3["status"] == "draft"


def test_post_with_post_id(db):
    """Test saving a post with external post ID"""
    post_id = db.save_post(
        platform="x",
        content="Posted content",
        post_id="1234567890",
        status="posted",
    )

    post = db.get_post(post_id)

    assert post is not None
    assert post["post_id"] == "1234567890"
    assert post["status"] == "posted"


def test_get_scheduled_posts_ordered(db):
    """Test that scheduled posts are ordered correctly"""
    # Create posts with different scheduled times
    time1 = datetime(2026, 3, 15, 10, 0, 0)
    time2 = datetime(2026, 3, 15, 9, 0, 0)
    time3 = datetime(2026, 3, 15, 11, 0, 0)

    db.save_post(platform="x", content="Post 1", scheduled_at=time1, status="scheduled")
    db.save_post(platform="x", content="Post 2", scheduled_at=time2, status="scheduled")
    db.save_post(platform="x", content="Post 3", scheduled_at=time3, status="scheduled")

    # Get scheduled posts
    posts = db.get_scheduled_posts()

    # Should be ordered by scheduled_at
    assert posts[0]["scheduled_at"] == time2.isoformat()
    assert posts[1]["scheduled_at"] == time1.isoformat()
    assert posts[2]["scheduled_at"] == time3.isoformat()
