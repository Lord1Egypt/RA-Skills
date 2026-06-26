#!/usr/bin/env python3
"""Telegram Autopilot — AI-powered auto-reply for personal accounts."""

import argparse
import asyncio
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

from telethon import TelegramClient, events


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def load_config(path):
    with open(path) as f:
        return json.load(f)


def load_history(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save_history(path, history):
    with open(path, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


async def notify(config, text):
    """Send notification to owner via Telegram bot."""
    notif = config.get("notifications", {})
    token = notif.get("bot_token")
    chat_id = notif.get("chat_id")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        log(f"Notify error: {e}")


async def generate_reply(config, sender_name, sender_username, message_text, history):
    """Generate AI reply using configured provider."""
    ai = config["ai"]
    contact = config["contacts"].get(sender_username, {})
    owner = config.get("owner", {})
    language = contact.get("language", "en")
    tone = contact.get("tone", "friendly")

    tone_desc = {
        "friendly": "friendly and direct",
        "formal": "formal and professional",
        "brief": "very brief and concise"
    }.get(tone, "friendly and direct")

    lang_desc = {"it": "Italian", "en": "English", "es": "Spanish", "fr": "French", "de": "German"}.get(language, language)

    recent = history.get(sender_username, [])[-10:]

    messages = [
        {
            "role": "user",
            "content": (
                f"[SYSTEM] You are {owner.get('name', 'the account owner')}. "
                f"{owner.get('bio', '')} "
                f"You're chatting on Telegram with {sender_name}.\n\n"
                f"Tone: {tone_desc}. Language: {lang_desc}.\n"
                f"Write short messages (1-2 sentences) like a real chat.\n"
                f"NEVER invent facts. If asked to confirm something you don't know, "
                f"say you'll check later.\n"
                f"If directly asked whether you are AI, be honest.\n"
                f"Reply ONLY with the message text."
            ),
        },
        {"role": "assistant", "content": "Understood, I'll respond naturally."},
    ]

    for entry in recent:
        messages.append({"role": entry["role"], "content": entry["text"]})
    messages.append({"role": "user", "content": message_text})

    if ai["provider"] == "anthropic":
        payload = json.dumps({
            "model": ai["model"],
            "max_tokens": ai.get("max_tokens", 300),
            "messages": messages,
        }).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": ai["api_key"],
                "anthropic-version": "2023-06-01",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["content"][0]["text"].strip()
    else:
        # OpenAI-compatible (Taalas, Novita, OpenAI, etc.)
        payload = json.dumps({
            "model": ai["model"],
            "messages": messages,
            "max_tokens": ai.get("max_tokens", 300),
            "temperature": ai.get("temperature", 0.7),
        }).encode()
        headers = {"Content-Type": "application/json"}
        if ai.get("api_key"):
            headers["Authorization"] = f"Bearer {ai['api_key']}"
        req = urllib.request.Request(ai.get("base_url", "https://api.openai.com/v1/chat/completions"), data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"].strip()


async def main(args):
    config = load_config(args.config)
    workdir = os.path.dirname(os.path.abspath(args.config))
    history_path = os.path.join(workdir, "conversations.json")
    history = load_history(history_path)

    session_path = os.path.join(workdir, args.session)
    client = TelegramClient(session_path, args.api_id, args.api_hash)
    await client.start()
    me = await client.get_me()
    log(f"Autopilot ONLINE — {me.first_name} (@{me.username})")

    contacts = config.get("contacts", {})
    allowed_ids = {v["id"]: k for k, v in contacts.items() if "id" in v}

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        if not event.is_private:
            return

        sender = await event.get_sender()
        if not sender or not sender.username:
            return

        username = sender.username.lower()
        sender_id = sender.id

        if username not in contacts and sender_id not in allowed_ids:
            return

        if username in contacts:
            contact_cfg = contacts[username]
        else:
            uname = allowed_ids[sender_id]
            contact_cfg = contacts[uname]
            username = uname

        msg_text = event.message.text
        if not msg_text:
            return

        sender_name = contact_cfg.get("name", sender.first_name or username)
        log(f"MSG from {sender_name} (@{username}): {msg_text[:100]}")

        await notify(config, f"🤖 <b>Autopilot</b>\nFrom: {sender_name}\nMsg: {msg_text[:200]}")

        if username not in history:
            history[username] = []
        history[username].append({"role": "user", "text": msg_text, "ts": datetime.now(timezone.utc).isoformat()})

        # Mark as read
        await client.send_read_acknowledge(event.chat_id, event.message)
        await asyncio.sleep(2)

        try:
            reply = await generate_reply(config, sender_name, username, msg_text, history)
        except Exception as e:
            log(f"AI error: {e}")
            return

        if not reply:
            return

        # Typing simulation
        async with client.action(event.chat_id, "typing"):
            await asyncio.sleep(min(len(reply) * 0.05, 5))

        await client.send_message(event.chat_id, reply)
        log(f"REPLY to {sender_name}: {reply[:100]}")

        history[username].append({"role": "assistant", "text": reply, "ts": datetime.now(timezone.utc).isoformat()})
        if len(history[username]) > 50:
            history[username] = history[username][-30:]
        save_history(history_path, history)

        await notify(config, f"💬 <b>Reply</b> to {sender_name}:\n{reply[:200]}")

    log("Listening for messages...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Telegram Autopilot")
    p.add_argument("--config", required=True, help="Path to config.json")
    p.add_argument("--session", default="user", help="Session file name")
    p.add_argument("--api-id", type=int, required=True)
    p.add_argument("--api-hash", required=True)
    args = p.parse_args()
    asyncio.run(main(args))
