# Parker — Setup Checklist (Ephemeral Relay)

Everything you need to do to get the encrypted relay live.

## 1. Generate Encryption Key (once, shared across machines)

```bash
openssl rand -base64 32 > ~/.openclaw/secrets/crystal-relay-key
chmod 600 ~/.openclaw/secrets/crystal-relay-key
```

Copy `~/.openclaw/secrets/crystal-relay-key` to both machines (Air + Mini).
This key never goes to Cloudflare. It stays on your hardware.

**How to copy:**
- AirDrop the file
- Or from one machine: `cat ~/.openclaw/secrets/crystal-relay-key` → paste on the other
- Or copy via the FireWire shared disk

## 2. 1Password Service Account Token (MacBook Air)

The Air needs the same service account token that's on the Mini.

- [ ] Copy `~/.openclaw/secrets/op-sa-token` from the Mac Mini
- [ ] Paste it to `~/.openclaw/secrets/op-sa-token` on the MacBook Air
- [ ] Run `chmod 600 ~/.openclaw/secrets/op-sa-token`

## 3. Cloudflare Setup

- [ ] Install wrangler (if not already): `npm install -g wrangler`
- [ ] Run `wrangler login` (opens browser, authenticates)

### Create R2 Bucket

```bash
cd /Users/parker/Documents/dev-wip/repos/memory-crystal
wrangler r2 bucket create memory-crystal-relay
```

### Set Secrets

Generate three bearer tokens (one per agent):
```bash
openssl rand -hex 32
```

- [ ] Set cc-air token: `wrangler secret put AUTH_TOKEN_CC_AIR`
- [ ] Set cc-mini token: `wrangler secret put AUTH_TOKEN_CC_MINI`
- [ ] Set lēsa token: `wrangler secret put AUTH_TOKEN_LESA`

**Save the cc-air token** — you'll need it for the Air's env config.
**Save the cc-mini token** — you'll need it for the Mini's poller config.

### Deploy

- [ ] Deploy the Worker:
  ```bash
  wrangler deploy
  ```
  Note the URL (e.g., `https://memory-crystal-relay.wipcomputer.workers.dev`)

### Verify

- [ ] Test health endpoint:
  ```bash
  curl https://memory-crystal-relay.wipcomputer.workers.dev/health
  ```
  Should return: `{"ok":true,"service":"memory-crystal-relay","mode":"ephemeral"}`

## 4. Configure MacBook Air (cc-air)

Set these environment variables (in `~/.zshrc` or Claude Code hook config):

```bash
export CRYSTAL_RELAY_URL="https://memory-crystal-relay.wipcomputer.workers.dev"
export CRYSTAL_RELAY_TOKEN="<cc-air bearer token from step 3>"
export CRYSTAL_AGENT_ID="cc-air"
```

The cc-hook will auto-detect relay mode when these are set.

## 5. Configure Mac Mini (cc-mini poller)

Set these environment variables:

```bash
export CRYSTAL_RELAY_URL="https://memory-crystal-relay.wipcomputer.workers.dev"
export CRYSTAL_RELAY_TOKEN="<cc-mini bearer token from step 3>"
```

### Set up poller (cron or launchd):

**Option A: Cron (every 2 min)**
```bash
crontab -e
# Add:
*/2 * * * * cd /path/to/memory-crystal && node dist/poller.js 2>> ~/.openclaw/logs/relay-poller.log
```

**Option B: LaunchAgent (recommended)**
Create a plist for continuous polling with `--watch` mode.

**Option C: Manual**
```bash
node dist/poller.js              # poll once
node dist/poller.js --watch      # poll continuously
node dist/poller.js --push-mirror # push mirror snapshot
```

## 6. Verify End-to-End

1. Talk to cc-air on the MacBook Air
2. Check relay has a blob: `curl -H "Authorization: Bearer <mini-token>" https://memory-crystal-relay.wipcomputer.workers.dev/pickup/conversations`
3. Run the poller on Mini: `node dist/poller.js`
4. Verify chunks ingested into master crystal: `node dist/cli.js status`
5. Push mirror: `node dist/poller.js --push-mirror`
6. Pull mirror on Air: `node dist/mirror-sync.js`
7. Search on Air — should return results from the conversation

## Quick Reference

| What | Where |
|------|-------|
| Encryption key | `~/.openclaw/secrets/crystal-relay-key` (both machines) |
| SA token | `~/.openclaw/secrets/op-sa-token` (both machines) |
| Repo | `/Users/parker/Documents/dev-wip/repos/memory-crystal` |
| Branch | `cc-air/phase2-relay` |
| Worker config | `wrangler.toml` |
| Air env vars | `CRYSTAL_RELAY_URL`, `CRYSTAL_RELAY_TOKEN`, `CRYSTAL_AGENT_ID` |
| Mini env vars | `CRYSTAL_RELAY_URL`, `CRYSTAL_RELAY_TOKEN` |

## What's NOT on Cloudflare

- No encryption keys
- No API keys
- No database
- No search capability
- No ability to read the data
- Just auth tokens and encrypted blobs that auto-expire in 24h
