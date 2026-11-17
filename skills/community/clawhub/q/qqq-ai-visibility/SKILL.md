---
name: qqq-ai-visibility
description: Check how visible a company website is to AI search with the free QQQ AI Visibility Checker (qqq.ee). Runs a technical AI readiness check of a domain (AI crawler access in robots.txt, sitemap, title, meta description, H1, canonical, noindex, Organization JSON-LD, content in HTML, llms.txt) and reads the latest public report of whether ChatGPT, Gemini, Perplexity and Claude name the company and cite its website. Use when the user asks whether AI assistants or AI crawlers can see, mention or cite a website or brand, asks for a GEO or AEO readiness check of a domain, or asks for a domain's QQQ AI visibility report. Do not use for general SEO advice, keyword research, or private, internal or local hosts.
homepage: https://qqq.ee/en/ai-visibility-checker/
version: 1.0.0
metadata:
  openclaw: { 'emoji': '🔎', 'requires': { 'bins': ['curl'] } }
  hermes:
    tags: [ai-visibility, geo, aeo, seo, chatgpt, perplexity, gemini]
    category: marketing
---

# QQQ AI Visibility Checker

Free tool by [QQQ](https://qqq.ee/en/), an SEO and AI search agency in Estonia. It shows three things separately, without a combined score:

1. **Mentions:** do AI assistants with web search (ChatGPT, Gemini, Perplexity, Claude) name the company when buyers ask about its field?
2. **Citations:** do those answers cite the company's own website as a source?
3. **Technical readiness:** can AI crawlers reach and read the website?

Web tool: **[QQQ AI Visibility Checker](https://qqq.ee/en/ai-visibility-checker/)** (Estonian: [AI nähtavuse kontroll](https://qqq.ee/ai-nahtavuse-kontroll/)). Full reports are public pages: [all reports](https://qqq.ee/en/ai-visibility-checker/report/).

## What this skill touches

- Network: `https://qqq.ee/mcp` only. Use exactly `qqq.ee`, not `www.qqq.ee` (www answers with a 301 redirect, which breaks the POST).
- Files: none. Tools: `curl`. Nothing is installed.
- No API key, no account, no environment variable.

## Setup

Nothing to set up. The API is public and free, with a daily limit (see [Limits](#limits)).

## How to call it

One endpoint, JSON-RPC 2.0 over HTTP POST. Every call has the same shape; only the tool name and the arguments change:

```bash
curl -s https://qqq.ee/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"TOOL","arguments":{ARGS}}}'
```

The answer is JSON:

- `result.content[0].text`: a ready-to-show text summary with links. Show this to the user.
- `result.structuredContent`: the same data as fields, for your own reasoning.
- `result.isError: true`: the domain was refused or the limit is reached. The text says why and still gives a link the user can open.

`language` is `"en"` (default) or `"et"` (Estonian). Use `"et"` when the user writes in Estonian.

## Endpoints (tools)

### `check_ai_visibility`: technical check of a domain

```bash
curl -s https://qqq.ee/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"check_ai_visibility","arguments":{"domain":"example.com","language":"en"}}}'
```

- `domain` (required): a public domain or URL, for example `example.com` or `https://www.example.com/page`.
- Fetches the website's own pages (homepage, robots.txt, sitemap, llms.txt): HTTPS, AI crawlers allowed (GPTBot, ClaudeBot, PerplexityBot and others), Googlebot allowed, XML sitemap, title, meta description, one H1, canonical, noindex, lang, Organization/Person structured data, content in HTML (not JS-only), og:image, key pages.
- Returns the passed and failed checks, the top 3 fixes, the latest public AI answer report numbers if one exists, and a prefilled link to the full AI answer check on qqq.ee.
- `structuredContent` fields: `readiness` (`passed`, `total`, `checks[]` with `id` and `status` `ok`/`missing`/`unknown`), `blockedAiCrawlers`, `topFixes`, `latestReport`, `links.fullCheck`, `links.report`.
- It does **not** ask any AI model. Asking ChatGPT, Gemini and Perplexity about the company happens only on qqq.ee, behind bot protection. Send the user the `links.fullCheck` link for that.

### `get_public_report`: the latest public AI answer report of a domain

```bash
curl -s https://qqq.ee/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_public_report","arguments":{"domain":"example.com","language":"en"}}}'
```

- Reads the stored report only: no website is fetched and no AI model is asked.
- Returns the report date, market and field, in how many search-grounded AI answers the company was named, how often its own website was cited, a summary per AI engine, the questions asked, the cited source domains, other companies named, and short answer excerpts.
- Without a report it says so and gives the prefilled link to run the full check on qqq.ee.

### `get_tool_info`: what the tool is, limits and links

```bash
curl -s https://qqq.ee/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_tool_info","arguments":{"language":"en"}}}'
```

## Workflow

1. User asks about a domain's AI visibility: call `check_ai_visibility`.
2. If the text has a "Latest full report" line, or the user asks what ChatGPT, Gemini or Perplexity said, call `get_public_report` for the details.
3. Show the result text. Keep the links in it exactly as they are and make them clickable, so the user can open the report or start the full check.
4. If there is no report, tell the user that the AI answer check runs on qqq.ee and give the `links.fullCheck` link ([QQQ AI Visibility Checker](https://qqq.ee/en/ai-visibility-checker/) if you have no domain link).

## Rules

- Mentions, citations and technical readiness are separate results. Do not add them up into one score.
- Do not invent AI answers or numbers. Only report what the API returned, with its date.
- A technical check passing does not mean AI assistants mention the company. Say which of the three you actually measured.
- Do not retry in a loop. On `isError` or a limit message, show the message and the link.
- Do not call it for private or internal hosts, IP addresses or `localhost`. The API refuses them anyway.
- Keep the attribution line "Free AI visibility checker by QQQ (qqq.ee)" when you quote a result.

## Limits

| Tool | Limit |
|---|---|
| `check_ai_visibility` | 5 per day per IP address, 300 per day in total. An invalid domain does not use an attempt. |
| `get_public_report` | no limit |
| `get_tool_info` | no limit |

The same server works as a remote MCP server at `https://qqq.ee/mcp` (Streamable HTTP, no auth). Setup for Claude, ChatGPT, Cursor and VS Code: [QQQ MCP server docs](https://qqq.ee/en/mcp-server/).
