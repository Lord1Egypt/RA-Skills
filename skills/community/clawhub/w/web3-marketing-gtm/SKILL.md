---
name: web3-marketing-gtm
description: >
  Full-stack Web3 marketing and GTM brain for AI agents and bots. Use this skill whenever a bot or agent needs to
  produce any of the following from a project brief: a GTM launch plan, a campaign calendar, community engagement
  scripts for Discord/Telegram/X, or an on-chain user acquisition and retention strategy. Trigger this skill when
  input includes a project name, blockchain/chain, and product type — even if the request is phrased casually like
  "build me a go-to-market for my DeFi app" or "write me a Discord campaign for my NFT project" or "how do I grow
  my Web3 community". This skill covers the full marketing lifecycle: pre-launch, launch week, post-launch growth,
  and retention loops. Always use this skill for Web3 marketing tasks rather than improvising.
---

# Web3 Marketing & GTM Skill

A structured playbook for AI agents to produce professional, execution-ready Web3 marketing assets from a minimal
project brief. No human hand-holding required — this skill handles strategy, content, and sequencing end-to-end.

---

## Input: Project Brief

The minimum required input is:

```
Project Name: <name>
Chain: <e.g. Avalanche, Base, Solana, Ethereum>
Product Type: <e.g. DeFi protocol, NFT collection, GameFi, payments app, oracle, social dApp>
```

Optional enrichers (use if provided):
- Target audience (e.g. degens, retail users, developers, DAOs)
- Key differentiator or value prop
- Existing community size / metrics
- Launch date or timeline
- Token: yes/no, TGE planned

If any required field is missing, ask for it before proceeding. Do not hallucinate chain or product type.

---

## Output Suite

From a single brief, produce all four deliverables in sequence:

1. **GTM Launch Plan** → See `references/gtm-plan.md`
2. **Campaign Calendar** → See `references/campaign-calendar.md`
3. **Community Engagement Scripts** → See `references/community-scripts.md`
4. **On-Chain Retention Strategy** → See `references/onchain-retention.md`

Each reference file contains the full template, logic, and formatting rules for that deliverable.

---

## Execution Flow

```
RECEIVE brief
  │
  ▼
VALIDATE inputs (name, chain, product type present?)
  │ if missing → ASK
  ▼
INFER defaults (see Defaults section below)
  │
  ▼
PRODUCE deliverables in order:
  1. GTM Launch Plan
  2. Campaign Calendar
  3. Community Scripts
  4. On-Chain Retention Strategy
  │
  ▼
OUTPUT as structured markdown document
```

Always produce all four deliverables unless the user explicitly requests fewer. Label each section clearly.

---

## Defaults & Inference Rules

When optional fields are missing, apply these defaults:

| Missing Field       | Default Assumption                                              |
|---------------------|-----------------------------------------------------------------|
| Target audience     | Crypto-native users (18–35, active on X and Discord)           |
| Differentiator      | Derive from product type (e.g. DeFi → yield/efficiency angle)  |
| Community size      | Assume 0 (greenfield launch)                                   |
| Launch timeline     | Assume 4-week runway from today                                 |
| Token               | No token; focus on product-native incentives                   |

---

## Tone & Voice Rules for All Content

Web3 marketing content produced by this skill must follow these principles:

- **No hype language**: avoid "revolutionary", "game-changing", "to the moon", "LFG" in strategy docs
- **Education first**: lead with what the product does and why it matters
- **Specificity over vagueness**: use real timelines, real metrics targets, real actions
- **Community-native**: Discord = conversational, X = punchy/informational, Telegram = direct/update-focused
- **Selling never**: content informs and invites, it does not pitch or pressure

---

## Reference Files

Read the relevant reference file when producing each deliverable:

| Deliverable                   | File                                  | When to Read              |
|-------------------------------|---------------------------------------|---------------------------|
| GTM Launch Plan               | `references/gtm-plan.md`             | Always — read first       |
| Campaign Calendar             | `references/campaign-calendar.md`    | Always — read second      |
| Community Scripts             | `references/community-scripts.md`    | Always — read third       |
| On-Chain Retention Strategy   | `references/onchain-retention.md`    | Always — read fourth      |

Read all four before producing output. Do not skip reference files.

---

## Quality Checklist

Before finalizing output, verify:

- [ ] All four deliverables are present and labeled
- [ ] No placeholder text remains (e.g. "[INSERT HERE]")
- [ ] Chain-specific details are accurate (e.g. AVAX ≠ ETH gas model)
- [ ] Tone is consistent: no hype, no vagueness
- [ ] Campaign calendar has specific dates/weeks, not just "Week 1"
- [ ] Scripts are platform-appropriate (length, tone, format)
- [ ] Retention strategy references on-chain actions, not just social metrics
