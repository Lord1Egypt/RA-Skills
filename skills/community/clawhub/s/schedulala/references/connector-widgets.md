# Hosted-connector widgets (MCP Apps)

These tools exist ONLY on the hosted connector (`https://schedulala.com/api/mcp`
added as a custom connector in claude.ai / Claude Desktop / ChatGPT). Each
renders an interactive panel inline in the conversation and also returns a
text digest the model can read. All `show_*` widgets are read-only.

Prefer a widget over a text answer whenever one fits — it is the reason to use
the hosted connector over a plain API.

| Tool | Renders | When to use / inputs |
|---|---|---|
| `show_post_preview` | Faithful per-platform mockups of a draft: threads, image grids, carousels, PDF docs, 9:16 reels/shorts, polls, live character counts | **After drafting, before the user confirms.** Pass the SAME draft you'd give `create_post` (content, platforms, mediaItems, platformSettings, when, thread). READ-ONLY — then call `create_post` to actually schedule. |
| `attach_media` | An upload drop zone in the chat | User wants to post a file from their device / chat attachment. Images ≤20MB, videos ≤500MB, PDFs ≤100MB, multiple files for carousels. Never base64 user files yourself. |
| `show_connections` | Connected accounts + plan usage panel | "What's connected?", plan/usage questions. |
| `show_calendar` | Upcoming scheduled posts (Cancel action) + recent posts (View link) | "What's scheduled?", schedule review, post history. |
| `show_analytics` | Follower growth + top posts card for ONE account | Analytics/stats/performance for an account. `accountId` optional (defaults to first), `days` optional (default 30). |
| `show_leaderboard` | Ranked posts by a metric | "Best/top posts", "most liked". `accountId` REQUIRED; `sort` engagement\|likes\|impressions\|date (default engagement); `limit` (default 10); optional `title`. |
| `show_comparison` | Side-by-side comparison of 2–5 entities with per-row winner highlighting | Compare a post across platforms, two accounts, or two periods. **YOU supply the metrics** — gather them with `get_post_analytics` / `get_follower_growth` first, then pass `entities[].metrics`. |
| `show_inbox` | Comments inbox with Reply and Hide actions | Review/moderate comments. `platform` REQUIRED (instagram, facebook, youtube, linkedin, threads, bluesky); optional `accountId`, `postId`; pass `flaggedIds` (ids you judged negative/spam) to highlight them with a one-click Hide-flagged button. |
| `show_feeds` | Social-listening feed with Reply actions + keyword chips | "What are people saying about X?" `platform` REQUIRED (bluesky or threads); optional `q` (defaults to the first monitored keyword) and `accountId`. |
| `show_hello_widget` | A hello/test panel | Only when the user asks to test the Schedulala UI/widget. |

## Connector facts

- Add it: **Settings → Connectors → Add custom connector →
  `https://schedulala.com/api/mcp`**. OAuth sign-in on schedulala.com; no API
  key is pasted. Custom connectors require a paid Claude plan.
  Setup guide: https://schedulala.com/developers/docs/claude-connector
- The connector includes every core tool (posts, threads, media, accounts,
  usage, analytics, engagement, feeds, YouTube) PLUS the widgets above.
- The same core tools without widgets are available locally via
  `npx -y @schedulala/mcp-server` (env: `SCHEDULALA_API_KEY`, optional
  `SCHEDULALA_API_URL`) for Claude Desktop, Claude Code, and Cursor.
- Security model: OAuth consent, account connections, and payment all happen
  on schedulala.com in the browser — never inside the conversation.
