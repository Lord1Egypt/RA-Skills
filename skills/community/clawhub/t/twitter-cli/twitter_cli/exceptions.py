"""Custom exceptions for twitter-cli.

Provides a structured exception hierarchy for categorized error handling:
- Authentication failures
- API errors (rate-limit, not-found, forbidden)
- Network errors
- Query ID resolution failures

Modeled after bilibili-cli/xiaohongshu-cli exception patterns.
"""

from __future__ import annotations


class TwitterError(RuntimeError):
    """Base exception for twitter-cli errors."""


class AuthenticationError(TwitterError):
    """Raised when cookies are missing, expired, or invalid."""


class RateLimitError(TwitterError):
    """Raised when Twitter rate limits the request (HTTP 429)."""


class NotFoundError(TwitterError):
    """Raised when a user or tweet is not found."""


class NetworkError(TwitterError):
    """Raised when upstream network requests fail."""


class QueryIdError(TwitterError):
    """Raised when a GraphQL queryId cannot be resolved."""


class TwitterAPIError(TwitterError):
    """Raised on non-OK Twitter API responses with HTTP status + message."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__("Twitter API error (HTTP %d): %s" % (status_code, message))
