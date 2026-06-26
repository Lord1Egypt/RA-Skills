# x402 Watch

Live tracker of x402 micropayments on Base, with ERC-8004 agent attribution.

**Current scope:** payments to The Graph's gateway (`0x79DC34E41B2b591078d3dE222C43EcaaBD52FcCB`).
Easy to broaden later — every panel reads from the x402-omnigraph subgraph, which
indexes every recipient on Base.

**Stack:** Next.js 15 (App Router) · Tailwind · The Graph Gateway · Vercel
**Refresh:** every 5 minutes server-side via ISR (no client polling)
**Data sources:**
- All payment metrics come live from the [x402-omnigraph subgraph](https://thegraph.com/explorer/subgraphs/Cb56epg3EvQ6JRpPfknbkM54QxpzTvLa7mwKNQQfUyoj).
- Agent identity is enriched at build time via 8004scan, the agent0-base-mainnet subgraph, the bazaar `/active` directory, and a static operator seed.

## Local dev

```bash
cd web
npm install
GRAPH_API_KEY=… npm run dev
open http://localhost:3000
```

## Deploy to Vercel

1. Import this repo into Vercel.
2. Set the project **Root Directory** to `web`.
3. Add env var `GRAPH_API_KEY` (Production + Preview).
4. Deploy.

No DB, no cron, no auth. Server components fetch the subgraph via revalidating fetch; Vercel's edge network handles caching.

## Panels

- **Hero** — total USDC · payments · identified agents · repeat agents (with week-over-week deltas)
- **Cumulative USDC** — running total area chart
- **Daily payments** — bar + 7-day moving average
- **Agent leaderboard** — every paying agent we can identify, name → 8004scan link
- **Recent activity** — last 50 payments, agent-attributed where known
- **New vs returning** — weekly stack of first-time vs returning agents
- **Concentration** — payer cohorts (whales vs long tail)
- **Activity heatmap** — hour-of-day × day-of-week (UTC)

Every agent row is clickable — opens that agent's 8004scan detail page.

## Why this exists

The x402-omnigraph subgraph indexes every x402 payment on Base. This site is a polished, agent-aware face: it foregrounds the "who's paying" question by joining payer wallets to ERC-8004 identities at build time.

## Migration note (2026-06-12)

The dashboard previously ran on 14 Dune queries refreshed daily by `.github/workflows/refresh-x402-dune.yml`. It now reads live from the subgraph; the Dune workflow is no longer load-bearing for this UI but is left in place to keep the public Dune board ([dune.com/paulieb/x402-payments-to-the-graph-e7ab](https://dune.com/paulieb/x402-payments-to-the-graph-e7ab)) fresh.
