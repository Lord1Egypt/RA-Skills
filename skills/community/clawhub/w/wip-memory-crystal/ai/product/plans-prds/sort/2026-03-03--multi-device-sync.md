# Plan: Multi-Device Sync (Mac mini -> MacBook Air)

**Date:** 2026-03-03
**Author:** CC-Mini
**Context:** Parker wants to test the full multi-device sync flow. Mac mini is the brain (source of truth, does embeddings). MacBook Air gets a synced local copy. Every Mac feels like a full local install.

---

## What Already Exists (code complete, not deployed)

Almost everything is already written:
- `src/worker.ts` ... Cloudflare Worker relay (R2 dead drop, encrypted)
- `src/poller.ts` ... Mini polls relay for conversation drops
- `src/mirror-sync.ts` ... Air pulls encrypted DB snapshot
- `src/crypto.ts` ... AES-256-GCM + HMAC-SHA256
- `src/pair.ts` ... QR code pairing (key sharing)
- `src/cc-hook.ts` ... already has RELAY mode (drops at relay instead of local ingest when CRYSTAL_RELAY_URL is set)
- Relay key already exists on Mini: `~/.openclaw/secrets/crystal-relay-key`

## What Needs to Happen

### Step 1: Deploy the Relay Worker to Cloudflare

**Files:** `worker.ts`, `wrangler.toml`
**What:** Deploy the encrypted dead drop relay to Cloudflare Workers + R2
**Commands:**
```bash
cd memory-crystal-private
wrangler r2 bucket create memory-crystal-relay
# Set auth secrets:
wrangler secret put AUTH_TOKEN_CC_MINI --config wrangler.toml
wrangler secret put AUTH_TOKEN_CC_AIR --config wrangler.toml
npm run build:worker
wrangler deploy --config wrangler.toml
```
**Result:** Relay live at a Cloudflare URL. Two channels: /conversations (Air -> Mini) and /mirror (Mini -> Air)

### Step 2: Configure Mini as Source of Truth

**On the Mini, set env vars** (in `~/.zshrc` or equivalent):
```bash
export CRYSTAL_RELAY_URL=<relay-worker-url>
export CRYSTAL_RELAY_TOKEN=<mini-auth-token>
```

**Add cron job on Mini** to push mirror after ingestion:
```bash
# After the existing crystal-capture cron, add mirror push
*/5 * * * * node ~/.ldm/extensions/memory-crystal/dist/poller.js --push-mirror
```

This makes the Mini: capture conversations -> embed -> push encrypted DB snapshot to relay every 5 minutes.

### Step 3: Install Memory Crystal on MacBook Air

Parker does this manually to test the flow:
```bash
npm install -g memory-crystal
crystal init --agent cc-air
```

### Step 4: Pair the Devices

```bash
# On Mini:
crystal pair
# Shows QR code + mc1:... string

# On Air:
crystal pair --code mc1:...
```

Both machines now share the encryption key.

### Step 5: Configure Air as Sync Client

**On the Air, set env vars:**
```bash
export CRYSTAL_RELAY_URL=<relay-worker-url>
export CRYSTAL_RELAY_TOKEN=<air-auth-token>
export CRYSTAL_AGENT_ID=cc-air
```

**Add cron on Air for mirror sync:**
```bash
*/5 * * * * node ~/.ldm/extensions/memory-crystal/dist/mirror-sync.js
```

**What happens automatically:**
- cc-hook.ts detects CRYSTAL_RELAY_URL, switches to RELAY mode
- Air captures conversations -> encrypts -> drops at relay
- Mini polls relay -> decrypts -> ingests into crystal.db -> embeds
- Mini pushes encrypted DB snapshot to relay
- Air pulls snapshot -> decrypts -> replaces local crystal.db
- Air now has full searchable database locally

### Step 6: Register MCP Server on Air

```bash
claude mcp add --scope user memory-crystal -- crystal-mcp
```

Air's Claude Code now has crystal_search, crystal_remember, crystal_forget, crystal_status. Searches hit the local (synced) copy of crystal.db. Fast, offline-capable.

---

## Data Flow Summary

```
MacBook Air                    Cloudflare R2              Mac mini
                               (encrypted relay)

capture conversation
  -> encrypt
  -> POST /drop/conversations  -> store blob
                                                          poll /pickup/conversations
                                                            -> decrypt
                                                            -> embed
                                                            -> ingest into crystal.db

                                                          push mirror:
                               store blob  <-             encrypt crystal.db
                                                            -> POST /drop/mirror
pull /pickup/mirror
  decrypt
  replace local crystal.db <-

Local search works.
```

---

## What Might Need Code Changes

1. **poller.ts --push-mirror**: Verify this mode exists and works. May need a CLI flag or separate script.
2. **mirror-sync.ts**: Verify it can run standalone from cron (not just imported).
3. **cc-hook.ts relay drop**: The relay mode exists but verify it works with the current capture flow (cc-poller.ts also needs relay awareness, not just cc-hook.ts).
4. **crystal init on second device**: Should detect it's a secondary device if relay vars are set. May want to skip cron setup or set up mirror-sync cron instead.
5. **Auth tokens in 1Password**: Store relay tokens in Agent Secrets vault for both machines.

---

## Test Plan (Parker on MacBook Air)

```
[ ] Deploy relay worker to Cloudflare
[ ] Set auth secrets on worker
[ ] Verify relay health: curl <relay-url>/health
[ ] Pair devices (crystal pair on Mini, crystal pair --code on Air)
[ ] Install memory-crystal on Air (npm install -g memory-crystal)
[ ] crystal init --agent cc-air on Air
[ ] Set env vars on Air (CRYSTAL_RELAY_URL, CRYSTAL_RELAY_TOKEN, CRYSTAL_AGENT_ID)
[ ] Set env vars on Mini (CRYSTAL_RELAY_URL, CRYSTAL_RELAY_TOKEN)
[ ] Start a Claude Code conversation on Air
[ ] Verify conversation drops at relay (check relay /pickup/conversations)
[ ] Verify Mini picks up and ingests (crystal status shows new chunks)
[ ] Trigger mirror push from Mini
[ ] Verify Air pulls mirror (crystal status on Air shows chunks)
[ ] Search on Air: crystal search "something from Mini history"
[ ] Confirm results come back. Local search on synced database. Works.
```

---

## Unknowns / Risks

- **DB size**: crystal.db is 170K+ chunks. Encrypted + uploaded every 5 min could be large. May need to do incremental sync instead of full DB snapshot. Check file size first.
- **sqlite-vec compatibility**: Air needs same sqlite-vec version. npm install -g should handle this.
- **Embedding provider on Air**: Air doesn't need one if it's only doing relay drops (Mini does embeddings). But crystal_search on Air needs the vectors in the synced DB, which should work since they're in sqlite-vec already.
- **Cron on Air**: crystal-capture.sh runs on cron, but on Air it should relay instead of local ingest. Need to verify cc-poller.ts respects CRYSTAL_RELAY_URL.
