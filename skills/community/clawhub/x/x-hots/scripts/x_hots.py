#!/usr/bin/env python3
"""
X (Twitter) Hot Topics Fetcher

Fetches recent hot tweets for given search queries using Tweepy API v2.

FALLBACK SOURCE ONLY: per SKILL.md the primary source is the logged-in
browser on x.com; this script runs only when the browser source fails.
X_BEARER_TOKEN is therefore OPTIONAL (needed only for this fallback);
no OAuth 1.0a user credentials are required.
"""

import os
import sys
import json
import tweepy
from datetime import datetime, timezone


def create_client():
    """Create Tweepy client using app-only Bearer token auth."""
    bearer_token = os.environ.get('X_BEARER_TOKEN')
    if not bearer_token:
        print(json.dumps({
            "success": False,
            "error": "X_BEARER_TOKEN not set (optional fallback credential). "
                     "Prefer the browser source per SKILL.md; set X_BEARER_TOKEN "
                     "only if API fallback is desired."
        }))
        sys.exit(1)

    # App-only auth: bearer token alone is sufficient for search_recent_tweets
    # and has broader search access than OAuth 1.0a user context.
    return tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)


def search_hot_topics(client, queries, max_results_per_query=10):
    """
    Search for hot topics based on a list of queries.

    Args:
        client: Tweepy Client instance.
        queries: List of search query strings.
        max_results_per_query: Number of tweets to fetch per query (default 10).

    Returns:
        dict: Mapping of query -> result (tweets, count, success status).
    """
    results = {}

    for query in queries:
        try:
            # Search recent tweets, sorted by relevancy for hot topics
            response = client.search_recent_tweets(
                query=f"{query} -is:retweet lang:en",
                max_results=max_results_per_query,
                sort_order="relevancy",
                tweet_fields=['created_at', 'public_metrics', 'author_id', 'lang']
            )

            if response.data:
                tweets = []
                for tweet in response.data:
                    tweet_data = {
                        "id": tweet.id,
                        "text": tweet.text,
                        "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
                        "metrics": tweet.public_metrics if hasattr(tweet, 'public_metrics') else {},
                        "url": f"https://twitter.com/twitter/status/{tweet.id}"
                    }
                    tweets.append(tweet_data)

                results[query] = {
                    "success": True,
                    "count": len(tweets),
                    "tweets": tweets
                }
            else:
                results[query] = {
                    "success": True,
                    "count": 0,
                    "tweets": [],
                    "note": "No tweets found"
                }

        except tweepy.TweepyException as e:
            results[query] = {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            results[query] = {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    return results


def main():
    """Main entry point. Expects a JSON array of search queries as the first argument."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: x_hots.py '<json_queries>'\nExample: x_hots.py '[\"AI\", \"economy\"]'"
        }))
        sys.exit(1)

    try:
        queries = json.loads(sys.argv[1])
        if not isinstance(queries, list):
            raise ValueError("Queries must be a JSON array")
    except (json.JSONDecodeError, ValueError) as e:
        print(json.dumps({
            "success": False,
            "error": f"Invalid JSON input: {str(e)}"
        }))
        sys.exit(1)

    client = create_client()
    results = search_hot_topics(client, queries)

    output = {
        "success": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "queries": queries,
        "results": results
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
