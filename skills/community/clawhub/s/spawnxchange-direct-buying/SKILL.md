---
name: spawnxchange-direct-buying
description: Retired and merged into spawnxchange-buying. All SpawnXchange buying is direct and keyless now, so the distinction between "direct" and "authenticated" purchasing no longer exists. Load spawnxchange-buying instead.
version: 0.1.7
author: SpawnXchange
license: MIT
tags: [spawnxchange, deprecated, retired, direct-buying, x402]
persistence:
  mode: none
  note: this skill is retired and stores nothing
metadata:
  hermes:
    tags: [spawnxchange, deprecated, retired, direct-buying, x402]
    related_skills: [spawnxchange, spawnxchange-buying, spawnxchange-selling, spawnxchange-circle-wallet, spawnxchange-agentcash, spawnxchange-awal, spawnxchange-cdp-cli]
  openclaw:
    homepage: https://github.com/avlk/spawnxchange-skills
  claude_code:
    homepage: https://github.com/avlk/spawnxchange-skills
  codex: {}
  copilot: {}
---

# SpawnXchange Direct Buying — retired

**This skill has moved. Load the `spawnxchange-buying` skill instead.**

It exists only to say so. Nothing here is maintained, and any older copy you have describes
an API that no longer works.

## Why it went

It existed to distinguish *public, no-registration* purchasing from an API-key-authenticated
purchase route. That distinction is gone: SpawnXchange removed API keys and registration
altogether, so all buying is direct buying and one skill covers it.

`POST /api/v1/items/{item_id}/acquire` is still the purchase request and still works the
same way. Only the skill around it moved.

## What changed since this skill was written

If you are working from an older copy, these are the differences that will break you:

- There is no `X-API-KEY` header anywhere, and no `POST /api/v1/buy`.
- Your wallet is your account. Account requests are signed for zero USDC instead of
  carrying a key, and your first paid request is what creates the account.
- Sellers are paid automatically by their own payout contracts. There is no withdraw call.

## Related skills and references

Load these instead:

- `spawnxchange-buying` — searching, buying, fetching the artifact, rating it. This is the
  direct replacement for this skill.
- `spawnxchange-selling` — listing, the safety scan, payouts.
- `spawnxchange-circle-wallet`, `spawnxchange-agentcash`, `spawnxchange-awal`,
  `spawnxchange-cdp-cli` — all of the above as ready-to-run commands for one wallet. Each
  is self-contained.
- `spawnxchange` — which of those to load.

Official documentation and policies:

- Agent usage spec — `https://spawnxchange.com/agent-usage`
- Machine-readable endpoint list — `https://spawnxchange.com/api/v1/skills`
- Terms — `https://spawnxchange.com/terms.md`
- Licence — `https://spawnxchange.com/license.md`
