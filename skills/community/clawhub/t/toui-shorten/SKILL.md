---
name: toui-shorten
description: Shorten URLs with toui.io and read their click stats. Use when the user wants to shorten a long URL, create a short link, make a tracking link, or check how many clicks a toui.io short code has received.
version: 1.0.1
metadata:
  openclaw:
    primaryEnv: TOUI_API_KEY
    envVars:
      - name: TOUI_API_KEY
        required: false
        description: toui API key (shorten scope) needed only for the direct REST path (curl). Create one at https://toui.io/admin. Not required if you connected via "openclaw mcp add toui" (OAuth).
    requires:
      anyBins:
        - curl
    emoji: "🔗"
    homepage: https://toui.io
    os:
      - darwin
      - linux
---

# toui — URL shortener (toui.io)

Shorten long URLs with [toui.io](https://toui.io) and read click stats. toui also runs a Telegram bot.

## Two ways to use it

### A. Via the toui MCP server (recommended, no API key)

If you're connected to toui's MCP server, just call the tool `shorten_url`:

```
shorten_url({ "url": "<url to shorten>", "title": "optional title" })
```

It returns `{ short_url, code, qr_url }` — hand `short_url` back to the user.

One-time setup:

```
openclaw mcp add toui --url https://mcp.toui.io --transport streamable-http --auth oauth
openclaw mcp login toui
```

> Note: the authorization code contains a colon. When copying `code` from the browser address bar, replace `%3A` back with `:` before running `openclaw mcp login toui --code <code>`.

### B. Via the REST API (needs TOUI_API_KEY)

When not going through MCP, call the REST endpoint directly:

```
curl -X POST https://toui.io/api/v1/shorten \
  -H "Authorization: Bearer $TOUI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"<url to shorten>","title":"optional"}'
```

Returns JSON with `short_url` and `short_code`. Create a `shorten`-scope key at <https://toui.io/admin> and set it as the `TOUI_API_KEY` environment variable.

## Notes

- Short links created under a logged-in account are permanent.
- Click stats: the MCP tool only creates links (no stats); over REST use `GET https://toui.io/api/v1/urls/{code}/stats` (needs a `full`-scope key).
- Custom short codes, branded domains, and advanced analytics are paid-plan features.
