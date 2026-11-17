---
name: telethon-plus
description: HTTP + MCP control plane over a REAL Telegram MTProto userbot (Telethon), a full user account, not the Bot API. Send/read/edit/delete/forward messages, browse dialogs, resolve entities/contacts, download + send media, manage chats (create/join/leave/admin), run polls, and forward every incoming message to a webhook (TELETHON_POST_TO_URL). JSON in / JSON out on one port; MCP streamable-HTTP at /mcp/ mirrors the same tools; optional bearer auth. Built-in anti-flood throttling keeps the account under Telegram's limits. Use when the user wants an agent, script, or curl one-liner to drive their own Telegram account over HTTP/MCP (read a chat, DM someone, post to a channel, react/pin, or pipe incoming DMs into an app). Drives a real account acting AS the user with full account access.
homepage: https://github.com/psyb0t/docker-telethon-plus
user-invocable: true
metadata:
  { "openclaw": { "emoji": "✈️", "primaryEnv": "TELETHON_PLUS_URL", "requires": { "bins": ["docker", "curl"] } } }
permissions:
  shell: "setup-only: docker/curl for install, login, and container management (see references/setup.md); runtime API calls are plain HTTP, not shell"
  network: "outbound HTTP to $TELETHON_PLUS_URL (every API/MCP call), plus server-side fetch of caller-supplied file_url when present (POST /api/messages, send_file)"
  account_access: "full-access Telegram user account: read, write, and admin (not a sandboxed bot); every call acts as the account owner"
---

# telethon-plus

Your Telegram account behind an HTTP API. Wraps [Telethon](https://codeberg.org/Lonami/Telethon) (the real MTProto **userbot** client, a full user account, not the neutered Bot API) behind a JSON HTTP API and a Model Context Protocol endpoint. Same tool registry, two doors: `POST` JSON at `/api/...`, or point an MCP-aware agent at `/mcp/`. Either way it talks to Telegram **as you**, with full account access.

Capabilities:

- **Messages**: send text, send media from a URL, read history, fetch one message, edit, bulk-delete, forward, mark read.
- **Reactions / pins**: react with an emoji, remove a reaction, pin / unpin.
- **Dialogs / entities**: list your chats, resolve any `@username` / phone / `t.me` link / numeric ID to a profile, bulk-resolve.
- **Media**: download an attachment (raw bytes over HTTP, or base64 via MCP).
- **Chats**: create a supergroup/channel, delete one you own, join public / private-invite, leave, resolve a channel's linked discussion group, list participants.
- **Admin**: ban / unban / kick / promote / demote in groups you administer.
- **Polls**: create, vote, read results.
- **Incoming events**: every new message / edit / delete / chat action streamed over WebSocket **and** POSTed to your webhook (`TELETHON_POST_TO_URL`).
- **Health / throttle**: liveness, live rate-limit state, flood-risk tier, Prometheus metrics.

For installation, login, and container setup, see [references/setup.md](references/setup.md).

## Security & safety

- **Declared capabilities** (see `permissions:` in the frontmatter): `shell` (setup-only), `network` (runtime HTTP), and full Telegram account access. **Setup-only shell vs. runtime API is a hard line**: `docker run` / `docker compose` / `curl` in [references/setup.md](references/setup.md) are one-time operator commands to stand up the container; every runtime call this skill makes afterward is a plain HTTP request (`curl` as an HTTP client, or MCP), never a new shell/docker invocation against the host.
- **Outbound HTTP**: every API call is a `curl`/HTTP request to the `telethon-plus` server (`$TELETHON_PLUS_URL`), and the server itself makes outbound calls to Telegram's MTProto servers and, when `file_url` is used, to whatever URL is given (see the SSRF note below).
- **Drives a full-access Telegram user account**: read AND write AND admin, not a sandboxed bot. Any call this skill makes acts as the account owner (see "Authorized / responsible use" below for the account-level rules).
- **Destructive / admin operations require explicit user confirmation** naming the exact target (chat, message IDs, user) before running. See the per-endpoint warnings in the API tables below (`DELETE /api/chats`, ban/kick/promote, bulk `DELETE /api/messages`).
- **Deployment:** bind the server to `localhost`/loopback or put it behind TLS on a reverse proxy, set `TELETHON_AUTH_KEY` (empty = no auth, wide open), and never expose `/mcp/` or `/api/` to untrusted agents/networks. Either surface hands out full account control. See [references/setup.md](references/setup.md) for the full deployment + auth guidance.

## Authorized / responsible use

**This drives a REAL Telegram user account, not a bot.** Whoever holds the session string *is* the account owner: full read/write access to every DM, group, and channel that account can reach. Treat it like the account's password.

- Only ever point this skill at an instance **the user runs and owns**, driving **the user's own account** (or an account they are explicitly authorized to operate).
- **Do not** send spam, mass-DM strangers, scrape at volume, auto-join channels en masse, or run any automation that violates [Telegram's Terms of Service](https://telegram.org/tos). That gets the account **banned** (the throttle layer reduces flood risk, it does not make abuse safe).
- **Never** provision, escalate, or log in a new account from here. This skill is **consumer-only**: it talks to an already-running, already-authorized instance. First-time login is an operator-side step (see setup) and is out of scope for the agent.
- Writes are destructive and act as the user. `DELETE /api/chats` is irreversible; deleting / editing messages and banning users are visible actions others see. Confirm intent before running writes on shared chats.
- Never print, log, or echo the session string, `TELETHON_API_HASH`, `TELETHON_AUTH_KEY`, phone numbers, or message contents beyond what the task needs.

## When To Use

- Read recent messages from a chat, or search a chat's history.
- Send a DM, post to a channel/group, or drop a note in Saved Messages (`chat=me`).
- Send a file/photo to a chat by URL, or download an attachment someone sent.
- React to, pin, edit, forward, or delete messages.
- List the account's dialogs, resolve a handle to a profile, or list a group's members.
- Create / join / leave a chat; run group admin actions on chats the account administers.
- Create or tally a poll.
- Wire incoming Telegram messages into an app via the outbound webhook or the WS stream.

## When NOT To Use

- **You don't have an instance the user owns**: this is consumer-only; it never stands up or logs in an account.
- **Anything the user isn't authorized to do with that account**: spam, mass outreach, bulk scraping, ToS-violating automation.
- **Bot-API-style multi-tenant bots**: this is one user account per container, not a bot framework. If you need a bot token surface, use the Bot API instead.
- **Real-time streaming reads**: history reads are request/response. For live events use the WS stream or the webhook, not a poll loop.
- **Bulk resolving cold numeric IDs**: MTProto needs an `access_hash`. Numeric IDs only resolve for entities the session has already seen (via a prior `@username` / `t.me` lookup, a dialog list, or an incoming message). Resolve by `@username` first.

## Setup

The container should already be running and logged in (operator-side, see setup). Set the base URL:

```bash
export TELETHON_PLUS_URL=http://localhost:8080
```

If the server was started with `TELETHON_AUTH_KEY`, export it too. Every request except `/healthz` and `/metrics` then needs the bearer header:

```bash
export TELETHON_AUTH_KEY=<the-key>
# add to every call below:  -H "Authorization: Bearer $TELETHON_AUTH_KEY"
```

**Verify:**

```bash
curl -s $TELETHON_PLUS_URL/healthz
# {"status": "ok", "authorized": true}
```

If the session is dead (bad/revoked string, or Telegram unreachable) the container fails to start rather than booting with `authorized: false`. The process exits and `/healthz` never comes up. Check `docker logs` and re-login. `/healthz` is always public.

For install / first-time login / env vars / ports, see [references/setup.md](references/setup.md).

## Conventions

- **Response shape:** every 2xx returns the resource directly (no `{"result": ...}` envelope). Lists are JSON arrays, singles are JSON objects. Errors return `{"detail": ...}` (FastAPI standard).
- **Chat references** (`chat`, `from_chat`, `to_chat`) accept whatever Telethon accepts: `@username`, phone `+1234567890`, `https://t.me/name`, numeric ID `123456789`, supergroup/channel ID `-1001234567890`, or `me` (your Saved Messages). In `{chat}` path segments, phone and `t.me` links must be URL-encoded (`+` → `%2B`); usernames and IDs work inline.
- **Errors:** `400` bad JSON / validation / bad input · `401` missing-or-wrong bearer (only when `TELETHON_AUTH_KEY` set) · `403` write attempted in read-only mode · `404` unknown endpoint / admin action · `429` `FLOOD_WAIT` too long to sleep through, with `Retry-After` and body `{"detail": {"telegram_error": "FloodWaitError", "message": "...", "seconds": N}}`: wait that long before repeating the call · `502` any other Telegram RPC error, body `{"detail": {"telegram_error": "...", "message": "..."}}`.

## API: `GET /api/me`

The authorized account's own profile.

```bash
curl -s $TELETHON_PLUS_URL/api/me | jq
```

```json
{ "id": 123456789, "type": "User", "username": "someone", "first_name": "Some", "phone": "+..." }
```

## API: `GET /api/entities`

Resolve any chat reference to a full profile.

| Param | Type | Default | Notes |
|---|---|---|---|
| `chat` | string | required | `@username` / phone / `t.me` link / numeric ID |

```bash
curl -s "$TELETHON_PLUS_URL/api/entities?chat=@telegram" | jq
# { "id": 1234567, "type": "Channel", "username": "telegram", "title": "Telegram" }
```

## API: `POST /api/entities/bulk`

Resolve many references at once, honoring the resolve-username bucket.

| Field | Type | Default | Notes |
|---|---|---|---|
| `chats` | list[string] | required | References to resolve |

## API: `GET /api/dialogs`

List the account's dialogs, newest activity first.

| Param | Type | Default | Notes |
|---|---|---|---|
| `limit` | int | 20 | 1-200 |
| `archived` | bool | false | List archived chats instead of the main list |
| `search` | string | none | Case-insensitive substring on title / username |

```bash
curl -s "$TELETHON_PLUS_URL/api/dialogs?limit=10&archived=false" | jq
```

Each dialog carries `id`, `type`, `username`, `first_name`/`title`, `unread_count`, `pinned`, and a `last_message` object.

## API: `GET /api/messages`

Read recent messages from a chat (newest first).

| Param | Type | Default | Notes |
|---|---|---|---|
| `chat` | string | required | Chat to read from |
| `limit` | int | 20 | 1-200 |
| `offset_id` | int | 0 | Start before this message ID (pagination) |
| `search` | string | none | Full-text filter |

```bash
curl -s "$TELETHON_PLUS_URL/api/messages?chat=me&limit=5&search=hello" | jq
```

```json
[
  { "id": 4242, "date": "2026-04-29T12:00:00+00:00", "chat_id": 12345,
    "sender_id": 67890, "text": "hello", "out": false,
    "reply_to_msg_id": null, "media": false, "media_type": null }
]
```

Returns `[]` if nothing matches.

## API: `GET /api/messages/{id}`

Fetch a single message. `chat` is a required query param.

```bash
curl -s "$TELETHON_PLUS_URL/api/messages/4242?chat=me" | jq
```

## API: `POST /api/messages`

Send a message. **One endpoint, two flavors**: if the body has `file_url`, that URL is fetched and sent as media (with `text` as the caption); otherwise `text` is sent as a plain message.

> **SSRF note:** `file_url` is fetched **server-side**: the container makes the HTTP request, not the caller. An attacker-controlled `file_url` can be used to probe internal/private network addresses reachable from the container. **Don't pass arbitrary caller-supplied URLs through as `file_url`.** Restrict it to `https` scheme and a small set of trusted, publicly-known domains you control or explicitly trust. Never build `file_url` from untrusted input (a message someone else sent, a scraped page, an LLM-generated guess). **Prefer local file upload over server-side URL fetches**: fetch the file yourself (client-side, where you can validate it) and send it as a direct upload instead of handing the container a URL to fetch blind.

| Field | Type | Default | Notes |
|---|---|---|---|
| `chat` | string | required | Target chat |
| `text` | string | required if no `file_url` | Message text or caption (1-4096 chars) |
| `file_url` | string | null | HTTPS URL to fetch and send as media |
| `parse_mode` | string | null | `md` / `markdown` / `html` / null |
| `reply_to` | int | null | Message ID to reply to |
| `silent` | bool | false | Send without notification |
| `link_preview` | bool | true | Show link previews (text only) |
| `schedule` | string | null | Future ISO datetime to schedule the send |
| `force_document` | bool | false | With `file_url`: send as generic document |
| `max_bytes` | int | 52428800 | With `file_url`: reject files larger than this (max 2 GB) |

```bash
# Text.
curl -s -X POST $TELETHON_PLUS_URL/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"chat":"me","text":"**hello** from a container","parse_mode":"md","silent":true}' | jq

# Media from a URL (text becomes the caption).
curl -s -X POST $TELETHON_PLUS_URL/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"chat":"me","file_url":"https://example.com/photo.jpg","text":"a caption"}' | jq
```

Returns the created message object.

## API: `PATCH /api/messages/{id}`

Edit a message you sent. ID in the URL, rest in the body.

| Field | Type | Default | Notes |
|---|---|---|---|
| `chat` | string | required | Chat containing the message |
| `text` | string | required | New text (1-4096 chars) |
| `parse_mode` | string | null | `md` / `html` / null |
| `link_preview` | bool | true | Show link previews |

```bash
curl -s -X PATCH $TELETHON_PLUS_URL/api/messages/4242 \
  -H 'Content-Type: application/json' \
  -d '{"chat":"me","text":"fixed version","parse_mode":"md"}' | jq
```

## API: `DELETE /api/messages`

Bulk delete by ID (body carries the list).

| Field | Type | Default | Notes |
|---|---|---|---|
| `chat` | string | required | Chat containing the messages |
| `message_ids` | list[int] | required | IDs to delete (max 100) |
| `revoke` | bool | true | Delete for everyone, not just yourself |

> **Irreversible**, and with `revoke: true` (the default) it deletes for everyone in the chat, not just you. Confirm the exact `chat` and `message_ids` with the user before calling this on a shared chat.

```bash
curl -s -X DELETE $TELETHON_PLUS_URL/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"chat":"me","message_ids":[4242,4243],"revoke":true}' | jq
# { "deleted": 2, "requested": 2 }
```

## API: `POST /api/messages/forward`

| Field | Type | Default | Notes |
|---|---|---|---|
| `from_chat` | string | required | Source chat |
| `to_chat` | string | required | Destination chat |
| `message_ids` | list[int] | required | IDs to forward (max 100) |
| `silent` | bool | false | Forward without notification |

## API: `POST /api/messages/read`

Mark messages as read.

| Field | Type | Default | Notes |
|---|---|---|---|
| `chat` | string | required | Chat to mark read |
| `max_id` | int | 0 | Mark up to this message ID. `0` = all. |

```bash
curl -s -X POST $TELETHON_PLUS_URL/api/messages/read \
  -H 'Content-Type: application/json' -d '{"chat":"me","max_id":0}' | jq
# { "ok": true }
```

## API: `GET /api/messages/{id}/media`

Download a message's attachment as **raw bytes** (binary stream). `Content-Type` comes from Telegram; `Content-Disposition: attachment; filename=...` is set. `chat` is a required query param.

| Param | Type | Default | Notes |
|---|---|---|---|
| `chat` | string | required | Chat containing the message |
| `max_bytes` | int | 52428800 | Reject files larger than this |

```bash
curl -s "$TELETHON_PLUS_URL/api/messages/4242/media?chat=me" -o attachment.bin
```

MCP clients: use the `download_media` tool instead, which returns base64 in the JSON result.

## API: reactions & pins

| Method + path | Body / params | What it does |
|---|---|---|
| `POST /api/messages/{id}/reactions` | `chat`, `emoji`, `big?` | React to a message |
| `DELETE /api/messages/{id}/reactions` | `chat` | Remove your reaction |
| `POST /api/messages/{id}/pin` | `chat`, `silent?`, `pm_oneside?` | Pin |
| `POST /api/messages/{id}/unpin` | `chat` | Unpin |

```bash
curl -s -X POST $TELETHON_PLUS_URL/api/messages/4242/reactions \
  -H 'Content-Type: application/json' -d '{"chat":"me","emoji":"🔥"}' | jq
```

## API: `GET /api/participants`

List members of a group or channel.

| Param | Type | Default | Notes |
|---|---|---|---|
| `chat` | string | required | Group or channel |
| `limit` | int | 100 | 1-1000 |
| `search` | string | none | Filter by name |

Large public channels may return a limited set or require admin rights.

## API: chats

| Method + path | Body / params | What it does |
|---|---|---|
| `POST /api/chats` | `title`, `megagroup?` (default `true`) | Create a supergroup (`true`) or broadcast channel (`false`) |
| `DELETE /api/chats` | `chat` | Delete a supergroup/channel you own (**irreversible**) |
| `POST /api/chats/join` | `chat` | Join a public channel/group |
| `POST /api/chats/invite` | `invite` | Join a private chat via a `t.me/+hash` link |
| `POST /api/chats/leave` | `chat` | Leave a channel/group |
| `GET /api/chats/{chat}/linked` | none | Resolve a channel's linked discussion group |

> **Destructive.** `DELETE /api/chats` permanently deletes the chat for everyone in it and cannot be undone. Require explicit user confirmation naming the exact chat before calling it, and prefer leaving it disabled/unused unless the task genuinely needs it.

```bash
curl -s -X POST $TELETHON_PLUS_URL/api/chats \
  -H 'Content-Type: application/json' -d '{"title":"my-group","megagroup":true}' | jq
# { "id": 1234567890, "type": "Channel", "title": "my-group" }
```

## API: chat admin

`POST /api/chats/{chat}/admin/{action}` where `{action}` is one of `ban`, `unban`, `kick`, `promote`, `demote`. Requires admin rights in the chat.

| Action | Body | Notes |
|---|---|---|
| `ban` | `user`, `until_seconds?` | Ban; `until_seconds=0` = permanent (**visible, disruptive**) |
| `unban` | `user` | Lift a ban |
| `kick` | `user` | Ban + immediate unban (they can rejoin via invite). **Visible, disruptive.** |
| `promote` | `user`, `title?` (≤16 chars), plus booleans `change_info`, `post_messages`, `edit_messages`, `delete_messages`, `ban_users`, `invite_users`, `pin_messages`, `add_admins`, `anonymous`, `manage_call` (all default `false`) | Grant admin rights. Pass the specific booleans you want; at least one must be `true`, otherwise the call fails with `400` (use `demote` to strip rights). **Privilege escalation, irreversible without another admin demoting them back.** |
| `demote` | `user` | Strip admin rights |

> **Admin ops act on other people's membership/permissions and are visible to the whole chat.** Require explicit user confirmation naming the exact chat and target user before calling `ban`, `kick`, or `promote`.

```bash
curl -s -X POST "$TELETHON_PLUS_URL/api/chats/-1001234567890/admin/ban" \
  -H 'Content-Type: application/json' -d '{"user":"@baduser"}' | jq
```

## API: polls

| Method + path | Body / params | What it does |
|---|---|---|
| `POST /api/polls` | `chat`, `question`, `options`, `multiple_choice?`, `quiz?`, `correct_option?`, `solution?` | Create a poll |
| `POST /api/polls/{id}/vote` | `chat`, `options` (0-based indices) | Vote |
| `GET /api/polls/{id}/results` | `chat` | Current vote counts |

## API: status & observability

| Path | What it returns |
|---|---|
| `GET /healthz` | `{"status": "ok", "authorized": <bool>}`, always public |
| `GET /api/throttle/status` | Live bucket usage, adaptive multiplier, recent flood events, cache stats |
| `GET /api/account/health` | `{"authorized", "risk", "multiplier", "flood_events_1h", ...}`; `risk` is `ok` / `warning` / `high` |
| `GET /metrics` | Prometheus exposition (public even when auth is on) |

Every `/api/...` response also carries `X-Throttle-Multiplier`, `X-Throttle-Flood-Events-1h`, and `X-RateLimit-Remaining-<bucket>` headers, so clients can self-throttle without polling.

> The server ships **conservative anti-flood throttling** on by default (per-method token buckets, per-chat send/read intervals, global gap + jitter, adaptive backoff on `FLOOD_WAIT`, plus a persistent entity cache). If a call seems slow, it may be the throttle protecting the account. Check `GET /api/throttle/status`. Tuning the buckets is an operator concern (see setup); don't try to defeat them.

## Incoming-message webhook (`TELETHON_POST_TO_URL`)

> **Data exfiltration warning:** enabling `TELETHON_POST_TO_URL` forwards **every incoming Telegram event** (full message content, sender metadata, and account activity) to that external endpoint, for as long as the container runs. Point it ONLY at a trusted HTTPS endpoint you control. Anyone who controls that endpoint gets a live copy of everything the account receives.

When the operator sets `TELETHON_POST_TO_URL` on the server, **every incoming Telegram event** (new message, edit, delete, chat action) is `POST`ed to that URL as JSON (fire-and-forget, so a slow or failing webhook never blocks Telethon's loop). This is the way to pipe incoming DMs/messages into a separate app or worker that can't hold a WebSocket open.

Event payload:

```json
{
  "type": "NewMessage",
  "message": {
    "id": 4242, "date": "2026-04-29T12:00:00+00:00", "text": "hi",
    "out": false, "sender_id": 12345, "chat_id": -1001234567890,
    "reply_to_msg_id": null, "media": false, "media_type": null
  },
  "chat_id": -1001234567890
}
```

`type` is `NewMessage`, `MessageEdited`, `MessageDeleted`, or `ChatAction` (same shape, fewer fields on the non-message ones).

The same events also stream over **WebSocket** at `GET /ws/updates` (pass `?token=<TELETHON_AUTH_KEY>` when auth is on, since browsers can't set the Authorization header). Multiple subscribers each get their own queue of `TELETHON_UPDATES_BUFFER_SIZE` events (default 256). A client that falls that far behind is closed with code `1013`. Reconnect, then read what was missed with `GET /api/messages`. Server shutdown closes clients with `1001`. Updates are only registered when `TELETHON_UPDATES_ENABLED=true` (the default).

## MCP Endpoint

An MCP server is mounted at **`/mcp/`** using the [streamable HTTP transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http), on the same port as the HTTP API, behind the same bearer auth. It's **stateless**: every request is independent, no session juggling. Every tool in the registry (same names, same schemas as the endpoints above) is exposed automatically.

Point an MCP-aware agent at:

```
http://your-host:8080/mcp/
```

Wire into Claude Code:

```bash
claude mcp add --transport http telethon-plus $TELETHON_PLUS_URL/mcp/
# with auth:
claude mcp add --transport http telethon-plus $TELETHON_PLUS_URL/mcp/ \
  --header "Authorization: Bearer $TELETHON_AUTH_KEY"
```

The 34 tools, grouped: `get_me`, `get_entity`, `bulk_resolve`, `get_dialogs`, `get_messages`, `get_message`, `send_message`, `send_file`, `edit_message`, `delete_messages`, `forward_messages`, `mark_read`, `download_media`, `set_reaction`, `remove_reaction`, `pin_message`, `unpin_message`, `get_participants`, `create_group`, `delete_chat`, `join_chat`, `leave_chat`, `join_via_invite`, `get_linked_chat`, `ban_user`, `unban_user`, `kick_user`, `promote_user`, `demote_user`, `create_poll`, `vote_poll`, `get_poll_results`, `throttle_status`, `account_health`.

> `send_message` and `send_file` are separate MCP tools (the `POST /api/messages` route dispatches between them by whether `file_url` is present). `download_media` returns base64 in `data_base64` (the HTTP `/media` route streams raw bytes instead).

### Raw JSON-RPC

The transport requires `Accept: application/json, text/event-stream`. For debugging or non-MCP callers, hit it directly:

```bash
# tools/list
curl -s $TELETHON_PLUS_URL/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# tools/call: send a message
curl -s $TELETHON_PLUS_URL/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{
      "name":"send_message",
      "arguments":{"chat":"me","text":"hi from mcp"}
    }
  }'
```

MCP tool errors come back as an error result (`isError: true`) whose text is JSON, not as an HTTP status: read-only → `{"error":"read_only",...}`, long `FLOOD_WAIT` → `{"error":"flood_wait","seconds":N,...}` (wait that long), other Telegram RPC → `{"error":"telegram_rpc","type":...}`, bad args → `{"error":"invalid_argument",...}`.

## Bearer-Token Auth

If `TELETHON_AUTH_KEY` is set on the server, every route **except `/healthz` and `/metrics`** requires `Authorization: Bearer <key>` (constant-time compared). Missing/wrong → `401 {"detail":"unauthorized"}`. The WebSocket takes the key as `?token=`. Empty/unset key = wide open (fine on a private network); for untrusted networks pair the key with a reverse proxy doing TLS.

```bash
curl -s -H "Authorization: Bearer $TELETHON_AUTH_KEY" $TELETHON_PLUS_URL/api/me | jq
```

## Typical Workflows

### Read the latest from a chat

```bash
curl -s "$TELETHON_PLUS_URL/api/messages?chat=@somechannel&limit=10" \
  | jq -r '.[] | "\(.sender_id): \(.text)"'
```

### Send a DM / post to a channel

```bash
curl -s -X POST $TELETHON_PLUS_URL/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"chat":"@someone","text":"heads up, deploy is done"}' | jq
```

### Note to self (Saved Messages)

```bash
curl -s -X POST $TELETHON_PLUS_URL/api/messages \
  -H 'Content-Type: application/json' -d '{"chat":"me","text":"remember this"}' | jq
```

### Resolve-then-refer (numeric IDs need a warm session)

```bash
# Resolve by @username once (caches the access_hash) ...
curl -s "$TELETHON_PLUS_URL/api/entities?chat=@somebot" | jq .id
# ... then subsequent calls can use the numeric ID.
```

### Send → verify → clean up (self-test roundtrip)

```bash
MARKER="ping-$(date +%s)"
ID=$(curl -s -X POST $TELETHON_PLUS_URL/api/messages \
  -H 'Content-Type: application/json' \
  -d "{\"chat\":\"me\",\"text\":\"$MARKER\"}" | jq .id)

curl -s "$TELETHON_PLUS_URL/api/messages?chat=me&search=$MARKER" | jq -r '.[].text'

curl -s -X DELETE $TELETHON_PLUS_URL/api/messages \
  -H 'Content-Type: application/json' \
  -d "{\"chat\":\"me\",\"message_ids\":[$ID]}" | jq
```

### Check flood risk before a burst of writes

```bash
curl -s $TELETHON_PLUS_URL/api/account/health | jq '{risk, multiplier, flood_events_1h}'
# risk "ok" → go; "warning"/"high" → back off, the account is being rate-limited.
```

For a small send/read wrapper over `TELETHON_PLUS_URL`, see [`scripts/telethon.sh`](scripts/telethon.sh).
