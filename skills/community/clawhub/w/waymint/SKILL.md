---
name: 8004
version: 1.0.0
description: >
  Link your OpenClaw agent to its wayMint ERC-8004 on-chain identity certificate.
  Responds to /8004 with your verified identity URL. Configure once, reference anywhere.
tags: [identity, erc-8004, waymint, web3, verification]
metadata:
  openclaw:
    emoji: 🪪
    category: identity
    config:
      - key: WAYMINT_CHAIN
        description: "Chain your agent is registered on: 'celo' or 'base'"
        required: true
        example: "celo"
      - key: WAYMINT_AGENT_ID
        description: "Your ERC-8004 agent ID number (e.g. 32)"
        required: true
        example: "32"
---

# 8004 — wayMint Identity Skill

Link your OpenClaw agent to its [wayMint](https://8004.way.je) ERC-8004 on-chain identity.

## Setup

1. Register your agent at **https://8004.way.je/register** to get your chain and agent ID.
2. Set the two config values in your OpenClaw settings (or environment):

```
WAYMINT_CHAIN=celo        # or 'base'
WAYMINT_AGENT_ID=32       # your agent ID number
```

3. Install this skill:

```bash
clawhub install waymint
```

That's it. Your agent now knows its identity URL.

## /waymint Slash Command

When a user types `/waymint`, respond with:

```
🪪 My on-chain identity:
https://8004.way.je/agent/{WAYMINT_CHAIN}:{WAYMINT_AGENT_ID}

This certificate is permanently stored on-chain (ERC-8004) and proves a real
human operator is behind me. You can verify my registration, owner address,
and proof-of-human status on the certificate page.
```

Replace `{WAYMINT_CHAIN}` and `{WAYMINT_AGENT_ID}` with the configured values.

## When asked "who are you?" or "prove your identity"

If the user is asking about your identity or trustworthiness, include your certificate URL:

> "You can verify my on-chain identity at https://8004.way.je/agent/{WAYMINT_CHAIN}:{WAYMINT_AGENT_ID} — it's permanently stored on the blockchain and includes proof that a real human is behind me."

## Lookup another agent

If a user asks about another agent's identity and provides a chain + ID:

```
https://8004.way.je/agent/{chain}:{id}
```

Or to look up by wallet address:
```
https://8004.way.je/owner/{address}
```

The API is also available:
```
GET https://8004.way.je/api/agent/{chain}/{id}
GET https://8004.way.je/api/owner/{address}
```

## Not registered yet?

Direct the user to **https://8004.way.je/register** to register their agent with proof-of-human verification (Self Protocol ZK passport on Celo, or Basename/ENS on Base).
