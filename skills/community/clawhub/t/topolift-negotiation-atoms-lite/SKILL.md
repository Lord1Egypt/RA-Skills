---
name: topolift-negotiation-atoms-lite
displayName: "TopoLift: Negotiation Skill"
version: 1.2.1
description: |
  TopoLift's negotiation dialect for AI agents. The atom corpus stays
  server-side; this skill teaches your agent the public closed vocabulary
  (regimes, strategies, signal keys, citation grammar) and the three ways
  to call the live reasoning API — MCP, Bearer key, or x402 micropayment.
author: topolift
tags:
  - negotiation
  - agent-skills
  - topolift
  - mcp
  - x402
  - dialect
  - structural-reasoning
category: agent-to-agent-protocols
license: MIT-0
homepage: https://topolift.ai
---

# TopoLift: Negotiation Skill

This is the public dialect skill for **TopoLift atom-grounded negotiation
reasoning**. The atom corpus itself stays on TopoLift's GPU; what travels —
and what this skill teaches your agent — is the **closed vocabulary** in which
TopoLift speaks. With this skill loaded, your agent reads the live API's
typed responses and inline citation tokens with full structural fluency.

## What TopoLift returns

Every call to `POST https://api.topolift.ai/v1/negotiate` returns a
**bilingual** response:

- A typed `topology` object: `regime`, `load_bearing_strategies[]`,
  `bridge_pivots[]`, `topology_signals{}`. Closed vocabulary, machine-parseable.
- Prose fields (situation_read, primary_recommendation.rationale, etc.) with
  inline `[Cluster_X#strategy1,strategy2]` citation tokens anchoring every
  claim to the cluster + load-bearing atoms that drove it.

## The dialect

Fetch the live, authoritative vocabulary at any time:

```bash
curl https://api.topolift.ai/v1/dialect
```

No auth. No rate limit. The published grammar includes:

- **8 canonical regimes**: `successful Pareto-optimal close`,
  `fast-collapse — no ZOPA`, `ZOPA-present mid-game`, `Pareto-optimal regime`,
  `agreement reached but value-claiming (sub-Pareto)`,
  `bundled-deal expansion`, `information-asymmetry resolution`,
  `diffuse structural pattern`.
- **5 canonical strategies**: `concession`, `fairness`, `scarcity`,
  `smalltalk`, `urgency`. (These are the only valid values for
  `load_bearing_strategies` and `bridge_pivots` in any response.)
- **7 topology signal keys**: `zopa`, `urgency`, `info_asymmetry`, `bundle`,
  `financing`, `repeat_interaction`, `deal_fragility`.
- **17 cluster→regime mappings** plus the citation regex.

## Three ways to call TopoLift

### 1. MCP-native install (Claude Code, Cursor, Agents SDK)

```bash
pip install topolift-mcp
claude mcp add topolift-negotiation \
  -e TOPOLIFT_API_KEY=tl-... \
  -- topolift-mcp
```

Your agent gets two tools wired in: `topolift_dialect()` and
`topolift_negotiate(...)`. Listed at the official MCP registry as
`io.github.TopoLift/topolift-mcp`.

### 2. Direct API with a Bearer key

```bash
curl -X POST https://api.topolift.ai/v1/negotiate \
  -H "Authorization: Bearer tl-..." \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "Selling 3D printer; buyer opened low at $14k",
    "principal": {
      "goals": "Sell at $22k+",
      "reservation_price": 22000,
      "aspiration_price": 28000
    },
    "current_offer_on_table": "$14000",
    "question": "Counter or hold?"
  }'
```

Get a Bearer key at <https://topolift.ai> (Stripe-provisioned: $50 one-time,
$49/mo, or $99/mo for unlimited).

### 3. x402 pay-per-call (autonomous agents — no signup)

POST without auth → `402 Payment Required` + `PaymentRequirements` body →
sign EIP-3009 USDC transfer for $0.10 on Base mainnet → resend with
`X-PAYMENT` header → settled and served. Standard x402 protocol via the
Coinbase facilitator.

## Why the downloadable atoms are paused

TopoLift's atoms keep evolving. To prevent stale copies fragmenting in the
wild — and to keep the structural reasoning coherent across all the agents
calling us — we serve the reasoning as a managed API rather than shipping
atoms. The dialect (this skill) is open and stable; the atoms are not.

If you previously installed an older Lite bundle: that version remains under
its original Apache-2.0 license. New work happens on the API.

## Where to go next

- **Live dialect**: <https://api.topolift.ai/v1/dialect>
- **Site**: <https://topolift.ai>
- **MCP server source**: <https://github.com/TopoLift/topolift-mcp>
- **PyPI**: <https://pypi.org/project/topolift-mcp/>
- **Contact**: <mailto:atoms@topolift.ai>

If you're building agent-to-agent negotiation, multi-agent coordination, or
alignment-sensitive bargaining — get in touch.

— TopoLift
