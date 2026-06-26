#!/usr/bin/env python3
"""Send paid media via a private Telegram channel."""

import argparse
import asyncio
import random

from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import SendMediaRequest, ExportChatInviteRequest
from telethon.tl.types import InputMediaPaidMedia, InputMediaUploadedPhoto


async def main(args):
    client = TelegramClient(args.session, args.api_id, args.api_hash)
    await client.connect()
    me = await client.get_me()
    print(f"Logged in: {me.first_name}", flush=True)

    target = await client.get_entity(args.target)
    print(f"Target: {target.first_name} (@{target.username})", flush=True)

    if args.channel_id:
        channel = await client.get_entity(int(args.channel_id))
        print(f"Using existing channel: {channel.title}", flush=True)
    else:
        print("Creating channel...", flush=True)
        result = await client(CreateChannelRequest(
            title=args.channel_name or "Paid Gallery 📸",
            about="Exclusive content",
            broadcast=True,
        ))
        channel = result.chats[0]
        print(f"Channel created: {channel.title} (ID: {channel.id})", flush=True)

    print("Uploading photo...", flush=True)
    uploaded = await client.upload_file(args.photo)

    paid_media = InputMediaPaidMedia(
        stars_amount=args.stars,
        extended_media=[InputMediaUploadedPhoto(file=uploaded)],
    )

    print("Posting paid media...", flush=True)
    await client(SendMediaRequest(
        peer=channel,
        media=paid_media,
        message=args.caption or "",
        random_id=random.randrange(-2**63, 2**63),
    ))
    print("Paid media posted!", flush=True)

    invite = await client(ExportChatInviteRequest(peer=channel))
    print(f"Invite: {invite.link}", flush=True)

    await client.send_message(target, f"{args.message or ''}\n{invite.link}".strip())
    print("Link sent!", flush=True)

    await client.disconnect()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Send Paid Media")
    p.add_argument("--session", required=True)
    p.add_argument("--api-id", type=int, required=True)
    p.add_argument("--api-hash", required=True)
    p.add_argument("--target", required=True, help="Recipient username")
    p.add_argument("--photo", required=True, help="Photo file path")
    p.add_argument("--stars", type=int, default=1, help="Star price")
    p.add_argument("--caption", default="", help="Media caption")
    p.add_argument("--message", default="", help="DM message with the link")
    p.add_argument("--channel-id", default=None, help="Reuse existing channel ID")
    p.add_argument("--channel-name", default=None, help="New channel name")
    args = p.parse_args()
    asyncio.run(main(args))
