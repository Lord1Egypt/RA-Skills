"""Which chat a widget goes to.

The agent frameworks expose the current conversation differently:

- Hermes Agent sets HERMES_SESSION_PLATFORM / HERMES_SESSION_CHAT_ID /
  HERMES_SESSION_THREAD_ID in the terminal tool's environment, and does not
  show the chat id in the prompt of a private chat.
- OpenClaw shows "chat_id": "telegram:<id>" (":topic:<n>" in forum topics) in
  the conversation info of every turn; the model passes it to --chat-id.
  OPENCLAW_CHANNEL_CONTEXT is read too, for channels that set it.

When the framework says what the current conversation is, a widget may only go
there: an explicit --chat-id that names another chat is refused.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, replace
from typing import Optional

_REF = re.compile(r"^(?:telegram:|tg:)?(-?\d+|@[A-Za-z0-9_]{4,})(?::(?:topic|direct-topic):(\d+))?$")


class TargetError(ValueError):
    pass


@dataclass
class Target:
    chat_id: str
    thread_id: Optional[int] = None
    source: str = "argument"

    @property
    def is_private(self) -> bool:
        # user ids are positive; groups and channels are negative, @names are public chats
        return bool(re.fullmatch(r"\d+", self.chat_id))

    def api_chat_id(self):
        return int(self.chat_id) if re.fullmatch(r"-?\d+", self.chat_id) else self.chat_id


def parse_ref(ref: str) -> Target:
    m = _REF.match(ref.strip())
    if not m:
        raise TargetError("cannot read chat id %r (expected a number or telegram:<id>)" % ref)
    return Target(m.group(1), int(m.group(2)) if m.group(2) else None)


def _session_chat() -> Optional[Target]:
    chat = os.environ.get("HERMES_SESSION_CHAT_ID", "").strip()
    if chat:
        thread = os.environ.get("HERMES_SESSION_THREAD_ID", "").strip()
        t = parse_ref(chat)
        t.thread_id = t.thread_id or (int(thread) if thread.isdigit() else None)
        t.source = "HERMES_SESSION_CHAT_ID"
        return t
    raw = os.environ.get("OPENCLAW_CHANNEL_CONTEXT", "").strip()
    if raw:
        try:
            chat_id = (json.loads(raw).get("chat") or {}).get("id")
        except (ValueError, AttributeError):
            chat_id = None
        if chat_id is not None:
            t = parse_ref(str(chat_id))
            t.source = "OPENCLAW_CHANNEL_CONTEXT"
            return t
    return None


def resolve(chat_arg: Optional[str], thread_arg: Optional[int] = None) -> Target:
    platform = os.environ.get("HERMES_SESSION_PLATFORM", "").strip().lower()
    if platform and platform != "telegram":
        raise TargetError("this conversation is on %s, not Telegram: widgets only exist in Telegram" % platform)

    session = _session_chat()
    explicit = (chat_arg or "").strip() or os.environ.get("TG_WIDGETS_CHAT_ID", "").strip()
    if explicit:
        target = parse_ref(explicit)
        if session and target.chat_id != session.chat_id:
            raise TargetError("chat %s is not the current conversation (%s from %s): a widget only goes to "
                              "the user you are talking to" % (target.chat_id, session.chat_id, session.source))
        if session and target.thread_id is None:
            target.thread_id = session.thread_id
    elif session:
        target = replace(session)  # a copy: --thread-id must not rewrite the session itself
    else:
        raise TargetError("no chat id: pass --chat-id (the private chat with the user, e.g. telegram:123456)")
    if thread_arg is not None:
        target.thread_id = thread_arg
    # Hermes says which topic the conversation is in (none when HERMES_SESSION_THREAD_ID is
    # empty), so the topic is part of "the current conversation" there too.
    if session and session.source == "HERMES_SESSION_CHAT_ID" and target.thread_id != session.thread_id:
        raise TargetError("topic %s is not the current conversation's topic (%s from HERMES_SESSION_THREAD_ID)"
                          % (target.thread_id, session.thread_id or "none"))
    return target
