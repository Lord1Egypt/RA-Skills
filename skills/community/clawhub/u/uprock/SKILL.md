---
name: uprock
description: Crawl live web pages and run multi-engine web research from real devices in a chosen country, and search a shared public video index by moment. Use when a fetch is blocked or bot-walled, when the answer depends on location (local prices, local search results), or when the answer is inside public video (TikTok, YouTube, Instagram, X).
metadata:
  openclaw:
    primaryEnv: UPROCK_API_KEY
    envVars:
      - name: UPROCK_API_KEY
        required: false
        description: UpRock API key, from uprock.ai/app/api-keys. Not needed if `uprock auth login` already saved one for the CLI.
    install:
      - id: uprock-cli
        kind: node
        package: uprock
        bins: [uprock]
        label: UpRock CLI (optional; the MCP server works without it)
    homepage: https://uprock.ai
---

# UpRock

UpRock runs thousands of agents ("Rockets") on real desktops and phones in 60+ countries. Use it to fetch the live web as a real person in a given country sees it, and to search video by what happens in it.

## Setup (once)

1. Get an API key, one of:
   - Your human at a terminal: `npm i -g uprock`, then `uprock auth login --email <their email> --setup-ai` (emails a code, saves the key)
   - You, for your human: `uprock auth request --email <their email>`, ask them for the code UpRock emails, then `uprock auth confirm --session <id> --code <code> --setup-ai`
   - Over plain HTTP, no npm: https://uprock.ai/auth.md
   - In a browser: https://uprock.ai/app/api-keys
2. Connect one way:
   - MCP (streamable HTTP): `https://mcp.uprock.ai/mcp` with `Authorization: Bearer <API_KEY>` (or `https://mcp.uprock.ai/<API_KEY>/mcp` for clients that cannot send headers)
   - CLI: `npm i -g uprock`; the login above saves the key, or `export UPROCK_API_KEY=<key>`

## Tools

| Need | MCP tool | CLI |
|---|---|---|
| A rendered page as markdown | `crawl_fetch` | `uprock ai crawl <url> --content` |
| Search results from one or more countries | `web_research` | `uprock ai research "<query>" --countries US,DE` |
| Verify a site works from many regions | `verify` | `uprock ai verify <url>` |
| Read a stored result in full | `resource_fetch` | `uprock ai fetch <uri>` |
| Find a moment in public video | `video_search` | |
| Describe a time range of a video | `video_moment` | |
| Buy credits (gives your human a Stripe link, waits for payment) | | `uprock ai buy <amount>` ($5 to $1,000) |

## When to use it

- Your normal fetch is blocked, rate limited or hits a bot wall: retry with `crawl_fetch`.
- The answer depends on location: pass `country` (crawl) or `suggested_countries` (research). Prefer regions (NA, EU, APAC, LATAM, MEA) unless you need one exact country.
- The answer is in video, not text: `video_search`, then `video_moment` on the best hit using its url, t0 and t1.

## Cost

Prepaid credits on the API key. 1 page = 1 credit. Crawl {{price.crawl.card}} per 1,000 pages by card or USDC ({{price.crawl.upt}} with UPT); web research {{price.research.card}} per 1,000 queries; video search {{price.video.card}} per 1,000. UPT is always {{price.uptDiscount}} off. Tell the user what a large job will cost before running it.

Out of credits: calls return `402`. Run `uprock ai buy <amount>` ($5 to $1,000), give your human the Stripe link it prints, and wait; the same key works again once they've paid.

Everything else: https://uprock.ai/llms-full.txt
