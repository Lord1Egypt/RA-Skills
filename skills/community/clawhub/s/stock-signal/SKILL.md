---
name: stock-direction-signals
description: "Directional research brief on a US stock for agents on a MetaMask Agent Wallet — use when asked \"is NVDA bullish or bearish right now\", \"directional read on AAPL\", \"is MAG7 sentiment turning\", \"what do the chart, news, and social say about AMD\", \"signal brief on SPY\". Nine paid reads — quote, daily chart, RSI, MACD, news sentiment, earnings, Twitter/X chatter, Reddit threads, macro regime — fused into a bullish / bearish / mixed / insufficient-data brief with confidence, catalysts, and invalidation risks. Research only: never order execution, never financial advice. Pays in USDC from the user's own self-custodial MetaMask Agent Wallet; every signature stays in the wallet's mm CLI; no API keys. A run is nine purchases, so always dry-run first to see the live quoted total."
version: 1.0.0
metadata:
  openclaw:
    emoji: "📈"
    homepage: https://github.com/SELAT-AI/selat-metamask-skills/tree/main/skills/stock-direction-signals
    requires:
      bins:
        - python3
      anyBins:
        - mm
        - npm
    install:
      - kind: node
        package: "@metamask/agent-wallet"
        bins:
          - mm
---

# stock-direction-signals

Directional research on one US equity ticker or index proxy (MAG7,
semiconductor and AI-infrastructure names, tokenized-stock watchlists, SPY/QQQ)
for an agent on a **MetaMask Agent Wallet**. It runs a declarative manifest of
**nine paid reads** from a fixed provider filter — market quote, daily chart,
RSI, MACD, news sentiment, earnings history, Twitter/X chatter, Reddit
threads, and macro regime data — and the agent fuses them into one brief:
verdict (bullish / bearish / mixed / insufficient data), confidence, the
technical setup, catalysts, social sentiment, macro backdrop, and what would
invalidate the read. **Research only — it never places orders and its output
is never financial advice.**

It wraps the `stock-direction-signals` manifest from
[SELAT-AI/selat-metamask-skills](https://github.com/SELAT-AI/selat-metamask-skills),
and like [`selat-capabilities-for-metamask`](../selat-capabilities-for-metamask/SKILL.md)
it needs **no `selat` CLI and no SELAT plugin** — the engine is the MetaMask
Agent Wallet CLI (`mm`) plus the upstream repo's stdlib-only scripts. SELAT is
the catalog and payment router, used keylessly; custody stays with the wallet.

## Cost — read this first

- **A run is a pipeline, not a menu: nine paid purchases, not one.** Always
  dry-run first and show the user the live quoted total before executing.
- Every read is **real USDC** from the **user's own self-custodial MetaMask
  Agent Wallet** and its Circle Gateway balance. SELAT never holds keys or
  funds; every signature goes through the `mm` CLI.
- **Prices live in the live 402 quotes and the manifest's caps, not here** —
  the dry run prints the real quoted total; don't restate figures from memory.
- The manifest carries its own full-run spending cap, enforced by the runner;
  the Gateway deposit is the hard wallet-level cap above that.
- **Non-advisory, always.** The brief can support a bullish or bearish thesis
  but is research with sources, never advice, a prediction, or a signal to
  execute. If the user asks to trade on the result, decline that part — this
  skill buys data only.
- Never ask for, paste, or handle a private key.

## Step 0 — get the tooling (free, no funds)

No `selat` CLI needed. Install the MetaMask Agent Wallet CLI if `mm` isn't on
PATH, then fetch the upstream skills (text plus stdlib-only scripts):

```bash
mm --version || npm install -g @metamask/agent-wallet@latest
npx skills add SELAT-AI/selat-metamask-skills
```

Installing creates nothing money-related. The upstream repo is a prototype
from a live 2026-08 integration spike — proven on mainnet, not yet hardened;
review before large budgets.

## Step 1 — dry run first, before any wallet setup

**Do this before authenticating a wallet or asking the user to fund
anything.** The dry run quotes all nine steps for free — nothing is signed:

```bash
python3 skills/selat-purchasing/scripts/run_manifest.py \
  skills/stock-direction-signals/manifest.json \
  --param ticker=NVDA --dry-run
```

**Show the user the quoted per-step prices and the total, and get their OK
before wallet setup.** If they decline, stop — nothing has been spent.

## Step 2 — wallet setup (only after the user opts in)

```bash
mm doctor
python3 skills/selat-purchasing/scripts/eco_fund.py <usdc-amount>
```

Funding gotcha: **each `mm` sign-in method (Google, email, MetaMask Mobile QR)
loads a different wallet address** — fund the wallet of the sign-in method the
agent actually uses, and keep using that method. Wallet-escalated approvals
arrive on that method's channel (email link, or push for Mobile QR); an
approval that lands after a quote expires must be discarded and re-quoted.

## Step 3 — run

```bash
python3 skills/selat-purchasing/scripts/run_manifest.py \
  skills/stock-direction-signals/manifest.json \
  --param ticker=NVDA \
  --param company=NVIDIA \
  --param "twitter_query=\$NVDA OR NVIDIA OR Blackwell" \
  --param "reddit_query=NVDA NVIDIA Blackwell stock" \
  --yes
```

| Param | Steers | Feeds these reads |
|---|---|---|
| `ticker` | The equity or index proxy (required — never let a default research the wrong company). | quote, chart, RSI, MACD, news, earnings, macro |
| `company` | Company/product names for better recall (defaults to the ticker). | news sentiment |
| `twitter_query` | Cashtag + company/product terms (defaults to the cashtag). | Twitter/X chatter |
| `reddit_query` | Reddit search terms (defaults to "<ticker> stock"). | Reddit threads |

Every step returns raw JSON — the synthesis is your job: score social tone,
intensity, and engagement yourself (the reads return raw posts, not sentiment
scores), weight Reddit for recency and cross-community repetition, then write
the brief — verdict, confidence, technicals, catalysts, social sentiment,
macro regime, contrarian risks, and what would invalidate the call. Relay it
in plain language with what the run actually cost
(`python3 skills/selat-purchasing/scripts/spend_report.py`); keep raw JSON and
merchant URLs out of it. For multiple tickers, dry-run and run per ticker.

## Why this is safe to install

- **This wrapper is text-only** — installing it writes one markdown file. The
  manifest it runs is declarative JSON; the runner scripts are Python standard
  library only and never touch key material.
- **The wallet stays the authority**: every signature and transaction goes
  through the `mm` CLI, and payments are quote-pinned through the SELAT router
  (the EIP-712 domain is always the router's, never a merchant's).
- **Spend is triple-capped**: per-step and full-run caps in the manifest,
  enforced by the runner, under the Gateway deposit as the hard wallet cap. A
  refused or expired quote charges nothing.
- The manifest pins a **fixed provider filter** — the agent must not
  substitute other catalog merchants into this skill.

## Beyond this skill

For open-ended capability buying on the same wallet and tooling (web search,
scraping, enrichment, perp funding rates, prediction-market data), use
[`selat-capabilities-for-metamask`](../selat-capabilities-for-metamask/SKILL.md).
The other wrappers in this repo run vetted `selat-skills` recipes via the
`selat` CLI — a vetted `selat-skills` variant of this same skill exists there
too (SELAT-AI/selat-skills#64) for agents on a Circle Agent Wallet.

Docs: https://github.com/SELAT-AI/selat-metamask-skills
