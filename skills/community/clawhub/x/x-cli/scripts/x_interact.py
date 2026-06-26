#!/usr/bin/env python3
"""
x-cli interact — Like, retweet, bookmark, follow, and other interactions.

Usage:
  python x_interact.py like <tweet-id-or-url>
  python x_interact.py unlike <tweet-id-or-url>
  python x_interact.py retweet <tweet-id-or-url>
  python x_interact.py unretweet <tweet-id-or-url>
  python x_interact.py bookmark <tweet-id-or-url>
  python x_interact.py unbookmark <tweet-id-or-url>
  python x_interact.py follow <username>
  python x_interact.py unfollow <username>
  python x_interact.py delete <tweet-id-or-url>
  python x_interact.py mute <username>
  python x_interact.py unmute <username>
  python x_interact.py block <username>
  python x_interact.py unblock <username>
"""

import argparse
import re

from x_utils import get_client, run


def extract_tweet_id(url_or_id: str) -> str:
    match = re.search(r"/status/(\d+)", url_or_id)
    return match.group(1) if match else url_or_id


async def resolve_user(client, username: str):
    username = username.lstrip("@")
    return await client.get_user_by_screen_name(username)


async def cmd_like(args):
    client = await get_client()
    tweet_id = extract_tweet_id(args.target)
    await client.favorite_tweet(tweet_id)
    print(f"❤️ Liked tweet {tweet_id}")

async def cmd_unlike(args):
    client = await get_client()
    tweet_id = extract_tweet_id(args.target)
    await client.unfavorite_tweet(tweet_id)
    print(f"💔 Unliked tweet {tweet_id}")

async def cmd_retweet(args):
    client = await get_client()
    tweet_id = extract_tweet_id(args.target)
    await client.retweet(tweet_id)
    print(f"🔁 Retweeted {tweet_id}")

async def cmd_unretweet(args):
    client = await get_client()
    tweet_id = extract_tweet_id(args.target)
    await client.delete_retweet(tweet_id)
    print(f"↩️ Unretweeted {tweet_id}")

async def cmd_bookmark(args):
    client = await get_client()
    tweet_id = extract_tweet_id(args.target)
    await client.bookmark_tweet(tweet_id)
    print(f"🔖 Bookmarked tweet {tweet_id}")

async def cmd_unbookmark(args):
    client = await get_client()
    tweet_id = extract_tweet_id(args.target)
    await client.delete_bookmark(tweet_id)
    print(f"📄 Removed bookmark {tweet_id}")

async def cmd_follow(args):
    client = await get_client()
    user = await resolve_user(client, args.target)
    await client.follow_user(user.id)
    print(f"✅ Following @{user.screen_name}")

async def cmd_unfollow(args):
    client = await get_client()
    user = await resolve_user(client, args.target)
    await client.unfollow_user(user.id)
    print(f"👋 Unfollowed @{user.screen_name}")

async def cmd_delete(args):
    client = await get_client()
    tweet_id = extract_tweet_id(args.target)
    await client.delete_tweet(tweet_id)
    print(f"🗑️ Deleted tweet {tweet_id}")

async def cmd_mute(args):
    client = await get_client()
    user = await resolve_user(client, args.target)
    await client.mute_user(user.id)
    print(f"🔇 Muted @{user.screen_name}")

async def cmd_unmute(args):
    client = await get_client()
    user = await resolve_user(client, args.target)
    await client.unmute_user(user.id)
    print(f"🔊 Unmuted @{user.screen_name}")

async def cmd_block(args):
    client = await get_client()
    user = await resolve_user(client, args.target)
    await client.block_user(user.id)
    print(f"🚫 Blocked @{user.screen_name}")

async def cmd_unblock(args):
    client = await get_client()
    user = await resolve_user(client, args.target)
    await client.unblock_user(user.id)
    print(f"✅ Unblocked @{user.screen_name}")


COMMANDS = {
    "like": cmd_like, "unlike": cmd_unlike,
    "retweet": cmd_retweet, "unretweet": cmd_unretweet,
    "bookmark": cmd_bookmark, "unbookmark": cmd_unbookmark,
    "follow": cmd_follow, "unfollow": cmd_unfollow,
    "delete": cmd_delete,
    "mute": cmd_mute, "unmute": cmd_unmute,
    "block": cmd_block, "unblock": cmd_unblock,
}


def main():
    parser = argparse.ArgumentParser(description="x-cli interact — X/Twitter interactions")
    parser.add_argument("command", choices=COMMANDS.keys(), help="Action to perform")
    parser.add_argument("target", help="Tweet URL/ID or @username")
    args = parser.parse_args()
    run(COMMANDS[args.command](args))


if __name__ == "__main__":
    main()
