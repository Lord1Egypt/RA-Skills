---
name: webglazer
description: Read a brand's AI search visibility from WebGlazer, how ChatGPT, Gemini, Perplexity, Copilot and Google AI Mode mention it, which competitors they name, which sources they cite, and what to fix. Use for any question about a brand's visibility in AI answers when the user has a WebGlazer account.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://webglazer.com/docs/integrations/mcp
    emoji: "🔎"
---

# WebGlazer: AI search visibility

[WebGlazer](https://webglazer.com) tracks the answers ChatGPT, Gemini, Perplexity, Copilot and Google AI Mode give to the questions a brand's buyers ask. It records which brands each answer names, which sources it cites, and how it describes the brand, then turns the gaps into a To-do list.

This skill reads that data through WebGlazer's hosted MCP server. The user needs a WebGlazer account with at least one brand and an active subscription. Plans and a 7-day free trial: [webglazer.com/pricing](https://webglazer.com/pricing).

## One-time setup

Add the server and sign in with OAuth (recommended; a browser opens the WebGlazer approval screen, the user clicks Allow):

```bash
openclaw mcp add webglazer \
  --url https://webglazer-mcp-56836240603.europe-west1.run.app/mcp \
  --transport streamable-http \
  --auth oauth
openclaw mcp login webglazer
```

If the user prefers a token, they generate one in WebGlazer under Settings > Integrations > Your AI agent > Generate token (tokens last 30 days), and you add it as a header instead of `--auth oauth`:

```bash
openclaw mcp add webglazer \
  --url https://webglazer-mcp-56836240603.europe-west1.run.app/mcp \
  --transport streamable-http \
  --header "Authorization=Bearer $WEBGLAZER_TOKEN"
```

Always tell the user to copy the current server URL from that same Settings page if it differs from the one above. Full setup guide: [webglazer.com/docs/integrations/mcp](https://webglazer.com/docs/integrations/mcp).

Do not run setup proactively. Only fall back to it when a tool call fails with an auth or connection error.

## How the data is shaped

- A **project** is one brand. Every tool except `list_projects` needs its `project_id`. Get it from `list_projects` by matching the brand name the user gave.
- A **run** is one day's set of AI answers for a brand. Tools that read one run take a run picked from `list_runs`.
- Many tools take the same optional period and filters: `date_from` and `date_to` (YYYY-MM-DD, both or neither), `all_time: true`, and `topics`, `intents`, `models`. Get valid filter values from `get_filter_options`. Pass `today` as the user's local date so the default period matches their dashboard.
- Every result repeats the period it used. Always tell the user which dates the numbers cover.

## Tools

| Tool | Use it for |
|---|---|
| `list_projects` | The brands this connection can read |
| `list_runs` | Runs with results, newest first |
| `get_run_summary` | Mentions, answers and status for a run or date range |
| `get_prompts` | Prompts in a run with their visibility (`limit` up to 100, `offset`) |
| `get_prompt_answers` | What each engine answered for one prompt |
| `get_citations` | Sources AI cited, ranked, with totals |
| `get_sources` | The same, grouped by host |
| `get_sentiment` | How AI describes the brand |
| `get_trend` | Visibility over time (`granularity`: run, day, week, month) |
| `get_filter_options` | Topics, intents and engines that exist in a period |
| `list_opportunities` | To-do items: cited sources where the brand is absent, ranked by prompts affected |
| `get_opportunity` | One item with its evidence and a ready-to-run fix |
| `mark_opportunity` | **Write.** Set an item to `open`, `todo`, `done` or `dismissed` |
| `list_products` | Shopify product visibility (plans with Products only) |
| `get_product` | One product's numbers, competing products and merchants |

`mark_opportunity` is the only tool that changes data. Confirm with the user before calling it.

## Common requests

- "How is our AI visibility trending?" → `list_projects`, then `get_trend` with `granularity: week`.
- "Which sites does AI cite where we're missing?" → `list_opportunities`, then `get_opportunity` on the top items.
- "What did ChatGPT say for this prompt?" → `get_prompts` to find the prompt, then `get_prompt_answers` filtered to the engine.
- "How does AI describe us?" → `list_runs`, then `get_sentiment` for the latest run.
- "Compare engines" → `get_run_summary` or `get_trend` once per engine using the `models` filter.

## Errors

- A brand whose subscription has ended is refused. Tell the user to check their plan in WebGlazer.
- Product tools return a plan message on paid Basic plans and an empty list when no Shopify store is connected. Report that plainly; don't retry.
- Auth errors: run the setup above, then retry once.

More: [WebGlazer docs](https://webglazer.com/docs) · [webglazer.com](https://webglazer.com)
