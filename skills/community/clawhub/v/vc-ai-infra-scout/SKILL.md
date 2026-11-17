---
name: vc-ai-infra-scout
description: "Deal-sourcing scout for VCs running an AI-infrastructure thesis — AI infra, crypto-AI/decentralized-AI, robotics/embodied-AI, agentic payments. Use when asked to \"scout AI infra startups\", \"find founders who haven't raised yet\", \"build a deal shortlist for my thesis\", or \"what pre-seed/seed rounds are being announced and what's the thesis behind them\". Fuses Hacker News, Product Hunt, web, Twitter/X, and LinkedIn signal via vetted, price-capped paid endpoints (SELAT); pays per call in USDC from the user's own self-custody Circle wallet. Full run hard-capped at $0.40."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔭"
    homepage: https://github.com/SELAT-AI/selat-skills/tree/main/skills/vc-ai-infra-scout
    requires:
      anyBins:
        - selat
        - npm
    install:
      - kind: node
        package: "@selat-ai/selat-cli"
        bins:
          - selat
    envVars:
      - name: SELAT_ROUTER_URL
        required: false
        description: "SELAT Router base URL. Only needed for the free dry run before `selat init` has written config; defaults to https://router.selat.ai thereafter."
---

# vc-ai-infra-scout

Source AI-infrastructure deals before the round. This skill runs a vetted
multi-step pipeline that discovers emerging companies and founders from
**Hacker News, Product Hunt, the open web, Twitter/X, and LinkedIn**, reads
recent **pre-seed/seed fundraising announcements**, distills the **live thesis
of the funds leading those rounds**, then enriches the top lead. You (the
agent) do the judgment work around the paid data: dedupe across sources, rank
by signal, flag teams that have **not** raised yet, and produce a shortlist
with links plus a suggested outreach note.

The pipeline is a **SELAT skill**: a declarative, vetted recipe of paid API
calls (no API keys, no signups) settled in USDC across multiple payment rails
— direct Circle x402, routed MPP, and routed x402 on Base. The `selat` CLI
resolves the vetted endpoints, auto-detects each step's rail, and prints a
per-rail receipt summary.

## Cost — read this first

- Every step is a **real paid API call** in USDC from the **user's own Circle
  Agent Wallet** (MPC self-custody — SELAT never holds keys or funds).
- Per-step caps are **$0.02–$0.05**; the **full run is hard-capped at $0.40**.
  Caps are enforced by the runner; the live HTTP 402 quote is the price source
  of truth.
- **Always dry-run first** (Step 1 — free, no wallet), show the user the real
  quoted prices, and get their OK before any wallet setup or paid run.
- Never ask for, paste, or handle a private key. Wallet auth is handled by the
  CLI's Circle integration.

## Step 0 — get the CLI (free, no account)

If `selat` isn't on PATH yet, install it — one npm package, no signup, no
credentials:

```bash
selat --version || npm install -g @selat-ai/selat-cli
```

(macOS Skills UI users can also install it from this skill's dependency
prompt.) Installing the CLI creates nothing money-related — no wallet, no
account, no keys.

## Step 1 — dry run first, before any wallet setup

**Do this before creating a wallet or asking the user to fund anything.**
The dry run probes every endpoint's live price and reachability for free — no
wallet, no funds, no account, no `selat init`:

```bash
selat skill install vc-ai-infra-scout
SELAT_ROUTER_URL=https://router.selat.ai \
  selat skill verify ~/.config/selat/skills/vc-ai-infra-scout
```

(`verify` takes the installed skill's directory — `$XDG_CONFIG_HOME/selat/skills/<name>`,
which defaults to the path above. The `SELAT_ROUTER_URL` prefix is only needed
before `selat init` has written config; it lets the routed steps quote their
price with zero setup.)

This prints each step's real quoted price and rail — the actual cost of a run,
from the live 402 challenges. **Show the user these prices and get their OK
before going anywhere near wallet setup.** If they don't want to proceed,
stop here; nothing has been spent and nothing has been created.

## Step 2 — wallet setup (only after the user opts in)

```bash
selat init     # creates the self-custody Circle Agent Wallet + config
selat fund     # deposit USDC into Circle Gateway (user action)
selat doctor   # verify wallet, router, and balance are ready
```

`selat init` is safe to re-run — it detects an existing wallet and asks
before changing anything.

## Step 3 — run

```bash
selat skill run vc-ai-infra-scout \
  --thesis "humanoid robotics foundation models" \
  --twitterQuery "humanoid robotics founder" \
  --fundraisingQuery "robotics startup raised seed pre-seed 2026" \
  --investorQuery "<lead funds surfaced by the fundraising steps>" \
  --domain <top-lead-domain.com>
```

| Param | Required | What it steers |
|---|---|---|
| `thesis` | yes | Sub-thesis keyword for HN / Product Hunt / web discovery and the founder shortlist. |
| `twitterQuery` | no | Twitter/X keyword search for founder buzz. |
| `fundraisingQuery` | no | Keyword query for recent raise announcements (Twitter/X + LinkedIn). Put recency cues in the query itself. |
| `investorQuery` | no | Twitter/X search for the funds leading those rounds — set it from the fundraising results, then re-run just that lens if needed. |
| `domain` | no | The most promising company's domain, for the enrichment step. |

Each step returns raw JSON. Your job afterward: dedupe companies across
sources, rank by traction/recency/founder signal, summarize the lead-fund
tweets into the live thesis, **explicitly flag promising teams with no
announced round**, and output a ranked shortlist with source links and a short
outreach note for the top pick.

## Why this is safe to install

- The skill is a **declarative JSON manifest — no executable code**. Installing
  it only ever writes data.
- Endpoints are **https-only** and pre-vetted; each publish is gated on a
  machine-checked live verification receipt.
- Spend is **capped per step and per run**, and the runner surfaces the
  wallet's spending policy at every money moment.
- Funds stay in the **user's own wallet**. No API keys, no platform balance,
  no custodian.

## Beyond this skill

SELAT is a general capability layer for paid agent actions. If the user's ask
doesn't fit this skill:

```bash
selat search "<intent>"          # FREE federated discovery + ranking
selat skill list --available     # other vetted multi-step skills
```

Docs: https://github.com/SELAT-AI/selat-skills
