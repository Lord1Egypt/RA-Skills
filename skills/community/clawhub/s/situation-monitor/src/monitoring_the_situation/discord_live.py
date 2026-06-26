from __future__ import annotations

from datetime import datetime, timedelta, timezone

import discord

from .config import Settings
from .models import MessageRecord


class SnapshotDiscordClient(discord.Client):
    def __init__(self, channel_ids: tuple[int, ...], cutoff: datetime, limit: int) -> None:
        intents = discord.Intents.default()
        intents.guilds = True
        intents.messages = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.channel_ids = channel_ids
        self.cutoff = cutoff
        self.limit = limit
        self.records: list[MessageRecord] = []

    async def on_ready(self) -> None:
        try:
            for channel_id in self.channel_ids:
                channel = self.get_channel(channel_id) or await self.fetch_channel(
                    channel_id
                )
                history = getattr(channel, "history", None)
                if history is None:
                    continue
                async for message in channel.history(
                    limit=self.limit, after=self.cutoff, oldest_first=False
                ):
                    if message.author.bot:
                        continue
                    self.records.append(
                        MessageRecord(
                            id=str(message.id),
                            channel=getattr(channel, "name", str(channel_id)),
                            author=str(message.author),
                            content=message.content,
                            created_at=message.created_at.astimezone(timezone.utc),
                            jump_url=message.jump_url,
                        )
                    )
        finally:
            await self.close()


async def fetch_discord_snapshot(
    settings: Settings, hours: int, limit_per_channel: int
) -> list[MessageRecord]:
    if not settings.discord_bot_token:
        raise ValueError("DISCORD_BOT_TOKEN is required for live Discord mode.")
    if not settings.discord_channel_ids:
        raise ValueError("DISCORD_CHANNEL_IDS must list at least one channel.")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    client = SnapshotDiscordClient(
        settings.discord_channel_ids,
        cutoff=cutoff,
        limit=min(limit_per_channel, settings.discord_message_limit),
    )
    await client.start(settings.discord_bot_token)
    return sorted(client.records, key=lambda item: item.created_at)
