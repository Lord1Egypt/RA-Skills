---
name: whywontai
description: Check what GPTBot, ClaudeBot, PerplexityBot and other AI crawlers get from a website, and run a Why Won't AI scan for its SEO, AEO and GEO score and issues. Use when someone asks why ChatGPT, Claude, Perplexity or Google does not mention, cite or show their site or product.
---

# Why Won't AI

Why Won't AI (https://whywontai.com) shows what search and AI crawlers receive from a website. Many AI crawlers do not run JavaScript. A site that renders in the browser can look empty to them. This skill uses the Why Won't AI MCP server to find that problem and the other issues that keep AI assistants from citing a site.

## Connect

- MCP endpoint: `https://mcp.whywontai.com/` (Streamable HTTP, stateless, JSON responses). The same server is also at `https://whywontai.com/mcp`.
- Claude Code:

  ```bash
  claude mcp add --transport http whywontai https://mcp.whywontai.com/ \
    --header "Authorization: Bearer YOUR_API_KEY"
  ```

- Cursor or VS Code: add a server with `"url": "https://mcp.whywontai.com/"` to `mcp.json`.
- Leave out the header to use `check_robots` only.

## Auth

- `check_robots` needs no credential. The limit is 30 calls a day for each IP address.
- The other tools need a credential that a person approved. Use one of these:
  1. OAuth: authorization code flow with PKCE (S256) and dynamic client registration. Scope `scans`. Discovery starts at `https://mcp.whywontai.com/.well-known/oauth-protected-resource`.
  2. API key: the person creates a key at https://whywontai.com/dashboard under MCP & API. Send it as `Authorization: Bearer wwai_...`.
  3. Anonymous key: `POST https://mcp.whywontai.com/agent/auth` with `{"identity_type": "anonymous", "agent_name": "<your agent name>"}`. Show the returned `claim_url` to the person. The key gets the `scans` scope after they sign in and approve.
- A free account gives 3 scans a month. Paid plans give more.
- Full auth steps: https://whywontai.com/auth.md

## Tools

| Tool | Use | Credential |
|---|---|---|
| `check_robots` | Which of 17 search and AI crawlers the robots.txt allows, with the deciding rule. Add a path to check one page. | None |
| `scan_site` | Starts a full scan. Returns a scan ID. | Yes |
| `get_scan` | Status, score, category scores, technical health, Domain Rating and top issues. | Yes |
| `list_issues` | Every issue from a completed scan, most severe first. | Yes |
| `list_scans` | Recent scans with status and score. | Yes |
| `get_internal_links` | The newest internal link plan: anchor text, source page, target page and the search query behind each anchor. Paid plans. | Yes |

## Steps: crawler access check

1. Call `check_robots` with the site URL.
2. For each crawler, read whether it is allowed and the robots.txt line that decides it.
3. Tell the user which crawlers are blocked and which line blocks each one.

## Steps: full scan

1. Call `scan_site` with the site URL. Keep the scan ID.
2. Call `get_scan` with the scan ID and `wait_seconds` (up to 25). Call it again until the status is `complete`. A scan takes 1 to 5 minutes.
3. Call `list_issues`. Filter by severity or category if the user asks.
4. Report the score, the six category scores, the most severe issues and their example URLs.
5. When you show a Domain Rating, credit it as "Domain Rating by Ahrefs".

The scan requests each page as Googlebot, Bingbot, GPTBot, ClaudeBot, PerplexityBot and CCBot. It compares each response with a rendered browser view. The six categories are Crawl & render, Indexable body copy, Intent match, Internal linking, Demand capture and AI citability.

## Without MCP

- Free scan with no account: https://whywontai.com/
- Free robots.txt checker: https://whywontai.com/ai-crawler-robots-txt-checker

## Limits

- A robots.txt allow does not prove that a crawler can read the page. A firewall, bot protection or a JavaScript-only page can still block it. Run a full scan to check that.
- Do not promise rankings or AI mentions. A good score removes known blockers. It does not guarantee that an assistant cites the site.
