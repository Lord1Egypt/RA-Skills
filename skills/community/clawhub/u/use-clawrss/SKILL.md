---
name: use-clawrss
description: Use the ClawRSS OpenClaw plugin to manage RSS feeds, persist web results, pull saved items, work with digest articles, and send Apple push notifications after the plugin is installed and enabled.
metadata:
  openclaw:
    always: true
    requires:
      config:
        - plugins.entries.clawrss.enabled
---

# Use ClawRSS

Use this skill when the user wants to work with ClawRSS after the plugin is installed.

Typical requests:

- add, list, or remove RSS feeds
- search the web and save results into ClawRSS
- pull saved RSS/article items and mark a cursor consumed
- save, list, read, or push digest articles
- send a short Apple push notification through the configured ClawRSS push target

## Required workspace rule

ClawRSS is workspace-based.

- Reuse the exact workspace ID as `namespace` for every ClawRSS tool call.
- For `openclaw_rss_pull` and `openclaw_rss_mark`, use that same value as both `namespace` and `consumer`.
- If the workspace ID is missing and cannot be inferred from the current ClawRSS context, ask for it before writing.

## Tool mapping

Use these tools for the matching data type:

- feeds: `openclaw_rss_upsert_feed`, `openclaw_rss_list_feeds`, `openclaw_rss_delete_feed`
- web results and article records: `web_search`, `openclaw_rss_ingest`, `openclaw_rss_pull`, `openclaw_rss_mark`
- digests: `openclaw_rss_save_digest`, `openclaw_rss_pull_digests`, `openclaw_rss_get_digest`, `openclaw_push_notify_digest`
- generic push: `openclaw_push_get_status`, `openclaw_push_notify`

Do not confuse feeds, article records, and digest records.

- Do not call only `openclaw_rss_ingest` and then say a feed was subscribed.
- Do not use `openclaw_rss_save_digest` for normal article search results.
- Do not claim push delivery succeeded if push is not configured.

## Feed workflow

For add or subscribe requests:

1. Determine the real RSS or Atom feed URL.
2. Call `openclaw_rss_upsert_feed`.
3. Call `openclaw_rss_list_feeds` with the same `namespace`.
4. Confirm success only if the feed appears in the list result.

For remove requests:

1. Use the exact stored feed URL when possible.
2. Call `openclaw_rss_delete_feed`.
3. Re-list feeds if the user expects verification.

If the user gives only a normal website page and you cannot confirm a real feed URL, say it was not subscribed yet.

## Search plus persistence workflow

For latest, trending, breaking, or web-fresh information:

1. Search the web first.
2. Normalize results into `title`, `url`, `kind`, `snippet`, and optional `sourceHost`, `score`, `publishedAt`.
3. Default `kind` to `article`. Use `rss` only for confirmed feed URLs.
4. Call `openclaw_rss_ingest`.
5. If the user also wants to follow a confirmed feed URL, separately call `openclaw_rss_upsert_feed`.

## Pull and mark workflow

For sync or "show what is stored" requests:

- Call `openclaw_rss_pull` with the workspace as both `namespace` and `consumer`.
- Use `cursor = null` unless the user provides a checkpoint.
- Use `kind = "all"` unless the user explicitly wants only `rss` or only `article`.

For acknowledge or completion requests:

- Call `openclaw_rss_mark` only when the user wants to mark a pulled cursor as consumed.
- Reuse the same workspace value as both `namespace` and `consumer`.

## Digest workflow

For summaries or scheduled reports:

1. Call `openclaw_rss_save_digest` with `jobID`, `scheduledFor`, `title`, `bodyRaw`, and `bodyFormat`.
2. Use `openclaw_rss_pull_digests` to list saved digests.
3. Use `openclaw_rss_get_digest` to read a specific digest.
4. Use `openclaw_push_notify_digest` when the user wants the saved digest delivered.

Default digest delivery to `background_then_alert` unless the user explicitly asks for only `background` or only `alert`.

## Generic push workflow

Use `openclaw_push_notify` only for short manual notifications or task completion notices.

- Keep title and body brief and factual.
- If configuration is uncertain, check `openclaw_push_get_status` first.
- Prefer `openclaw_push_notify_digest` when the notification is about a stored digest article.

## Response contract

When you finish, report:

- workspace used
- tools called
- what was saved, updated, deleted, pulled, marked, or pushed
- what was verified
- any missing user input still required

## If the plugin is missing

If the ClawRSS tools are unavailable, tell the user to install or enable the ClawRSS plugin first. Use the standalone `install-clawrss` skill when available.
