# Phase 2 -- Your Moves, Parker

**From:** cc-mini
**Date:** 2026-02-26
**Branch:** `mini/phase2-relay` (ready, not merged to main yet)

Code is done. Build passes. These are the things only you can do.

## Now (before deploying)

- [ ] **Review the branch.** `git log main..mini/phase2-relay --oneline` in the memory-crystal repo. 4 commits including the cc-air relay merge.

- [ ] **Run migrate-db.** Moves crystal.db to `~/.ldm/memory/`. Stop gateway first.
  ```bash
  openclaw gateway stop
  cd ~/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude\ Code\ -\ Mini/repos/memory-crystal
  node dist/cli.js migrate-db
  openclaw gateway restart
  ```
  Verify: `node dist/cli.js status` should show data dir as `~/.ldm/memory/`.

- [ ] **Deploy updated plugin.** Copy built files to extension dir:
  ```bash
  cd ~/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude\ Code\ -\ Mini/repos/memory-crystal
  npm run build
  cp -r dist skills openclaw.plugin.json package.json ~/.openclaw/extensions/memory-crystal/
  cd ~/.openclaw/extensions/memory-crystal && npm install --omit=dev
  openclaw gateway restart
  ```

## When you're ready for relay (Air <-> Mini sync)

- [ ] **Generate encryption key:**
  ```bash
  openssl rand -base64 32 > ~/.openclaw/secrets/crystal-relay-key
  chmod 600 ~/.openclaw/secrets/crystal-relay-key
  ```

- [ ] **Copy key to MacBook Air** (same path, same permissions)

- [ ] **Cloudflare setup:**
  ```bash
  wrangler login
  wrangler r2 bucket create memory-crystal-relay
  wrangler secret put AUTH_TOKEN_CC_AIR    # generate a random token
  wrangler secret put AUTH_TOKEN_CC_MINI   # generate a random token
  wrangler secret put AUTH_TOKEN_LESA      # generate a random token
  wrangler deploy
  ```

- [ ] **Set env vars on Mini** (in your shell profile or launchd):
  ```
  CRYSTAL_RELAY_URL=https://memory-crystal-relay.<your-account>.workers.dev
  CRYSTAL_RELAY_TOKEN=<cc-mini bearer token>
  CRYSTAL_AGENT_ID=cc-mini
  ```

- [ ] **Set env vars on Air:**
  ```
  CRYSTAL_RELAY_URL=<same URL>
  CRYSTAL_RELAY_TOKEN=<cc-air bearer token>
  CRYSTAL_AGENT_ID=cc-air
  ```

- [ ] **End-to-end test:** Run a CC session on Air, check Mini picks it up via poller.

Full checklist with more detail: `ai/todos/parker/2026-02-25--cc-air--setup-checklist.md`

## Merge to main + release

- [ ] **Merge branch:** `git checkout main && git merge mini/phase2-relay`
- [ ] **Release:** `wip-release minor --notes="Phase 2: LDM scaffolding, JSONL archive, MD summaries, relay merge"`
