#!/usr/bin/env python3
"""
Slack Auto-Collector

Connects to Slack workspace via Bot Token to automatically collect
messages, threads, and activity from a target user.

Usage:
    python3 slack_collector.py --setup
    python3 slack_collector.py --username "alex.chen" --output-dir ./knowledge/alex --msg-limit 1000
"""

from __future__ import annotations

import json
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

CONFIG_PATH = Path.home() / ".teammate-skill" / "slack_config.json"


def setup():
    """Interactive setup for Slack Bot Token."""
    print("=== Slack Auto-Collector Setup ===\n")
    print("You'll need a Slack Bot Token with these scopes:")
    print("  - channels:history")
    print("  - channels:read")
    print("  - users:read")
    print("  - groups:history (for private channels)")
    print("  - search:read (optional, for better coverage)\n")
    print("Create a Slack App at: https://api.slack.com/apps\n")

    token = input("Slack Bot Token (xoxb-...): ").strip()
    if not token.startswith("xoxb-"):
        print("⚠️  Token should start with 'xoxb-'. Proceeding anyway.")

    config = {"bot_token": token}
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"\n✅ Config saved to {CONFIG_PATH}")
    print("   Make sure the bot is added to the channels you want to collect from.")


def load_config() -> dict:
    """Load Slack config."""
    if not CONFIG_PATH.exists():
        print("❌ No Slack config found. Run with --setup first.")
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def collect(username: str, output_dir: str, msg_limit: int = 1000, channel_limit: int = 20):
    """Collect messages from target user via Slack API."""
    try:
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError
    except ImportError:
        print("❌ slack_sdk not installed. Run: pip3 install slack_sdk")
        sys.exit(1)

    config = load_config()
    client = WebClient(token=config["bot_token"])

    # Find target user
    print(f"Looking up user: {username}")
    try:
        users_response = client.users_list()
        users = users_response["members"]
    except SlackApiError as e:
        print(f"❌ Failed to list users: {e.response['error']}")
        sys.exit(1)

    target_uid = None
    target_name = None
    username_lower = username.lower()
    for u in users:
        if u.get("deleted"):
            continue
        name = u.get("real_name", "")
        uname = u.get("name", "")
        if username_lower in name.lower() or username_lower in uname.lower():
            target_uid = u["id"]
            target_name = name or uname
            break

    if not target_uid:
        print(f"❌ User '{username}' not found. Available users:")
        for u in users[:20]:
            if not u.get("deleted") and not u.get("is_bot"):
                print(f"   {u.get('real_name', 'N/A')} (@{u.get('name', 'N/A')})")
        sys.exit(1)

    print(f"Found: {target_name} ({target_uid})")

    # Get channels with pagination
    all_channels = []
    try:
        cursor = None
        while True:
            params = {"types": "public_channel,private_channel", "limit": 200}
            if cursor:
                params["cursor"] = cursor
            channels_response = client.conversations_list(**params)
            all_channels.extend(channels_response["channels"])
            cursor = channels_response.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break
    except SlackApiError as e:
        print(f"❌ Failed to list channels: {e.response['error']}")
        sys.exit(1)

    channels = all_channels

    # Collect messages from each channel
    all_messages = []
    all_threads = []
    channels_processed = 0
    rate_limit_wait = 1  # seconds, increases on 429

    for channel in channels[:channel_limit]:
        channel_name = channel.get("name", channel["id"])
        try:
            cursor = None
            while len(all_messages) < msg_limit:
                params = {"channel": channel["id"], "limit": 200}
                if cursor:
                    params["cursor"] = cursor
                try:
                    history = client.conversations_history(**params)
                except SlackApiError as e:
                    if e.response.get("error") == "ratelimited":
                        retry_after = int(e.response.headers.get("Retry-After", rate_limit_wait))
                        print(f"   ⏳ Rate limited, waiting {retry_after}s...")
                        import time
                        time.sleep(retry_after)
                        rate_limit_wait = min(rate_limit_wait * 2, 60)
                        continue
                    raise

                for msg in history.get("messages", []):
                    if msg.get("user") != target_uid:
                        continue
                    if msg.get("subtype") in ("channel_join", "channel_leave", "bot_message"):
                        continue

                    text = msg.get("text", "").strip()
                    if not text:
                        continue

                    ts = msg.get("ts", "0")
                    try:
                        dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
                        timestamp = dt.strftime("%Y-%m-%d %H:%M")
                    except (ValueError, OSError):
                        timestamp = "unknown"

                    all_messages.append({
                        "channel": channel_name,
                        "timestamp": timestamp,
                        "text": text,
                    })

                    # Collect thread replies if this is a thread parent
                    if msg.get("reply_count", 0) > 0:
                        try:
                            thread_response = client.conversations_replies(
                                channel=channel["id"],
                                ts=msg["ts"],
                                limit=50,
                            )
                            for reply in thread_response.get("messages", [])[1:]:  # skip parent
                                if reply.get("user") == target_uid:
                                    reply_text = reply.get("text", "").strip()
                                    if reply_text:
                                        all_threads.append({
                                            "channel": channel_name,
                                            "timestamp": timestamp,
                                            "text": reply_text,
                                            "parent_text": text[:100],
                                        })
                        except SlackApiError:
                            pass

                    if len(all_messages) >= msg_limit:
                        break

                cursor = history.get("response_metadata", {}).get("next_cursor")
                if not cursor or len(all_messages) >= msg_limit:
                    break

        except SlackApiError:
            continue

        channels_processed += 1
        # Progress indicator
        if channels_processed % 5 == 0:
            print(f"   Processed {channels_processed}/{min(len(channels), channel_limit)} channels, {len(all_messages)} messages so far...")

        if len(all_messages) >= msg_limit:
            break

    # Write output
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Messages
    with open(out_path / "messages.txt", "w", encoding="utf-8") as f:
        f.write(f"# Slack Messages from {target_name}\n")
        f.write(f"# Total: {len(all_messages)} messages from {channels_processed} channels\n\n")
        for msg in sorted(all_messages, key=lambda m: m["timestamp"]):
            f.write(f"[{msg['timestamp']}] #{msg['channel']}: {msg['text']}\n")

    # Threads
    with open(out_path / "threads.txt", "w", encoding="utf-8") as f:
        f.write(f"# Slack Thread Replies from {target_name}\n")
        f.write(f"# Total: {len(all_threads)} thread replies\n\n")
        for t in sorted(all_threads, key=lambda m: m["timestamp"]):
            f.write(f"[{t['timestamp']}] #{t['channel']} (re: {t['parent_text']}...): {t['text']}\n")

    # Summary
    summary = {
        "target": target_name,
        "target_uid": target_uid,
        "messages_collected": len(all_messages),
        "threads_collected": len(all_threads),
        "channels_processed": channels_processed,
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(out_path / "collection_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Collection complete:")
    print(f"   Messages: {len(all_messages)}")
    print(f"   Thread replies: {len(all_threads)}")
    print(f"   Channels: {channels_processed}")
    print(f"   Output: {out_path}/")


def main():
    parser = argparse.ArgumentParser(description="Slack auto-collector for teammate.skill")
    parser.add_argument("--setup", action="store_true", help="Run interactive setup")
    parser.add_argument("--username", help="Target user's Slack username or display name")
    parser.add_argument("--output-dir", default="./knowledge", help="Output directory")
    parser.add_argument("--msg-limit", type=int, default=1000, help="Max messages to collect")
    parser.add_argument("--channel-limit", type=int, default=20, help="Max channels to scan")

    args = parser.parse_args()

    if args.setup:
        setup()
    elif args.username:
        collect(args.username, args.output_dir, args.msg_limit, args.channel_limit)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
