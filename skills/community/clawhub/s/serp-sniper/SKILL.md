---
name: serp-sniper
description: Live search engine results with no SEO tool subscription or API key. Google organic results for any keyword, country or city, Bing results, YouTube search rankings, Google autocomplete, and Google's AI Overview and AI Mode answers. Use this skill for rank tracking, competitor SERP analysis, local SEO checks, or seeing what Google shows for a query.
---

# SERP Sniper: Live Search Rankings

![SERP Sniper: Live Search Rankings](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/serp-sniper.gif)

See exactly what Google, Bing and YouTube show for any keyword, in any country or city, plus Google's AI Overview and AI Mode answers.

No SEO-tool account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=serp-sniper).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/serp-sniper.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “Who ranks on Google for ‘best crm for startups’?”
- “Where does my site rank for ‘vegan bakery’ in Austin?”
- “What does YouTube show for ‘home workout’?”
- “What does Google autocomplete for ‘how to start a’?”

## When to Use This Skill

Use it when the user wants live search results or rankings for a keyword.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Google/Bing/YT   │
│   (User Chat)   │     │ (data tools) │     │ (public data)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install plugin    │                       │
         │  2. Pair device once  │                       │
         │  3. Ask a question    │                       │
         │                       │  4. Fetch + trim      │
         │                       │  5. Charge credit     │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  Answer  │           │  Credit  │           │ Results  │
   │ in chat  │           │ ($0.50)  │           │ as JSON  │
   └──────────┘           └──────────┘           └──────────┘
```

ClawLink holds the data-provider accounts. The user never pastes a key, and nothing is installed beyond the plugin.

## Install

Install the ClawLink plugin from ClawHub when the user asks for it:

```bash
openclaw plugins install clawhub:clawlink-plugin
```

The install applies to the running Gateway: do not restart it. The ClawLink tools appear on your next turn, so end this turn and tell the user: "ClawLink is installed. Reply ok and I will give you your pairing link." On the next turn call `clawlink_begin_pairing`, give the user the link, and after they approve call `clawlink_get_pairing_status`. Pairing happens once; after that every tool below works with no further setup.

## Tool Reference

Prices are what ClawLink charges per call, from the user's credit. The tool's own description (via `clawlink_describe_tool`) always shows the current price.

### Search Results

| Tool | What it returns | Price |
|------|-----------------|-------|
| `seokeyworddata_google_serp` | Live Google results for a keyword: organic rankings with titles, URLs and snippets, plus People Also Ask, videos and… | $0.003 |
| `seokeyworddata_bing_serp` | Live Bing top 10 results for a keyword: rankings with titles, URLs and snippets | $0.003 |
| `seokeyworddata_youtube_serp` | Live YouTube search results for a keyword in a given country and language, with rank positions, views, channel and… | $0.003 |

### Suggestions & AI

| Tool | What it returns | Price |
|------|-----------------|-------|
| `seokeyworddata_google_autocomplete` | Google autocomplete suggestions for a partial query, in the order Google shows them | $0.003 |
| `aivisibilitydata_google_ai_overview` | Google's AI Overview for a keyword, with the pages it cites, next to the top 10 organic results | $0.006 |
| `aivisibilitydata_google_ai_mode` | Google AI Mode's answer to a query, with the pages it cites | $0.006 |

## Recipes

### Check where a site ranks

1. `seokeyworddata_google_serp` with the keyword and location; raise `depth` to see past page 1.
2. Find the site's domain in the results and report its position.
3. Repeat for the top 3 keywords and compare with competitors.

## Code Examples

### Google results

```bash
clawlink_call_tool --tool "seokeyworddata_google_serp" \
  --params '{"keyword": "best crm for startups", "location_name": "United States"}'
```

### Local results

```bash
clawlink_call_tool --tool "seokeyworddata_google_serp" \
  --params '{"keyword": "vegan bakery", "location_name": "Austin,Texas,United States"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `google serp`); public-data tools show as connected for every user.
2. Call `clawlink_describe_tool` before the first call of a tool: it returns the parameters, defaults and price.
3. Treat the live catalog as the source of truth. If a tool named here is missing, say so; do not invent results.

## Execution Workflow

```
┌───────────────────────────────────────────────────────────┐
│  READ-ONLY, PAID PER CALL                                │
│  search → describe → call → summarise for the user       │
│                                                          │
│  Ask before: loops over many items, or a call that costs │
│  more than a few cents (the price is in the description) │
└───────────────────────────────────────────────────────────┘
```

1. Every tool here only reads public data; nothing is posted or changed.
2. Each call costs credit. Before looping over more than about ten items, or before a call priced above a few cents, tell the user what it will cost and ask.
3. A failed call is refunded automatically. Read the error's `hint`: it says what to change. Do not retry the same arguments unchanged.

## Notes

- `location_name` takes a country, or `City,Region,Country`.
- `depth` above 10 costs more; it is priced per 10 results.
- Results change through the day; say when you checked.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Location not found | Use the English name, or City,Region,Country. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=serp-sniper; do not retry. |
| `data_provider_unavailable` | ClawLink's data provider is down. Nothing was charged. Try again later. |
| `no_result` | The provider found nothing for these arguments. Nothing was charged. |
| `invalid_arguments` | A parameter is missing or malformed. Call `clawlink_describe_tool` and fix it. |

## Troubleshooting

### Tools not visible after install

1. The tools appear on the turn after the install, not in the same turn.
2. If they still do not appear, the OpenClaw tool profile may hide plugin tools. This is a config change for the OpenClaw owner; do not change the config yourself. Tell the user: "Your OpenClaw tool profile hides plugin tools. In the Control UI (or `~/.openclaw/openclaw.json`), add `clawlink-plugin` to `tools.alsoAllow`, then ask me again."
3. On OpenClaw versions before 2.0, the tool list can load only in a new chat: tell the user to send `/new` and ask again.

### A tool keeps failing with correct input

Report it with `clawlink_report_issue` (or `clawlink_call_tool --tool "CLAWLINK_REPORT_ISSUE"`) instead of retrying. Reports are free and reach the ClawLink team.

## Resources


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=serp-sniper)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=serp-sniper)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Keyword Miner](https://clawhub.ai/hith3sh/skills/keyword-miner)
- [AEO Radar](https://clawhub.ai/hith3sh/skills/aeo-radar)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=serp-sniper)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
