---
name: rizamo
description: Publish and schedule social media posts on Instagram, TikTok, LinkedIn, Facebook, YouTube and Threads with Rizamo, see how they did, and answer comments and messages. Use when the user wants to post or schedule social content, check post or account analytics, or reply to their audience.
metadata:
  openclaw:
    envVars:
      - name: RIZAMO_API_KEY
        required: false
        description: Rizamo API key for the REST API, created in Rizamo under Developers. Not needed when the Rizamo MCP server is connected.
    homepage: https://docs.rizamo.com/connect-an-agent
---

# Rizamo

Rizamo publishes to a team's social accounts, grouped in profiles (one per brand or client, each with its own accounts, queue and time zone). Two ways in:

- **MCP (preferred when your client supports remote MCP servers):** `https://mcp.rizamo.com/mcp`, streamable HTTP. The user signs in with OAuth and chooses the profiles you can reach. Its tools follow the steps below by name (`list_accounts`, `create_media`, `validate_post`, `create_post`, `publish_post`, `get_post`, `get_analytics`, `list_threads`, `reply_to_thread`). In OpenClaw, `openclaw plugins install clawhub:rizamo-mcp` adds the server; the user signs in under Settings, MCP.
- **REST API:** `https://api.rizamo.com/v1` with `Authorization: Bearer $RIZAMO_API_KEY`. The user creates the key in Rizamo under Developers (it starts with `rz_live_`). Reference: https://docs.rizamo.com/api

The user needs a Rizamo account (free for two social accounts) with at least one account connected.

## Rules

- **Ask first.** Show the user what you will publish, reply, delete or connect, and wait for their yes, unless they told you to act on your own. Create posts as drafts until then.
- **Only the user's own audience.** Publish what the user asked for to the accounts they connected. Never use Rizamo for spam, unsolicited messages, fake engagement or bulk posting the user has not reviewed.
- **TikTok has no defaults.** Before each TikTok post, read the account's creator info and ask the user every choice it lists (privacy for photos, comments, Duet, Stitch, promotional content, paid partnership, AI-generated). Set `consent` only after the user agreed to TikTok's Music Usage Confirmation.
- **Writes are safe to retry.** Send a new `Idempotency-Key` (a UUID) with each write; after a timeout, send the same request with the same key.
- Times are ISO 8601 in UTC. Queue times are in the profile's time zone.
- Errors answer `{ "code", "status", "message" }`; the message says what to change.

## Publish or schedule a post

1. Find the profile and its accounts: `GET /profiles`, then `GET /accounts?profileId=<id>`.
2. Add each image or video Rizamo can download: `POST /media` with `{ "url": "https://..." }`. Keep `media.id`.
3. For a TikTok account: `GET /accounts/<id>/tiktok/creator-info` and ask the user the choices.
4. Check it: `POST /posts/validate` with the post below. Fix every `problems` entry; `warnings` would stop it later.
5. Create it as a draft:

   ```sh
   curl https://api.rizamo.com/v1/posts \
     -H "Authorization: Bearer $RIZAMO_API_KEY" \
     -H "Idempotency-Key: $(uuidgen)" \
     -H "Content-Type: application/json" \
     -d '{
       "profileId": "prof_...",
       "text": "Our autumn menu is here.",
       "targets": [{ "accountId": "acc_..." }],
       "mediaIds": ["med_..."],
       "status": "draft"
     }'
   ```

   To schedule instead: `"status": "scheduled", "scheduledAt": "2026-12-01T09:00:00Z"`. For the profile's next free posting time: `"status": "scheduled", "queue": true` (never with `scheduledAt`). A target can carry its own `text`, `mediaIds`, `format` and network `options` (TikTok's choices go in `options.tiktok`).
6. After the user's yes: `POST /posts/<id>/publish` publishes now; a scheduled post goes out by itself.
7. Follow it: `GET /posts/<id>`. Each target has its own `status` and, once live, its `url`. `GET /events?resourceId=<post id>` says why a target failed.

## See how posts did

- `GET /analytics/overview?days=30`: views, reach, engagements and followers against the period before, by day and network, with the top posts. Add `profileId` for one brand.
- `GET /analytics/posts?days=30&sort=views`: every post of the period, ranked.

## Answer comments and messages

1. `GET /inbox/threads?status=open` lists open comment and message threads.
2. `GET /inbox/threads/<id>` reads one with its messages.
3. After the user approves the text: `POST /inbox/threads/<id>/messages` with `{ "text": "..." }`.
4. `PATCH /inbox/threads/<id>` with `{ "status": "done" }` closes it.

## Regular reports and checks

When the user asks for something on a schedule ("every Monday, send me last week's results", "every morning, tell me what needs a reply"), set it up with your own scheduler, such as OpenClaw's automations; Rizamo sends no reports itself. On each run:

- Results: `GET /analytics/overview?days=7` (`get_analytics`): views against the week before, then the top three posts and anything that dropped.
- Inbox: `GET /inbox/threads?status=open` (`list_threads`): how many threads are open and which wait longest. Draft replies, but send none without the user's yes.
- Keep it to a few lines, and send it where the user asked (the chat, WhatsApp, Telegram).

## Short links

`POST /links` with `{ "url": "https://...", "utm": { "source": "instagram", "campaign": "autumn" } }` returns a `shortUrl` that counts its clicks; `GET /links/<id>` shows them by day and country.
