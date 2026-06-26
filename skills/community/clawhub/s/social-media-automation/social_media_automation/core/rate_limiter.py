"""
Rate limit management for Twitter API
"""

import time
from collections import defaultdict
from datetime import datetime, timedelta

from pydantic import BaseModel

from social_media_automation.utils.logger import setup_logger

logger = setup_logger()


class RateLimit(BaseModel):
    """Rate limit information"""

    limit: int
    remaining: int
    reset: datetime


class RateLimiter:
    """Rate limiter for API calls"""

    def __init__(self) -> None:
        """Initialize rate limiter"""
        self.rate_limits: dict[str, RateLimit] = defaultdict(lambda: RateLimit(limit=0, remaining=0, reset=datetime.now()))

    def update_rate_limit(self, endpoint: str, limit: int, remaining: int, reset: int) -> None:
        """Update rate limit for an endpoint"""
        reset_time = datetime.fromtimestamp(reset)
        self.rate_limits[endpoint] = RateLimit(limit=limit, remaining=remaining, reset=reset_time)

        logger.info(f"Rate limit updated for {endpoint}: {remaining}/{limit} (resets at {reset_time})")

    def check_rate_limit(self, endpoint: str) -> tuple[bool, int]:
        """Check if request is allowed"""
        rate_limit = self.rate_limits[endpoint]

        # Reset if expired
        if datetime.now() >= rate_limit.reset:
            rate_limit.remaining = rate_limit.limit
            rate_limit.reset = datetime.now() + timedelta(minutes=15)

        if rate_limit.remaining <= 0:
            wait_time = (rate_limit.reset - datetime.now()).total_seconds()
            logger.warning(f"Rate limit exceeded for {endpoint}. Must wait {wait_time:.2f}s")
            return False, int(wait_time)

        return True, rate_limit.remaining

    def wait_for_reset(self, endpoint: str) -> None:
        """Wait for rate limit to reset"""
        _, remaining = self.check_rate_limit(endpoint)
        if remaining <= 0:
            rate_limit = self.rate_limits[endpoint]
            wait_time = (rate_limit.reset - datetime.now()).total_seconds()
            if wait_time > 0:
                logger.info(f"Waiting {wait_time:.2f}s for rate limit reset...")
                time.sleep(wait_time)

    def decrement_remaining(self, endpoint: str) -> None:
        """Decrement remaining requests"""
        rate_limit = self.rate_limits[endpoint]
        if rate_limit.remaining > 0:
            rate_limit.remaining -= 1

    def get_status(self) -> dict[str, dict[str, Any]]:
        """Get status of all rate limits"""
        return {
            endpoint: {
                "limit": rate_limit.limit,
                "remaining": rate_limit.remaining,
                "reset_at": rate_limit.reset.isoformat(),
            }
            for endpoint, rate_limit in self.rate_limits.items()
        }
