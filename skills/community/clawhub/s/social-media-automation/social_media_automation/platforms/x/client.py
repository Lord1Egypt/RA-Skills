"""
Twitter/X API client using Tweepy
"""

import time
from typing import Any

import tweepy

from social_media_automation.core.rate_limiter import RateLimiter
from social_media_automation.utils.logger import setup_logger

logger = setup_logger()


class TwitterClient:
    """Twitter/X API client"""

    def __init__(self, config: object) -> None:
        """Initialize Twitter client"""
        self.config = config
        self.rate_limiter = RateLimiter()

        if not config.twitter_bearer_token:
            raise ValueError("Twitter Bearer Token is not configured")

        # Initialize Twitter client
        self.client = tweepy.Client(
            bearer_token=config.twitter_bearer_token,
            consumer_key=config.twitter_api_key,
            consumer_secret=config.twitter_api_secret,
            access_token=config.twitter_access_token,
            access_token_secret=config.twitter_access_secret,
        )

    def post_tweet(self, text: str) -> tweepy.Response:
        """Post a tweet"""
        try:
            logger.info(f"Posting tweet: {text[:50]}...")
            response = self.client.create_tweet(text=text)
            self.rate_limiter.update_rate_limit("create_tweet", 50, 49, int(time.time()) + 900)
            return response
        except tweepy.TweepyException as e:
            logger.error(f"Failed to post tweet: {e}")
            raise Exception(f"Twitter API error: {e}")

    def get_user_info(self, username: str) -> dict[str, Any]:
        """Get user information"""
        try:
            user = self.client.get_user(username=username)
            return user.data.data
        except tweepy.TweepyException as e:
            logger.error(f"Failed to get user info: {e}")
            raise Exception(f"Twitter API error: {e}")

    def delete_tweet(self, tweet_id: str) -> bool:
        """Delete a tweet"""
        try:
            self.client.delete_tweet(tweet_id)
            logger.info(f"Deleted tweet: {tweet_id}")
            return True
        except tweepy.TweepyException as e:
            logger.error(f"Failed to delete tweet: {e}")
            raise Exception(f"Twitter API error: {e}")

    def get_home_timeline(self, limit: int = 20) -> list[tweepy.Tweet]:
        """Get home timeline"""
        try:
            logger.info(f"Fetching home timeline (limit: {limit})")
            tweets = self.client.get_home_timeline(max_results=min(limit, 100))

            if not tweets.data:
                return []

            return tweets.data
        except tweepy.TweepyException as e:
            logger.error(f"Failed to fetch home timeline: {e}")
            raise Exception(f"Twitter API error: {e}")

    def get_user_timeline(self, username: str, limit: int = 20) -> list[tweepy.Tweet]:
        """Get user timeline"""
        try:
            logger.info(f"Fetching user timeline for {username} (limit: {limit})")

            user = self.client.get_user(username=username)
            tweets = self.client.get_users_tweets(id=user.data.id, max_results=min(limit, 100))

            if not tweets.data:
                return []

            return tweets.data
        except tweepy.TweepyException as e:
            logger.error(f"Failed to fetch user timeline: {e}")
            raise Exception(f"Twitter API error: {e}")

    def post_reply(self, tweet_id: str, text: str) -> tweepy.Response:
        """Post a reply to a tweet"""
        try:
            logger.info(f"Posting reply to {tweet_id}: {text[:50]}...")
            response = self.client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
            return response
        except tweepy.TweepyException as e:
            logger.error(f"Failed to post reply: {e}")
            raise Exception(f"Twitter API error: {e}")

    def retweet(self, tweet_id: str) -> bool:
        """Retweet a tweet"""
        try:
            logger.info(f"Retweeting: {tweet_id}")
            self.client.retweet(tweet_id=tweet_id)
            return True
        except tweepy.TweepyException as e:
            logger.error(f"Failed to retweet: {e}")
            raise Exception(f"Twitter API error: {e}")

    def like_tweet(self, tweet_id: str) -> bool:
        """Like a tweet"""
        try:
            logger.info(f"Liking tweet: {tweet_id}")
            self.client.like(tweet_id=tweet_id)
            return True
        except tweepy.TweepyException as e:
            logger.error(f"Failed to like tweet: {e}")
            raise Exception(f"Twitter API error: {e}")

    def get_mentions(self, limit: int = 20) -> list[tweepy.Tweet]:
        """Get mentions timeline"""
        try:
            logger.info(f"Fetching mentions (limit: {limit})")
            tweets = self.client.get_mentions_timeline(max_results=min(limit, 100))

            if not tweets.data:
                return []

            return tweets.data
        except tweepy.TweepyException as e:
            logger.error(f"Failed to fetch mentions: {e}")
            raise Exception(f"Twitter API error: {e}")

    def get_rate_limit_status(self) -> dict[str, Any]:
        """Get rate limit status"""
        return self.rate_limiter.get_status()


# Add RateLimiter class here as well to avoid circular import
class SimpleRateLimiter:
    """Simple rate limiter without complex dependencies"""

    def __init__(self) -> None:
        self.rate_limits: dict[str, dict[str, Any]] = {}

    def update_rate_limit(self, endpoint: str, limit: int, remaining: int, reset: int) -> None:
        """Update rate limit for an endpoint"""
        self.rate_limits[endpoint] = {
            "limit": limit,
            "remaining": remaining,
            "reset_at": reset,
        }

    def get_status(self) -> dict[str, Any]:
        """Get status of all rate limits"""
        return self.rate_limits

