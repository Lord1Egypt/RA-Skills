"""Tests for Telegram client helpers without hitting the network."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import click
import pytest

from tg_cli.client import connect, fetch_history, sync_all


@dataclass
class FakeEntity:
    id: int
    title: str


@dataclass
class FakeDialog:
    entity: FakeEntity
    name: str


@dataclass
class FakeMessage:
    id: int
    sender_id: int
    text: str
    date: datetime
    message: str | None = None


class FakeClient:
    def __init__(self, dialogs: list[FakeDialog], messages_by_chat: dict[int, list[FakeMessage]]):
        self._dialogs = dialogs
        self._messages_by_chat = messages_by_chat

    async def get_entity(self, chat):
        if isinstance(chat, FakeEntity):
            return chat
        for dialog in self._dialogs:
            if chat == dialog.entity.id or chat == dialog.name:
                return dialog.entity
        raise ValueError(f"unknown chat: {chat}")

    async def iter_dialogs(self):
        for dialog in self._dialogs:
            yield dialog

    async def iter_participants(self, entity):
        if False:
            yield None

    async def iter_messages(self, entity, limit: int, min_id: int = 0):
        messages = self._messages_by_chat.get(entity.id, [])
        for msg in messages[:limit]:
            if msg.id > min_id:
                yield msg


@pytest.mark.asyncio
async def test_fetch_history_returns_inserted_count(db):
    entity = FakeEntity(id=100, title="Test Group")
    client = FakeClient(
        dialogs=[FakeDialog(entity=entity, name="Test Group")],
        messages_by_chat={
            100: [
                FakeMessage(id=1, sender_id=1, text="old", date=datetime.now(timezone.utc)),
                FakeMessage(id=2, sender_id=1, text="new-1", date=datetime.now(timezone.utc)),
                FakeMessage(id=3, sender_id=1, text="new-2", date=datetime.now(timezone.utc)),
            ]
        },
    )

    db.insert_message(
        chat_id=100,
        chat_name="Test Group",
        msg_id=1,
        sender_id=1,
        sender_name="Alice",
        content="old",
        timestamp=datetime.now(timezone.utc),
    )

    inserted = await fetch_history(client, 100, db=db, limit=10)
    assert inserted == 2


@pytest.mark.asyncio
async def test_sync_all_discovers_dialogs_from_client(db):
    dialogs = [
        FakeDialog(entity=FakeEntity(id=100, title="Group A"), name="Group A"),
        FakeDialog(entity=FakeEntity(id=200, title="Group B"), name="Group B"),
    ]
    client = FakeClient(
        dialogs=dialogs,
        messages_by_chat={
            100: [FakeMessage(id=1, sender_id=1, text="hello", date=datetime.now(timezone.utc))],
            200: [FakeMessage(id=1, sender_id=2, text="world", date=datetime.now(timezone.utc))],
        },
    )

    results = await sync_all(client, db, limit_per_chat=10)
    assert results == {"Group A": 1, "Group B": 1}
    assert db.count() == 2


@pytest.mark.asyncio
async def test_connect_requires_user_provided_credentials(monkeypatch):
    monkeypatch.delenv("TG_API_ID", raising=False)
    monkeypatch.delenv("TG_API_HASH", raising=False)

    with pytest.raises(click.ClickException, match="Missing Telegram app credentials"):
        async with connect():
            pass
