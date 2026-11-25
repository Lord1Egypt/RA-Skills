---
name: socialmcp
description: Schedule and publish posts to X and LinkedIn through SocialMCP's hosted MCP server, with one social media calendar. Use when the person wants to post, schedule, plan, edit, reschedule or cancel social media posts, write X threads or LinkedIn posts, fill their posting slots, or see what is scheduled or already published.
license: MIT
compatibility: Needs network access and the SocialMCP MCP server (https://getsocialmcp.com/mcp, Streamable HTTP, OAuth sign-in).
metadata:
  homepage: https://getsocialmcp.com
  author: XVELOPERS LTD.
  version: 1.0.0
---

# SocialMCP

SocialMCP is a social media calendar for X and LinkedIn with a hosted MCP server. Once it's connected, you can write, check, schedule and publish posts for the person, and every post shows up on their SocialMCP calendar at https://getsocialmcp.com/app.

## Connect the server (once)

The server is `https://getsocialmcp.com/mcp` (Streamable HTTP). Sign-in is OAuth: the person signs in to SocialMCP in their browser and clicks **Allow**. There is no API key. They need a SocialMCP account (free to start at https://getsocialmcp.com/signup) with an X account or LinkedIn profile connected.

If the SocialMCP tools (`get_account`, `create_post`…) aren't available yet, help the person connect:

**OpenClaw**

```bash
openclaw mcp add socialmcp --url https://getsocialmcp.com/mcp --transport streamable-http --auth oauth
openclaw mcp login socialmcp
```

- If the Gateway is running and `add` refuses to probe, add `--no-probe`.
- Or in the Control UI: Settings → MCP → Add server → Streamable HTTP → `https://getsocialmcp.com/mcp`, then **Sign in**.
- On a VPS without a public HTTPS origin, the browser ends on a failed `127.0.0.1` page after **Allow**. Copy that whole URL and run `openclaw mcp login socialmcp --callback-url '<that URL>'`.

**Hermes Agent**

```bash
hermes mcp add socialmcp --url https://getsocialmcp.com/mcp --auth oauth
hermes mcp login socialmcp
```

- Run `hermes mcp login` in its own terminal, then `/reload-mcp` in the session.
- On a remote machine, paste the failed redirect URL back into Hermes when it asks, or use an SSH tunnel to the callback port it prints.

**Any other MCP client**: add a remote server named `socialmcp` with URL `https://getsocialmcp.com/mcp` and OAuth. Guides for each agent: https://getsocialmcp.com/docs/mcp

## Start here

1. Call `get_account` first. It returns the connected accounts (with each X account's `character_limit`), the person's timezone and current time, their posting slots, settings, and plan limits and usage.
2. If the network they want isn't connected, call `connect_account` and give them the link.
3. Times without an offset are in the person's timezone. Say times back to them in their timezone.

## Posting well

- **Confirm before anything goes out.** Show the final text, the networks and the time, and wait for a yes before `create_post`. `create_post` without a time publishes immediately, and SocialMCP can't remove a published post from the networks.
- **Check first.** `check_post` shows exactly what each network gets, the character counts and whether the plan has room, without posting. If a day is full, it suggests the next time with room.
- **X**: each account's `character_limit` is 280, or 25,000 with an X subscription. X counts links as 23 characters and CJK characters and emoji as 2. Longer text goes out as a thread: pass `parts`, one item per post.
- **LinkedIn**: one post, up to 3,000 characters. Thread parts are combined there.
- **Write for each network** rather than pasting the same text: a punchy thread on X, one fuller post on LinkedIn. Use `overrides` for a network-specific version.
- **Posting slots**: `posting_time: "next"` puts the post in the next open slot of each account. Set or change the slots with `set_posting_times`.
- **Images**: `upload_image` from an https URL or base64 returns a `media_id` to attach.
- **Retries**: send the same `idempotency_key` when retrying `create_post`, so nothing posts twice.
- **When something doesn't fit**, nothing is posted and the error code says why (for example `daily_limit` with a suggested time). Tell the person plainly and offer the suggested time.

## Changing plans

- `list_posts` finds posts by date range or status, `get_post` shows one with its live links.
- `update_post` edits the text or time of a post that hasn't gone out.
- `cancel_post` stops a scheduled post. `delete_post` removes a post from SocialMCP only, not from the networks.
- `retry_post` posts again to the networks where a post failed.
- `open_dashboard` gives a signed-in link to the calendar or one post.

## Examples

- "Post what I shipped today to X and LinkedIn, tomorrow at 9am."
- "Turn this changelog into an X thread for Monday morning."
- "What do I have scheduled this week?"
- "Move my next post to Friday afternoon." / "Cancel the post about the launch."
