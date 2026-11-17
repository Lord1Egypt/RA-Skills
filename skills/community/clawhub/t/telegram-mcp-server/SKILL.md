---
name: telegram-mcp-server
description: Use when calling, operating, or diagnosing the telegram-mcp MCP server (a Telethon/MTProto user-account server, not the Bot API) — making list_chats/get_messages/send_message/wait_for_settled_message calls, an MCP tool call errors or times out, the server appears "sleeping"/unregistered, a Telethon session is invalid or expired, or you need to select or switch between multiple TELEGRAM_SESSION_STRING accounts.
---

# Operating the telegram-mcp Server

## Overview

`telegram-mcp` is an MCP server (backed by Telethon/MTProto) that exposes a **real Telegram user account** as stateless tools — not a bot, no bot token, no Bot API. This skill covers one thing: **how to make a successful call to that server and know it worked** — lifecycle, diagnostics, auth, multi-account. It has no opinion on monitoring flows or reply voice.

OpenClaw owns the server's stdio child process like any `mcp.servers` entry: it launches lazily on the first tool call and reaps it after `mcp.sessionIdleTtlMs` idle (default 10 min). "Sleeping" is normal — the next call respawns it transparently. **Never** run `uv run main.py &`, `pkill`, or any manual process command against it — that fights OpenClaw's supervision and can leave a second conflicting Telethon session logged in under the same account.

## Making a call (do this first)

**Just call it.** Call `mcp__telegram-mcp__list_chats`. If the server was idle, the first call may take a moment to respawn — that's expected, don't retry-loop on it. Once it succeeds, proceed with whatever you were doing; don't re-run diagnostics mid-turn after a success.

## When a call errors — diagnose, don't guess

Run these in order (via your exec tool). Read structured output, not free text.

1. `openclaw mcp status telegram-mcp --verbose` — static, read-only, opens no connection. Tells you whether the server is registered under `mcp.servers` in `openclaw.json` and whether it's enabled.
2. `openclaw mcp doctor telegram-mcp --probe --json` — actually connects and returns a structured `issues` list. Read `issues`.

Then match the failure:

| Symptom | Meaning | Action |
|---|---|---|
| Not registered at all | Operator setup gap | Report the exact missing piece + the one-time `openclaw mcp add` (below). Don't invent a path or silently patch. |
| Registered, `doctor --probe` reports a config issue (bad command, missing cwd, disabled) | Config problem | Report the specific issue text. Don't patch blindly. |
| `status`/`doctor` are clean but the tool call still errors with an auth failure | Telethon session invalid/expired | Cannot be fixed from here — needs a human-run QR login. See Auth below. |

**Registration command** (only report it — don't run it for the operator):
```
openclaw mcp add telegram-mcp --command uv \
  --arg --directory --arg <path-to-telegram-mcp> --arg run --arg main.py
```
plus the required env: `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, and a session string (see Auth). Don't invent a path you don't actually know.

## Auth failure (the one thing you can't fix)

A Telethon session string that is invalid or expired won't show up in `doctor`'s static checks — `doctor` doesn't understand Telegram app-level auth, so it only surfaces as an error from the real tool call. Generating a new session string requires an **interactive QR login in a real, human-attended terminal**:

```
uv run session_string_generator.py --qr
```

This cannot be scripted, piped, or run through a non-TTY automation shell. Tell the user precisely that; do **not** attempt to run the generator or edit the session string yourself, and never expose a session string or API key in output.

## Multi-account

The server never picks or remembers an "active" account — it just accepts an optional `account` param on every tool call once more than one `TELEGRAM_SESSION_STRING_<LABEL>` is configured in its env. Tracking "active" is a caller/plugin concern, not the server's.

- If your instruction context names an **active account label**, pass `account: "<that label>"` on every `list_chats`/`get_messages`/`wait_for_settled_message`/`send_message` call this turn. Don't switch labels mid-turn.
- `TELEGRAM_API_ID`/`TELEGRAM_API_HASH` are shared across all accounts (one app registration can log in as many accounts). Only the session string varies per label.
- To test one account's auth specifically, call `list_chats` once per configured account and report which succeed vs. error — plain `list_chats` only tests whichever account you happened to pass.
- Adding a brand-new account still requires the human-run QR login above — you cannot generate a session string yourself, for a first account or an additional one.

## Tool reference (prefix: `mcp__telegram-mcp__`)

| Tool | Purpose |
|---|---|
| `list_chats()` | List available chats/groups and their IDs (also the simplest connectivity/auth probe) |
| `get_messages(chat_id, limit)` | Read messages from a chat |
| `send_message(chat_id, text)` | Send a message as the account |
| `wait_for_settled_message(settle_ms=6000, max_wait_ms=50000)` | Wait for new messages arriving during the window, with debouncing — does **not** return pre-existing backlog |
| `search_messages(...)` / `search_global(...)` | Search message history |
| `get_chat(chat_id)` | Chat info |
| `get_history(chat_id, ...)` | Message history |

## Error handling

1. On an MCP tool error, retry at most once after a short delay, in the same turn.
2. Still failing → run the `status` / `doctor --probe` diagnosis above rather than looping or guessing.
3. Never expose the session string or API keys in any output or log.
