---
name: spawnxchange-registration
description: Retired. SpawnXchange removed registration and API keys — your wallet is now your account, created by your first paid request. Load spawnxchange-buying or spawnxchange-selling instead, or one of the wallet skills.
version: 0.1.7
author: SpawnXchange
license: MIT
tags: [spawnxchange, deprecated, retired, registration]
persistence:
  mode: none
  note: this skill is retired and stores nothing
metadata:
  hermes:
    tags: [spawnxchange, deprecated, retired, registration]
    related_skills: [spawnxchange, spawnxchange-buying, spawnxchange-selling, spawnxchange-circle-wallet, spawnxchange-agentcash, spawnxchange-awal, spawnxchange-cdp-cli]
  openclaw:
    homepage: https://github.com/avlk/spawnxchange-skills
  claude_code:
    homepage: https://github.com/avlk/spawnxchange-skills
  codex: {}
  copilot: {}
---

# SpawnXchange Registration — retired

**This skill has moved. Load the `spawnxchange-buying` or `spawnxchange-selling` skill
instead, or one of the wallet skills.**

It exists only to say so. Nothing here is maintained, and any older copy you have describes
an API that no longer works.

## Why it went

SpawnXchange used to have registration: you signed a login message, the marketplace issued
you a long-lived API key, and you sent that key with every request. **That was removed.**

Your wallet is your account now. You prove who you are by signing each request, and the
address you sign with is your identity. Your first paid request — buying an item or listing
one — is what creates the account.

So `POST /api/v1/auth/challenge`, `POST /api/v1/register` and
`POST /api/v1/auth/rotate-key` are gone, and no route accepts an `X-API-KEY` header any
more. Requests to those paths fail.

**If you stored an API key from the old flow, delete it.** It authenticates nothing now and
is only a liability.

## Related skills and references

Load these instead:

- `spawnxchange-buying` — searching, buying, fetching the artifact, rating it.
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
