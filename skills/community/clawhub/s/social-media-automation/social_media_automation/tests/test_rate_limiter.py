"""
Additional unit tests for rate limiter
"""

import pytest
from datetime import datetime, timedelta

from social_media_automation.core.rate_limiter import RateLimiter


@pytest.fixture
def rate_limiter():
    """Create a RateLimiter instance"""
    return RateLimiter()


def test_rate_limiter_initialization(rate_limiter):
    """Test RateLimiter initialization"""
    assert rate_limiter.rate_limits is not None


def test_rate_limiter_update_rate_limit(rate_limiter):
    """Test updating rate limit for an endpoint"""
    rate_limiter.update_rate_limit(
        endpoint="tweets/create",
        limit=60,
        remaining=59,
        reset=int(datetime.now().timestamp()) + 900,
    )

    status = rate_limiter.get_status()

    assert "tweets/create" in status
    assert status["tweets/create"]["limit"] == 60
    assert status["tweets/create"]["remaining"] == 59


def test_rate_limiter_check_rate_limit(rate_limiter):
    """Test checking rate limit"""
    # Set rate limit
    rate_limiter.update_rate_limit(
        endpoint="tweets/create",
        limit=60,
        remaining=5,
        reset=int(datetime.now().timestamp()) + 900,
    )

    # Check if request is allowed
    allowed, remaining = rate_limiter.check_rate_limit("tweets/create")

    assert allowed is True
    assert remaining == 5


def test_rate_limiter_exceeded(rate_limiter):
    """Test rate limit exceeded"""
    # Set rate limit with 0 remaining
    rate_limiter.update_rate_limit(
        endpoint="tweets/create",
        limit=60,
        remaining=0,
        reset=int((datetime.now() + timedelta(minutes=1)).timestamp()),
    )

    # Check if request is allowed
    allowed, wait_time = rate_limiter.check_rate_limit("tweets/create")

    assert allowed is False
    assert wait_time >= 0


def test_rate_limiter_decrement_remaining(rate_limiter):
    """Test decrementing remaining requests"""
    # Set rate limit
    rate_limiter.update_rate_limit(
        endpoint="tweets/create",
        limit=60,
        remaining=5,
        reset=int(datetime.now().timestamp()) + 900,
    )

    # Decrement
    rate_limiter.decrement_remaining("tweets/create")

    # Check status
    status = rate_limiter.get_status()

    assert status["tweets/create"]["remaining"] == 4