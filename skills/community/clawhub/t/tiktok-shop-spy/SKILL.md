---
name: tiktok-shop-spy
description: TikTok Shop product research without a seller account or API key. Search TikTok Shop products with prices, units sold and ratings, open a product page, read buyer reviews, browse a store's best-sellers, see which products a creator promotes, and what a live stream is selling. Use this skill for finding winning products, competitor store research, or affiliate creator research.
---

# TikTok Shop Spy: Product Research

![TikTok Shop Spy: Product Research](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/tiktok-shop-spy.gif)

Find what sells on TikTok Shop: products with prices, units sold and ratings, buyer reviews, a store's best-sellers, and which products creators push.

No TikTok seller account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-shop-spy).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/tiktok-shop-spy.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “What lip gloss is selling on TikTok Shop?”
- “Read the reviews of this TikTok Shop product”
- “What are this store's best-sellers?”
- “Which products does this creator promote?”

## When to Use This Skill

Use it when the user wants TikTok Shop products, stores, reviews or creator showcases.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ TikTok Shop      │
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

### Products

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_shop_search` | TikTok Shop products matching a keyword, with prices and sales | $0.00282 |
| `tiktokdata_shop_product` | One TikTok Shop product by URL: price, sales, rating, seller and variants | $0.00282 |
| `tiktokdata_shop_product_reviews` | Buyer reviews of a TikTok Shop product | $0.00282 |
| `tiktokdata_shop_search_suggestions` | TikTok Shop's autocomplete suggestions for a product search | $0.0015 |

### Stores & Creators

| Tool | What it returns | Price |
|------|-----------------|-------|
| `tiktokdata_shop_products` | Products of one TikTok Shop store, best-selling or newest first | $0.00282 |
| `tiktokdata_creator_showcase` | Products a TikTok creator promotes in their profile showcase | $0.00282 |
| `tiktokdata_live_products` | Products a TikTok live stream is selling | $0.0015 |

## Recipes

### Find a winning product

1. `tiktokdata_shop_search` for the niche; rank by units sold.
2. `tiktokdata_shop_product_reviews` on the leaders for complaints to fix.
3. `tiktokdata_creator_showcase` on creators selling it, to find affiliates.

## Code Examples

### Search products

```bash
clawlink_call_tool --tool "tiktokdata_shop_search" \
  --params '{"query": "lip gloss"}'
```

### Reviews

```bash
clawlink_call_tool --tool "tiktokdata_shop_product_reviews" \
  --params '{"product_id": "1729512085846726019"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `tiktok shop`); public-data tools show as connected for every user.
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

- US results are the most reliable; other regions may be incomplete.
- Units sold is lifetime as shown on TikTok.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Product not found | Use the product URL or id from a search result. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-shop-spy; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-shop-spy)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-shop-spy)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [TikTok Trend Radar](https://clawhub.ai/hith3sh/skills/tiktok-trend-radar)
- [Amazon Scout](https://clawhub.ai/hith3sh/skills/amazon-scout)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tiktok-shop-spy)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
