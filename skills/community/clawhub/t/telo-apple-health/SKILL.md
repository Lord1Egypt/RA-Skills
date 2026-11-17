---
name: telo-apple-health
description: Live Apple Health data in OpenClaw through the telo remote MCP server. No export file, nothing to install locally; the telo iPhone app syncs in the background. Sleep, HRV, resting heart rate, activity, workouts and long-term trends.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://telo.health
    emoji: "🫀"
---

# telo: Apple Health in OpenClaw

telo keeps your Apple Health history in sync from the telo iPhone app and serves it to assistants through a remote MCP server at `https://telo.health/mcp`, with OAuth sign-in. There is no export file to refresh and no local package to run: OpenClaw talks to the server, and the iPhone keeps it current in the background.

## Set up (once)

1. Install telo from the App Store, sign in, and send your history to telo. Wait for the first sync to finish.
2. Stop the OpenClaw Gateway. The `mcp add` and `mcp login` commands refuse to run while a Gateway owns the state directory.
3. Add the server and sign in:

   ```
   openclaw mcp add telo --url https://telo.health/mcp --transport streamable-http --auth oauth
   openclaw mcp login telo
   ```

   The login opens a telo page in your browser. Enter your email, type the 6-digit code you receive, and approve access.
4. Check the connection, then start the Gateway again:

   ```
   openclaw mcp doctor telo --probe
   ```

   If `openclaw mcp status --verbose` reports `authorization-required`, run `openclaw mcp login telo` again.

Equivalent config under `mcp.servers`:

```json
{
  "mcp": {
    "servers": {
      "telo": {
        "url": "https://telo.health/mcp",
        "transport": "streamable-http",
        "auth": "oauth"
      }
    }
  }
}
```

Do not put an `Authorization` header in the config; OAuth handles the token.

## Using the tools

Answer in the user's language. Always call `data_status` before interpreting freshness, and `list_metrics` to discover exact metric names and units; do not assume names from another provider.

- `query_daily`: daily metrics, aggregated by day, week or month.
- `sessions`: sleep nights and workouts, with workout UUIDs.
- `workout_detail`: zones, laps and splits; raw series are kept for 30 days, summaries permanently.
- `derived_metrics`: training load and personal HRV and resting heart rate baselines.

Rules that keep answers honest:

- Timestamps carry the local UTC offset. Never convert them to UTC.
- Sleep stages exclude time in bed. Do not add time in bed to the stages.
- A missing row or a null is unavailable, not zero. Never fill gaps.
- Responses cut at 500 rows and say so. On truncation, split the request into smaller non-overlapping ranges.
- Do not diagnose, and do not infer causation from these records.

## Guided workflows

- Weekly review (this week against the previous seven days, with coverage): follow `references/weekly-health-review.md`.
- Trends over months or years: follow `references/long-term-trends.md`.

## Privacy

Queries only read records; they never modify health data. telo stores the records the iPhone app uploads and logs which tool ran on which date range. To stop OpenClaw's access, run `openclaw mcp logout telo`. Deleting the account and all its data is in the Account tab of the telo app.

[Website](https://telo.health) · [Privacy](https://telo.health/privacy) · [Terms](https://telo.health/terms) · [Support](mailto:contact@telo.health)
