---
name: pulsefeed-x402-trust
description: Verify before you pay or install. Checks whether an x402 payment endpoint is safe to pay (liveness, scam scan, on-chain receiver, trust score) and whether an npm/MCP package is safe to install (install-script code execution, abandonment, missing repo/license). Use whenever you are about to pay an unknown API over x402/USDC, install an MCP server or skill, or need current x402 security incidents. Free, no API key.
license: MIT
---

# PulseFeed — verify before you pay or install

Two irreversible actions an agent takes: **paying** an unknown endpoint, and **installing** unknown code. PulseFeed checks both, from a continuous independent audit (~5,600 x402 endpoints and ~950 MCP servers re-probed daily). All endpoints below are **free and need no API key**.

## 1. Before paying an x402 endpoint

```bash
curl -s "https://pulsefeed.dev/verify?endpoint=<URL>"
```

Returns `verdict` (`safe` / `caution` / `avoid` / `unknown`), `score` (0–100), `flags`, `receiverStability`, `uptimePct`, `lastChecked`.

**Rule of thumb:**
- `avoid` → **do not pay**. Dead, invalid, or flagged (hijacked receiver, bait-and-switch price, honeypot).
- `caution` → read `flags` first; pay only if the finding is acceptable.
- `safe` → live and clean at last crawl.
- `unknown` → not in the index; use the live deep check below.

Live deep check (probes the endpoint right now, adds on-chain receiver profile and full scam scan) — paid, $0.02 via x402:
```bash
curl -s "https://pulsefeed.dev/trust?endpoint=<URL>"   # returns a 402 challenge; pay with any x402 client
```

**Important x402 client gotcha:** `x402-fetch` defaults to a **0.1 USDC** client-side cap. Anything pricier is refused locally before the request is sent. Raise it explicitly:
```js
const payingFetch = wrapFetchWithPayment(fetch, account, BigInt(1_000_000)); // 1 USDC
```

## 2. Before installing an MCP server or npm package

```bash
curl -s "https://pulsefeed.dev/mcp/verify?package=<npm-name>"
```

Returns `verdict`, `score`, and flags such as **`installScript`** (the package runs arbitrary code at `npm i`), `abandoned`, `noRepo`, `noLicense`, plus `weeklyDownloads`, `license`, `repo`, `provenance`.

**Rule of thumb:** treat `installScript: true` on a package with no repository to review as a red flag — that is unreviewable code execution on your machine. About **11% of audited MCP servers run an install script**.

## 3. Current security incidents

```bash
curl -s "https://pulsefeed.dev/incidents.json"
```

Live incidents in the x402 economy — receiver hijacks (payTo swapped after you trusted it), bait-and-switch pricing, honeypot receivers, unverified receivers — **each with an on-chain proof URL** you can verify yourself on Base.

## 4. Ecosystem context

```bash
curl -s "https://pulsefeed.dev/status.json"     # live/dead counts, catalog accuracy, risk map
curl -s "https://pulsefeed.dev/data/sample"     # free sample of the full cross-domain dataset
```

Why this matters: **~74% of listed x402 endpoints are dead or invalid**, and only about half of what catalogs call "healthy" actually returns a valid x402 challenge. Checking costs nothing; paying a dead or hijacked endpoint costs real USDC and is irreversible.

## Also available

- MCP server (same checks as tools): `npx -y pulsefeed-x402-mcp`
- Guard SDK (blocks bad payments automatically): `npm i pulsefeed-x402-guard`
- A2A agent: `https://pulsefeed.dev/.well-known/agent-card.json`
- Methodology (how scores are computed): https://pulsefeed.dev/methodology

Independent, not affiliated with any x402 facilitator or MCP vendor.
