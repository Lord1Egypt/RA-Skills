from __future__ import annotations

from twitter_cli.filter import filter_tweets


def test_filter_tweets_does_not_mutate_input(tweet_factory) -> None:
    tweet = tweet_factory("1", score=0.0)
    output = filter_tweets([tweet], {"mode": "all", "weights": {}})

    assert tweet.score == 0.0
    assert output[0].score > 0.0
    assert output[0] is not tweet


def test_filter_tweets_applies_language_and_retweet_filters(tweet_factory) -> None:
    tweets = [
        tweet_factory("1", lang="en", is_retweet=False),
        tweet_factory("2", lang="zh", is_retweet=False),
        tweet_factory("3", lang="en", is_retweet=True),
    ]
    output = filter_tweets(
        tweets,
        {
            "mode": "all",
            "lang": ["en"],
            "excludeRetweets": True,
            "weights": {},
        },
    )

    assert [tweet.id for tweet in output] == ["1"]
