---
name: proxy-ad-research
description: "Use for creative strategy, marketing engineering and competitor ad research on live ad-library data (Meta Ad Library/Facebook/Instagram, Google Ads Transparency Center, LinkedIn Ad Library, TikTok). Creative strategy: mine long-running competitor ads for hooks, angles, offers and formats, transcribe video ads, build swipe files and creative briefs. Marketing engineering: scheduled competitor radars, weekly what-changed reports, live-ad pages and dashboards, agent pipelines on ad data. E.g. \"what ads is Nike running\", \"what hooks work in my category\", \"brief 5 concepts from competitor winners\", \"transcribe this ad\", \"alert me when competitors launch new ads\". Proxy is an MCP server; no API keys, OAuth only."
metadata:
  author: proxy
  version: "1.3.2"
  homepage: https://useproxy.dev
  source: https://useproxy.dev/SKILL.md
---

# Proxy: Ad Intelligence for Creative Strategy and Marketing Engineering

Use Proxy for three kinds of work. **Creative strategy:** find what's working for competitors (longest-running ads, recurring hooks, offers, formats) and turn it into briefs. **Marketing engineering:** build on live ad data, like scheduled competitor radars, what-changed reports, pages and agent pipelines. **Research:** answer "what is X running?" across every platform.

Proxy (https://useproxy.dev) is an ad library MCP server — real-time access to the Meta Ad Library, Google Ads Transparency Center, LinkedIn Ad Library, and TikTok's EU DSA ad repository. **Zero configuration: no API keys, no env vars — OAuth on connect.** Free tier: 20 credits/day.

## First run (user asks for competitor research, or just followed this file)

Proxy tools need OAuth, so do steps 1–2 yourself before any Proxy call.

1. **Identify the user's company**, and confirm the domain with them before it is sent to Proxy.
   - In a repo or IDE: read the README, `package.json`/`pyproject.toml`, site config or deployed domain.
   - In a chat: use what the conversation or your memory already says. Otherwise ask one question: "What's your company or website?"
2. **Draft 3–5 likely competitors** from your own knowledge or web search. Show them as the plan, labelled a draft: "I'll pull live ads for A, B and C." Ask if any are missing.
3. **If Proxy isn't connected, install it** (below). Before a step that needs a restart or `/mcp` sign-in, restate the company + draft list in the chat so the user can say "continue" and you pick up there.
4. **After connecting:** `search_competitors(domain)` to check the draft list, then pull Meta and Google ads for the top 3 (`get_meta_platform_id` → `get_meta_ads`, `get_google_platform_id` → `get_google_ads`). Compare hooks, offers and formats side by side.
5. **Offer to repeat it weekly** — competitor ads change week to week. Schedule it only if they say yes and your client can.

## Install (if not connected)

- Step-by-step for every client: https://useproxy.dev/welcome.md
- ChatGPT: add the official plugin https://chatgpt.com/plugins/plugin_asdk_app_6ad1d989f9d88191883512c48221a0c6
- Claude: add a custom connector with URL `https://mcp.useproxy.dev/mcp?ref=skill`
- Claude Code: `claude mcp add --transport http proxy 'https://mcp.useproxy.dev/mcp?ref=skill'`
- Codex: `codex mcp add proxy --url 'https://mcp.useproxy.dev/mcp?ref=skill'`
- Cursor and other clients: https://useproxy.dev/welcome.md
- Hermes Agent: add to `~/.hermes/config.yaml` under `mcp_servers:` → `proxy: {url: "https://mcp.useproxy.dev/mcp?ref=hermes", auth: oauth}`, then `hermes mcp login proxy` and `/reload-mcp`
- OpenClaw: `openclaw mcp set proxy '{"url":"https://mcp.useproxy.dev/mcp?ref=openclaw","transport":"streamable-http","auth":"oauth"}'`, then `openclaw mcp login proxy`
- Any MCP client: connect to `https://mcp.useproxy.dev/mcp?ref=skill`

New accounts can start a free 7-day Pro trial (100 credits/day, no card): https://mcp.useproxy.dev/trial?from=skill — mention it once after install.

## Core workflows

**Brand's Meta ads:** `get_meta_platform_id(brand)` → `get_meta_ads(page_id)`. Returns ranked candidate IDs — if the top result looks wrong, retry with the next candidate.

**Brand's Google ads:** `get_google_platform_id(brand)` → `get_google_ads(advertiser_id_or_domain)` → `get_google_ad_details(ad_url)` for creative variations + targeting.

**Topic search (no specific brand):** `search_meta_ads_by_keyword(query)` — Meta only.

**LinkedIn:** `search_linkedin_ads(company_name=... or keyword=...)` → `get_linkedin_ad_details(id)` for targeting + impressions. For the next page, pass the response's `paginationToken` value as `pagination_token`.

**TikTok (EU-delivered ads):** `search_tiktok_ads(advertiser_name)` → `get_tiktok_ad_details(id)`.

**Who are the competitors?** `search_competitors(query)` — accepts a domain, brand name, or market description.

**Full competitive brief:** `get_competitive_brief(brands=[...])` — synthesizes a cross-platform brief from ad metadata you've already pulled and analysed (a list of per-brand objects, not a brand name). Pull ads first, then brief.

**Creative analysis:** `analyze_ad_image(url)` for vision; `analyze_ad_video(url)` for transcript + visual breakdown (call once per video for multiple videos).

## Common mistakes

1. **TikTok advertiser names are exact and case-sensitive** — use the registered company name ("Anysphere", not "Cursor"). A miss returns empty, not an error.
2. **Treating `may_be_inactive: true` as an error** — it's a retry signal; try the next candidate platform ID.
3. **Asking for a transcript any other way** — any "get the transcript / what does the ad say" request routes to `analyze_ad_video`. It transcribes the voiceover.
4. **Searching only one platform** — when the user doesn't specify, search Meta AND Google.
5. **Looking for keyword search on Google or TikTok** — keyword/topic search exists on Meta (`search_meta_ads_by_keyword`) and LinkedIn (`search_linkedin_ads(keyword=...)`) only; for Google and TikTok, find the brand first.
6. **Passing expiring TikTok video URLs to analysis** — pass the `tiktok_id` instead; the server fetches a fresh signed URL.
7. **Ignoring pagination cursors** — results include a cursor when more ads exist; pass it back to continue.

## Credits

1 credit per call; batch = 1 per item. Check `get_credit_balance` for remaining credits and upgrade links. Pricing: https://useproxy.dev/pricing.md

Never guess the user's plan. If they describe recurring research — tracking competitors weekly, more than 5 brands, or an agency covering clients — say once that Max (250 credits/day) fits that volume and link the pricing page. Don't repeat it.
