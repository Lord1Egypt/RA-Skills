#!/usr/bin/env python3
"""Fetch new messages from WeFlow groups and format for summarization."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

import yaml


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config_path, config):
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def load_members(members_path):
    if not members_path or not os.path.exists(members_path):
        return {}
    with open(members_path, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_messages(host, talker):
    url = (
        f"{host}/api/v1/messages"
        f"?talker={talker}&limit=500&media=1&image=1&voice=0&video=0&emoji=0"
    )
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def download_image(media_url, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    filename = media_url.rsplit("/", 1)[-1]
    save_path = os.path.join(save_dir, filename)
    if os.path.exists(save_path):
        return save_path
    try:
        req = urllib.request.Request(media_url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(save_path, "wb") as f:
                f.write(resp.read())
        return save_path
    except Exception as e:
        print(f"Warning: failed to download {media_url}: {e}", file=sys.stderr)
        return None


def format_time(timestamp_ms):
    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    return dt.strftime("[%Y-%m-%d %H:%M]")


def resolve_nickname(sender, members):
    return members.get(sender, sender)


def process_group(host, group, images_dir):
    talker = group["talker"]
    name = group.get("name", talker)
    members_path = group.get("members")
    prompt = group.get("summary_prompt", "")
    subscribe = group.get("subscribe_members", [])
    last_id = group.get("last_local_id", 0)

    members = load_members(members_path)

    try:
        data = fetch_messages(host, talker)
    except Exception as e:
        print(f"Error fetching messages for {name}: {e}", file=sys.stderr)
        return last_id

    all_msgs = data.get("messages", [])
    new_msgs = [m for m in all_msgs if m.get("localId", 0) > last_id]

    if not new_msgs:
        print(f"群名：{name}")
        print("无新消息。")
        print()
        return last_id

    # Sort by localId ascending
    new_msgs.sort(key=lambda m: m.get("localId", 0))

    img_dir = os.path.join(images_dir, talker) if images_dir else None

    # Format main messages
    lines = []
    subscribe_messages = {wxid: [] for wxid in subscribe}

    for msg in new_msgs:
        sender = msg.get("senderUsername", "")
        nickname = resolve_nickname(sender, members)
        ts = msg.get("createTime", 0)
        time_str = format_time(ts) if ts else ""
        content = msg.get("content", "")

        # Handle image messages
        if msg.get("mediaType") == "image" and msg.get("mediaUrl"):
            img_path = None
            if img_dir:
                img_path = download_image(msg["mediaUrl"], img_dir)
            if img_path:
                content = f"[图片] {os.path.abspath(img_path)}"
            else:
                content = "[图片]"

        line = f"{time_str} {nickname}: {content}"
        lines.append(line)

        # Track subscribe_members messages
        if sender in subscribe_messages:
            subscribe_messages[sender].append(content)

    # Output
    print(f"群名：{name}")
    if prompt:
        print(f"用户要求：{prompt}")
    print("近期群信息：")
    for line in lines:
        print(line)

    # Subscribe members section
    has_subscribe = any(msgs for msgs in subscribe_messages.values())
    if has_subscribe:
        print()
        print("另外总结关注群友的发言：")
        for wxid, msgs in subscribe_messages.items():
            if not msgs:
                continue
            member_name = resolve_nickname(wxid, members)
            print(f"{member_name}说：")
            for i, m in enumerate(msgs, 1):
                print(f"{i}. {m}")

    print()

    # Return new last_local_id
    return max(m.get("localId", 0) for m in new_msgs)


def main():
    parser = argparse.ArgumentParser(description="Fetch WeFlow group messages")
    parser.add_argument("config", help="Path to weflow-groups.yaml")
    parser.add_argument(
        "--images-dir",
        default="images",
        help="Directory to save downloaded images (default: images)",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    host = config.get("host", "").rstrip("/")

    if not host:
        print("Error: 'host' not set in config", file=sys.stderr)
        sys.exit(1)

    groups = config.get("groups", [])
    if not groups:
        print("Error: no groups configured", file=sys.stderr)
        sys.exit(1)

    print("根据用户要求，总结各群消息")
    print()

    updated = False
    for group in groups:
        new_last_id = process_group(host, group, args.images_dir)
        if new_last_id > group.get("last_local_id", 0):
            group["last_local_id"] = new_last_id
            updated = True

    if updated:
        save_config(args.config, config)


if __name__ == "__main__":
    main()
