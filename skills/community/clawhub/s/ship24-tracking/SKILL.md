---
name: ship24-tracking
description: Track shipments and manage trackers using Ship24's universal tracking API — 2,500+ couriers and eCommerce platforms worldwide.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: [SHIP24_API_KEY]
    primaryEnv: SHIP24_API_KEY
    homepage: https://docs.ship24.com
    emoji: 📦
---

# Ship24 Tracking

Connect Claude to [Ship24](https://ship24.com) — the universal shipment tracking API covering **2,500+ couriers and eCommerce platforms** worldwide.

## Setup

1. Sign up and get your API key from the [Ship24 dashboard](https://dashboard.ship24.com)
2. Add the Ship24 MCP server to your `.mcp.json`:

```json
{
  "mcpServers": {
    "ship24-api": {
      "type": "http",
      "url": "https://api.ship24.com/mcp",
      "headers": {
        "Authorization": "Bearer ${SHIP24_API_KEY}"
      }
    }
  }
}
```

3. Set your API key as an environment variable:

```
SHIP24_API_KEY=your_api_key_here
```

## Available Tools

| Tool | Description |
|------|-------------|
| `track` | Create a persistent tracker and immediately return full tracking results (events, status, milestones). Idempotent — safe to call multiple times for the same tracking number. |
| `create_tracker` | Register a tracker to receive webhook notifications. Returns tracker metadata only — use `get_tracking_results` to fetch events and status. |
| `bulk_create_trackers` | Register up to 100 trackers in one request. Returns counts of created, duplicate, and failed entries. Not fully idempotent — retrying a failed request may partially create trackers. |
| `get_tracker` | Get tracker metadata by `trackerId` or `clientTrackerId`. Does **not** include events or delivery status — use `get_tracking_results` for that. |
| `update_tracker` | Partially update a tracker (PATCH). Common uses: toggle webhook subscription (`isSubscribed`), correct destination, set a `clientTrackerId` reference. |
| `list_trackers` | List all trackers in your account (paginated). |
| `get_tracking_results` | Get full tracking events and delivery status for a tracker. Returns `statusMilestone` values such as `in_transit`, `delivered`, `out_for_delivery`, `exception`, and more. |
| `search_tracking` | One-off per-call tracking lookup — no persistent tracker is created. Billed per query on per-call plans. |
| `search_tracking_by_number` | Search tracking results by raw tracking number across all couriers without needing a `trackerId`. |
| `get_couriers` | Get the full list of 2,500+ supported couriers with their codes and required fields. Rate-limited to 1 request/second. |
| `resend_webhooks` | Replay all webhook events for a tracker (use when your endpoint missed previous notifications). Rate-limited to 1 request/second per tracker. |

## Key Concepts

- **`trackerId` vs `clientTrackerId`**: `trackerId` is Ship24's internal ID. `clientTrackerId` is your own reference (order ID, internal key) — set it on creation or via `update_tracker`, then use `searchBy: "clientTrackerId"` in `get_tracker`, `update_tracker`, and `resend_webhooks`.
- **`track` vs `create_tracker`**: Use `track` when you want results immediately. Use `create_tracker` when you're setting up webhook-driven monitoring.
- **`search_tracking` vs `track`**: `search_tracking` is for per-call billing plans and leaves no persistent tracker. `track` creates a tracker in your account.

## Example Prompts

- *"Track my package 1Z999AA10123456784"*
- *"Create a tracker for JD014600006600006810 shipping to France"*
- *"Look up where RA123456785CN is without creating a tracker"*
- *"Bulk create trackers for these 5 tracking numbers: ..."*
- *"Show me all my active trackers"*
- *"Update tracker abc123 to subscribe to webhook notifications"*
- *"Get the full tracking history for tracker ID abc123"*
- *"What couriers do you support for shipments from China?"*
- *"Resend all webhook events for tracker abc123"*
