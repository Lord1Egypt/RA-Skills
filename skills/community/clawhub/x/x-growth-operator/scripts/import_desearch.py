from __future__ import annotations

import argparse

from desearch_client import normalize_tweets, search_posts, timeline, post_replies
from common import load_local_env, utc_now_iso, write_json


def transform_tweet(tweet: dict) -> dict:
    user = tweet.get("user") or {}
    likes = int(tweet.get("like_count") or 0)
    replies = int(tweet.get("reply_count") or 0)
    reposts = int(tweet.get("retweet_count") or 0)
    quotes = int(tweet.get("quote_count") or 0)
    views = int(tweet.get("view_count") or 0)
    engagement_sum = likes + replies * 2 + reposts + quotes * 2
    growth_velocity = min(1.0, engagement_sum / 500.0)

    hashtags: list[str] = []
    entities = tweet.get("entities") or {}
    mentions: list[str] = []
    for tag in entities.get("hashtags") or []:
        if isinstance(tag, dict) and tag.get("text"):
            hashtags.append(str(tag["text"]).lower())
        elif isinstance(tag, str):
            hashtags.append(tag.lower())
    for mention in entities.get("mentions") or []:
        if isinstance(mention, dict) and mention.get("username"):
            mentions.append(str(mention["username"]).lower())

    referenced_tweets = tweet.get("referenced_tweets") or []
    reply_settings = tweet.get("reply_settings") or "everyone"
    is_reply_tweet = any(
        isinstance(reference, dict) and reference.get("type") == "replied_to"
        for reference in referenced_tweets
    )

    return {
        "id": f"desearch-{tweet.get('id')}",
        "source_account": user.get("username", ""),
        "source_type": "kol" if int(user.get("followers_count") or 0) > 10000 else "user",
        "text": tweet.get("text", ""),
        "url": tweet.get("url") or f"https://x.com/{user.get('username', 'i')}/status/{tweet.get('id', '')}",
        "posted_at": tweet.get("created_at", ""),
        "likes": likes,
        "replies": replies,
        "reposts": reposts,
        "quotes": quotes,
        "views": views,
        "growth_velocity": round(growth_velocity, 2),
        "sentiment": "positive",
        "topics": hashtags,
        "reply_settings": reply_settings,
        "conversation_id": tweet.get("conversation_id", ""),
        "referenced_tweets": referenced_tweets,
        "mentions": mentions,
        "is_reply_tweet": is_reply_tweet,
    }


def main() -> int:
    load_local_env()
    parser = argparse.ArgumentParser(description="Import X opportunities from Desearch.")
    parser.add_argument("command", choices=["x", "x_timeline", "x_post_replies"], help="Desearch command")
    parser.add_argument("query", help="Command query")
    parser.add_argument("--count", type=int, default=10, help="Result count")
    parser.add_argument("--sort", choices=["Top", "Latest"], default="Latest", help="Search sort order")
    parser.add_argument("--user", help="Restrict search to a username")
    parser.add_argument("--lang", help="Language filter")
    parser.add_argument("--start-date", help="Start date YYYY-MM-DD")
    parser.add_argument("--end-date", help="End date YYYY-MM-DD")
    parser.add_argument("--verified", action="store_true", help="Only verified users")
    parser.add_argument("--blue-verified", action="store_true", help="Only blue verified users")
    parser.add_argument("--is-quote", action="store_true", help="Only quote tweets")
    parser.add_argument("--is-video", action="store_true", help="Only video tweets")
    parser.add_argument("--is-image", action="store_true", help="Only image tweets")
    parser.add_argument("--min-retweets", type=int, help="Minimum retweet count")
    parser.add_argument("--min-replies", type=int, help="Minimum reply count")
    parser.add_argument("--min-likes", type=int, help="Minimum like count")
    parser.add_argument("--reply-query", help="Filter replies by keyword for x_post_replies")
    parser.add_argument("--output", default="data/opportunities_from_desearch.json", help="Output JSON path")
    args = parser.parse_args()

    if args.command == "x":
        payload = search_posts(
            args.query,
            count=args.count,
            sort=args.sort,
            user=args.user,
            start_date=args.start_date,
            end_date=args.end_date,
            lang=args.lang,
            verified=args.verified,
            blue_verified=args.blue_verified,
            is_quote=args.is_quote,
            is_video=args.is_video,
            is_image=args.is_image,
            min_retweets=args.min_retweets,
            min_replies=args.min_replies,
            min_likes=args.min_likes,
        )
    elif args.command == "x_timeline":
        payload = timeline(args.query, count=args.count)
    else:
        payload = post_replies(args.query, count=args.count, query=args.reply_query)

    tweets = normalize_tweets(payload)
    items = [transform_tweet(tweet) for tweet in tweets]
    output = {
        "generated_at": utc_now_iso(),
        "source": f"desearch:{args.command}",
        "count": len(items),
        "items": items,
    }
    path = write_json(args.output, output)
    print(f"Wrote {len(items)} opportunities to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
