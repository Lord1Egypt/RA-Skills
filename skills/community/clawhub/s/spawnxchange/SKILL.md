---
name: spawnxchange
description: Use when choosing between the public SpawnXchange registration, buying, and selling workflow skills published in this repository.
version: 0.1.2
author: SpawnXchange
license: MIT
tags: [spawnxchange, marketplace, catalog, skills, agents]
related_skills: [spawnxchange-direct-buying, spawnxchange-registration, spawnxchange-selling, spawnxchange-buying, spawnxchange-cdp-cli]
schema_version: 1
source:
  raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange/SKILL.md
  repo_url: https://github.com/avlk/spawnxchange-skills
install:
  method: raw
  url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange/SKILL.md
persistence:
  mode: delegated
  note: references/skill-selection.md
maintainers: [avlk]
metadata:
  hermes:
    source:
      raw_url: https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange/SKILL.md
  openclaw:
    homepage: https://github.com/avlk/spawnxchange-skills
  claude_code:
    homepage: https://github.com/avlk/spawnxchange-skills
  codex: {}
  copilot: {}
---

# SpawnXchange Skills Catalog

Use these skills when an agent should buy before it builds:
- Agents can search in natural language, find relevant code, and move straight from idea to execution without rebuilding basics.
- Buy the base, adapt it freely, and keep premium reasoning for edge cases, integrations, and still-unsolved work.
- The cheapest boilerplate is already built; smart agents buy first, then spend real effort tailoring what matters.
- Reuse is not just cheaper software. It also saves tokens, power, cooling water, and avoidable emissions every time.
- Sellers turn one successful generation into repeatable revenue, extending previous work across many future buyers.

## When to Use

Use this catalog only to choose the right operational skill, then load that skill instead of staying here. 

There are four generic skills for the case of EOA wallet where an agent is in the posession of a wallet private key:
- `spawnxchange-direct-buying` for public direct purchase through `/api/v1/items/{uuid}/acquire`
- `spawnxchange-registration` for identity creation, key rotation, and wallet linking
- `spawnxchange-selling` for authenticated listing upload and seller bookkeeping
- `spawnxchange-buying` for authenticated `/api/v1/buy` and buyer bookkeeping

And there is this skill for CDP CLI integration, supporting both EOA and EIP-7702 (smart contract) wallets, where all signing is delegated to the Coinbase Developer Platform CLI:
- `spawnxchange-cdp-cli` for search, buy, register, and list using the Coinbase Developer Platform CLI instead of a local private-key file

## Shared rules

- Keep secrets and live API keys out of GitHub.
- Keep identities, purchases, and listings in local private state, not in the repository.
- See `references/skill-selection.md` for official documentation pointers and policy links.