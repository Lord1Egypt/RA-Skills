---
name: website-monitoring
description: Creates and manages website-change monitors via the Crawlora API — watch a page for a content change or a sitemap for added/removed URLs, and get a signed webhook the moment something changes. No polling loop or diffing pipeline to run yourself. Use when the user wants to track a competitor's pricing page, watch for new pages on a site, get notified when content changes, or otherwise avoid re-checking a URL by hand.
---

# Website change monitoring

Create, list, update, and delete monitors that watch a URL (exact content
diff) or a sitemap (added/removed URL tracking) on a schedule, with signed
webhook delivery on change — all as normalized JSON from the Crawlora API,
with no polling loop or diffing logic of your own to write.

## When to use this skill

- "Watch this page and tell me when it changes." / "Track this competitor's
  pricing page."
- "Alert me when new pages get added to this site" (sitemap mode).
- "List my active monitors." / "Pause/update/delete this monitor."
- "Show me this monitor's recent check history" — did it run, did it find a
  change, did the webhook deliver.
- Anything that would otherwise mean writing your own cron job + diffing +
  notification pipeline for "let me know when X changes."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Create** — `POST /monitors` with `url`, `cadence_minutes` (5 to
   10080, i.e. 5 minutes to 7 days), and optionally `target_type`
   (`page`, the default — exact SHA-256 content-fingerprint diff — or
   `sitemap`, which tracks a sitemap's `<loc>` entries for additions and
   removals, with optional `sitemap.include_patterns`/`exclude_patterns`
   glob filters and `sitemap.max_urls`). Add `notification.webhook_url`
   (must be `https` and resolve to a public address) and an optional
   `notification.webhook_secret` to get a signed delivery on change.
   `notification.events` opts into `change.detected` (default — fires only
   when a check finds a difference) and/or `run.completed` (fires on every
   completed run, a heartbeat for a "last checked" UI).
2. **List / get** — `GET /monitors` lists the caller's own monitors (newest
   first, capped at 100, free to call); `GET /monitors/{id}` fetches one.
3. **Update** — `PATCH /monitors/{id}` partially updates a monitor (free to
   call). Changing `target_type` or `sitemap` resets the stored diff
   baseline (fingerprint, snapshot, or URL set), so the next check starts
   fresh rather than comparing against the old target's state.
4. **Delete** — `DELETE /monitors/{id}` removes a monitor.
5. **Check history** — `GET /monitors/{id}/checks` lists the monitor's most
   recent check runs (newest first, capped at 50), including per-run
   webhook delivery status — use this to debug "why didn't I get notified."
6. **Verify webhook deliveries** — every delivery carries an
   `X-Crawlora-Signature: t=<unix>,v1=<hmac-hex>` header, an HMAC-SHA256
   digest of `"{t}.{rawBody}"` keyed by your `webhook_secret`. Recompute it
   and reject stale timestamps to guard against replay.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Create a page monitor with a webhook:
scripts/crawlora.sh -X POST /monitors '{
  "url": "https://example.com/pricing",
  "cadence_minutes": 60,
  "name": "Pricing page",
  "notification": {"webhook_url": "https://example.com/webhooks/crawlora"}
}' | jq '.'

# Create a sitemap monitor (new/removed pages):
scripts/crawlora.sh -X POST /monitors '{
  "url": "https://example.com/sitemap.xml",
  "target_type": "sitemap",
  "cadence_minutes": 1440
}' | jq '.'

# List monitors:
scripts/crawlora.sh /monitors | jq '.'

# Check one monitor's recent runs:
scripts/crawlora.sh /monitors/mon_abc123/checks | jq '.'

# Pause a monitor:
scripts/crawlora.sh -X PATCH /monitors/mon_abc123 '{"enabled": false}' | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Monitors
endpoint this skill uses (method, path, params, description).

## Examples

- **Competitor pricing watch:** `POST /monitors` on a competitor's pricing
  page with `notification.events: ["change.detected"]`, then poll
  `/monitors/{id}/checks` (or just wait for the webhook) to see when it
  actually changes.
- **New-page discovery:** `target_type: "sitemap"` on a site's sitemap URL
  to get notified when a new product/blog page goes live, without crawling
  the whole site yourself.
- **"Is my monitor actually working?"** — `GET /monitors/{id}/checks` shows
  whether recent runs completed, found a change, and whether the webhook
  delivered — the fastest way to debug a monitor that "should have fired."

## Notes & limits

- **Credits / pay-on-success:** management calls (create, list, get, update,
  delete) are **free**; only checks are billed. Free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode,
  query-param, or commit it. Always verify the webhook signature before
  trusting a delivery's payload.
- **Public data only** — a monitor watches a publicly-reachable URL; it
  can't authenticate into a page behind a login.
- **`cadence_minutes` range is 5 to 10080** (5 minutes to 7 days) — pick the
  cadence that matches how often the target actually changes; a tighter
  cadence than needed just burns checks faster.
- Every request scopes to the caller's own API key — there's no
  cross-account listing or lookup.
