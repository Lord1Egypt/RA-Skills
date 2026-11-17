---
name: ticker-watch
description: Stock prices and market data with no brokerage account or API key. Latest end-of-day prices for any ticker, price history, intraday prices, ticker search across 70+ exchanges, dividends and splits. Use this skill for portfolio check-ins, stock research, earnings-week tracking, or quick market updates.
---

# Ticker Watch: Stock Prices

![Ticker Watch: Stock Prices](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/ticker-watch.gif)

Check any stock in plain English: the latest close, how it moved over weeks or years, intraday prices, dividends and splits, on 70+ exchanges.

No brokerage account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=ticker-watch).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/ticker-watch.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “How did AAPL, NVDA, MSFT and TSLA close yesterday?”
- “Show Apple's price over the last year”
- “What dividends has Coca-Cola paid this year?”
- “Find the ticker for BMW in Germany”

## When to Use This Skill

Use it when the user wants stock prices, history, dividends or splits.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Stock exchanges  │
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

### Prices

| Tool | What it returns | Price |
|------|-----------------|-------|
| `stockmarketdata_price` | The most recent end-of-day bar (open, high, low, close, volume) for one or more stocks: yesterday's close during… | $0.001499 |
| `stockmarketdata_price_history` | Daily open, high, low, close and volume for one or more stocks over a date range, with split- and dividend-adjusted… | $0.001499 |
| `stockmarketdata_intraday_prices` | Intraday bars for a US stock from the IEX exchange (delayed, not real time): open, high, low, close, volume per interval | $0.001499 |

### Corporate Actions

| Tool | What it returns | Price |
|------|-----------------|-------|
| `stockmarketdata_dividends` | Dividend payments of a stock: date and amount per share | $0.001499 |
| `stockmarketdata_splits` | Stock splits of a stock: date and split factor | $0.001499 |

### Lookup

| Tool | What it returns | Price |
|------|-----------------|-------|
| `stockmarketdata_search_tickers` | Find a stock's ticker by company name or symbol, with the exchange it trades on | $0.001499 |
| `stockmarketdata_exchanges` | Stock exchanges covered, with MIC code, country, city, timezone and currency | $0.001499 |

## Recipes

### Portfolio check-in

1. `stockmarketdata_price` with all the tickers, comma-separated.
2. Compare open and close; flag the biggest movers.
3. `stockmarketdata_price_history` for anything that moved a lot.

## Code Examples

### Latest prices

```bash
clawlink_call_tool --tool "stockmarketdata_price" \
  --params '{"symbols": "AAPL,NVDA,MSFT"}'
```

### One year of history

```bash
clawlink_call_tool --tool "stockmarketdata_price_history" \
  --params '{"symbols": "AAPL", "date_from": "2025-10-01"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `stock price`); public-data tools show as connected for every user.
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

- Non-US tickers carry the exchange, e.g. `BMW.XETRA`: find them with `stockmarketdata_search_tickers`.
- Prices are end of day unless you use the intraday tool.
- Not investment advice.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| At least one valid symbol must be provided | The ticker is wrong or needs its exchange suffix. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=ticker-watch; do not retry. |
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

- [Marketstack](https://marketstack.com)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=ticker-watch)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=ticker-watch)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Crypto Pulse](https://clawhub.ai/hith3sh/skills/crypto-pulse)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=ticker-watch)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
