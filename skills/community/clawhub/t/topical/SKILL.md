---
name: topical
description: Query Topical topic intelligence via MCP — breaking news, signals, trends, and source links from scheduled runs. Use for topic briefings, competitive intel, or monitoring updates.
homepage: https://usetopical.com
metadata: { "openclaw": { "requires": { "config": ["mcp.servers.topical"] } } }
---

# Topical intelligence (MCP)

Topical is **continuous intelligence infrastructure**: long-lived **topics** are monitored on a **schedule the user configures** in Topical (portal or product settings). Each completed pipeline run surfaces **breaking news**, **signals**, and **trends** drawn from ingested sources.

**You do not run the pipeline.** MCP tools read intelligence that Topical has already produced. When you call `get_topic_update` or `get_topic_narrative`, results are **current as of the last completed pipeline run** for that topic — not live web search. If nothing has changed since the user's last run, responses may be empty even though the wider web has moved on.

Tell the user when their briefing reflects a scheduled snapshot, especially if they expect up-to-the-minute news.

## OpenClaw integration

Full wiring (MCP + inbound webhooks) is a separate install flow:

1. Portal: **Settings → Connect OpenClaw** at `https://app.usetopical.com/portal/openclaw/`.
2. ClawHub: [topical](https://clawhub.ai/daveangelcode/skills/topical) · [topical-openclaw-setup](https://clawhub.ai/daveangelcode/skills/topical-openclaw-setup)
3. Skills: `openclaw skills install @daveangelcode/topical-openclaw-setup --global` then ask your agent to **set up Topical**.
4. Usage skill (this file): `openclaw skills install @daveangelcode/topical --global`

Hook transform assets live in `{baseDir}/assets/`. Payload reference: `{baseDir}/references/payloads.md`.

## Setup (once)

1. User creates an **Agent API key** in the Topical portal (**Settings → Agent API keys**, or the **Connect OpenClaw** wizard at `/portal/openclaw/`).
   Keys look like `agt_live_<uuid>_<secret>` (~89 chars); the embedded UUID is normal.
2. Wire MCP (prefer CLI over hand-editing JSON):

```bash
openclaw mcp set topical '{"url":"https://app.usetopical.com/api/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer <AGENT_API_KEY>"}}'
openclaw mcp probe topical
openclaw gateway restart
```

OAuth is for interactive clients; OpenClaw uses the long-lived Bearer token.

For **push delivery** (digests and event alerts), also complete the topical-openclaw-setup skill: copy `{baseDir}/scripts/copy-transforms.sh` assets, merge `examples/openclaw.hooks.fragment.json5`, expose the gateway hook URL, and register that URL in Topical via portal or `manage_agent_webhook`.

Restart the gateway or start a new session after config changes.

## Tools

| Tool | Purpose |
| --- | --- |
| `list_topics` | List monitored topics (`topicId`, `name`). Start here when topic is unknown. |
| `get_topic_update` | **Primary read** — breaking news, signals, and trends with source URLs since a checkpoint. |
| `get_topic_narrative` | Ready-made markdown summary with inline source links. |
| `submit_topic_feedback` | Steer future relevance: `not_relevant` or `interest` on breaking news, a signal, or a trend. |
| `list_topic_subscriptions` | RSS / YouTube feeds on the topic ingest plan. |
| `subscribe_topic_source` | Add RSS or YouTube for **future** runs only. |
| `unsubscribe_topic_source` | Remove a feed/channel subscription (`subscriptionId` from `list_topic_subscriptions`). |
| `manage_agent_webhook` | Register Topical → agent webhook URL for briefings and breaking-news alerts (`get` / `set` / `remove`). |
| `manage_topic_schedule` | Read or set the topic's recurring pipeline schedule (`weekly`, `fortnightly`, `monthly`). |

Responses may include `next_actions` suggesting the next tool to call. Tool **text** content also includes a JSON block with the same payload as `structuredContent` for MCP clients (including older OpenClaw) that only read the primary text field.

## Recommended workflows

### Scheduled briefing (after a pipeline run)

When the user wants "what's new since Topical last ran" (aligned with their schedule):

1. `list_topics` if you need `topicId`.
2. `get_topic_update` with `{ "topicId": "<topicId from list_topics>", "sinceLastRun": true }`.

`sinceLastRun` uses the **latest completed run** as the cutoff — the right default for recurring check-ins.

### Incremental check (between scheduled runs)

When you already briefed the user and want only new activity:

1. `get_topic_update` with `{ "topicId": "<topicId>", "lastCheckedAt": "<checkpoint>" }`.

Save the `checkpoint` from each `get_topic_update` response and pass it as `lastCheckedAt` next time. The response also includes `since` (the cutoff used) and `name` (topic label).

### Ready-made prose

For a polished markdown summary instead of structuring raw facts yourself:

1. `get_topic_narrative` with `{ "topicId": "<topicId>", "lastCheckedAt": "<checkpoint>" }`  
   or pass `since` for a time window (defaults to ~7 days), or `sinceRunId` to anchor on a specific run.

Use `get_topic_update` when you need structured breaking news, signals, trends, and URLs to write your own briefing.

### Steer monitoring

On breaking news, a signal, or a trend the user cares about (or wants to ignore):

- `submit_topic_feedback` with `kind: "interest"` or `"not_relevant"`, plus `targetType` (`breaking_news`, `signal`, or `trend`) and `targetId` (`breakingNewsId`, `signalId`, or `trendId` from `get_topic_update`).

Feedback affects **future** ingest and ranking, not the current snapshot.

### Add a source

1. `subscribe_topic_source` (`rss_feed` with `feedUrl` or `siteUrl`, or `youtube_channel` with `channel`).
2. Confirm with `list_topic_subscriptions`.

New sources are picked up on the **next scheduled run**, not immediately.

### Configure push delivery

After OpenClaw hooks are wired:

```json
{
  "action": "set",
  "url": "https://<gateway>/hooks/topical-inbound",
  "breakingNewsAlertsEnabled": true,
  "briefingEnabled": true,
  "bearerToken": "<hooks.token>"
}
```

Call via `manage_agent_webhook`. Save the returned signing secret to verify `X-Topical-Signature`.

### Manage schedule

To check or change when Topical runs the pipeline for a topic:

```json
{ "topicId": "<topicId>", "action": "get" }
```

```json
{
  "topicId": "<topicId>",
  "action": "set",
  "cadence": "weekly",
  "dayOfWeek": "Monday",
  "timezone": "Europe/London"
}
```

Use `action: "disable"` to turn the schedule off.

## Response shape (`get_topic_update`)

- **breakingNews** — global stories matched to the topic (`breakingNewsId`, title, summary, sources with `url` + optional `title`).
- **signals** — topic-specific signals (`signalId`, title, summary, sources).
- **trends** — emerging trends (`trendId`, title, summary, sources).
- **checkpoint** — pass as `lastCheckedAt` on the next call.
- **since** — ISO cutoff used for this response.

Cite source URLs when briefing the user. Empty arrays mean no new intelligence since the cutoff (often since the last run).

## Constraints

- **Read-only intelligence** — no MCP tool triggers ingest; do not tell the user you "searched the web" unless you used a separate search tool.
- **Stale relative to the open web** — freshness is bounded by the user's Topical schedule and last successful run.
- **Subscription scope** — tools operate on the authenticated Topical account's topics only.
- **Source subscriptions** — RSS/YouTube tools change the ingest plan; Brave search queries are configured in Topical and run every ingest.

## Example user prompts

| User says | You do |
| --- | --- |
| "What's new on our AI tools topic?" | `get_topic_update` with `sinceLastRun: true` |
| "Give me the weekly competitive intel briefing" | `get_topic_narrative` or `get_topic_update` + synthesize |
| "Anything since you last told me?" | `get_topic_update` with saved `lastCheckedAt` |
| "Stop showing me funding round noise" | `submit_topic_feedback` with `not_relevant` on the relevant breaking-news item, signal, or trend |
| "Track this company's blog" | `subscribe_topic_source` (RSS), note it applies after the next run |
| "Set up Topical webhooks in OpenClaw" | Run topical-openclaw-setup skill; use `manage_agent_webhook` when MCP works |
