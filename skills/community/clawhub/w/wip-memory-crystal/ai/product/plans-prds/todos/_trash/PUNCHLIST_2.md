# Memory Crystal ... Punchlist

**Updated:** 2026-02-28
**Repo:** `wipcomputer/memory-crystal-private`

## Active: Cloud MCP Server (PR #10)

Code is written and compiling. These are the steps to get it live.

### 1. Merge + Release
- [ ] Review and merge PR #10 (`mini/dev` -> `main`)
- [ ] `wip-release minor --notes="Cloud MCP server for ChatGPT + Claude (6 surfaces, 2 tiers)"`

### 2. Create D1 Database
```bash
cd cloud
npx wrangler d1 create memory-crystal-cloud
```
- [ ] Copy the `database_id` into `cloud/wrangler.toml`

### 3. Run Migrations (remote)
```bash
npm run cloud:db:migrate:remote
```
- [ ] Verify tables: `oauth_clients`, `authorization_codes`, `access_tokens`, `users`

### 4. Set Secrets
```bash
cd cloud
npx wrangler secret put CRYSTAL_RELAY_KEY      # same base64 key as local relay
npx wrangler secret put OAUTH_SIGNING_SECRET   # any random string
npx wrangler secret put OPENAI_API_KEY         # for Tier 2 embeddings (future)
```
- [ ] `CRYSTAL_RELAY_KEY` ... must match the key in `~/.openclaw/secrets/` (same one the poller uses)
- [ ] `OAUTH_SIGNING_SECRET` ... generate with `openssl rand -hex 32`
- [ ] `OPENAI_API_KEY` ... can use the same key from 1Password

### 5. Deploy Cloud Worker
```bash
npm run cloud:deploy
```
- [ ] Verify health: `curl https://memory-crystal-cloud.<account>.workers.dev/health`
- [ ] Verify OAuth discovery: `curl .../.well-known/oauth-authorization-server`

### 6. Redeploy Relay Worker (new channels)
The relay worker needs the `chatgpt` + `chatgpt-attachments` channels.
```bash
npm run build:worker
cd .. && npx wrangler deploy --config wrangler.toml
```
- [ ] Verify relay health: `curl https://memory-crystal-relay.<account>.workers.dev/health`

### 7. Test OAuth Flow
- [ ] POST `/oauth/register` with ChatGPT redirect URI
- [ ] GET `/oauth/authorize` shows consent page
- [ ] POST consent with email, get auth code
- [ ] POST `/oauth/token` with PKCE verifier, get access token
- [ ] POST `/mcp` with Bearer token, call `tools/list`

### 8. Test End-to-End
- [ ] Call `memory_remember` via MCP ... verify encrypted drop appears in R2
- [ ] Call `memory_log` with a conversation turn ... verify drop in R2
- [ ] Run poller (`node dist/poller.js`) ... verify drops picked up and ingested
- [ ] `crystal search` for the remembered text ... verify it's in crystal.db
- [ ] Check `~/.ldm/agents/gpt-web/memory/transcripts/` for JSONL files
- [ ] Call `memory_upload` with a small base64 image ... verify attachment saved

### 9. Connect ChatGPT
- [ ] ChatGPT > Developer Mode > Add MCP server
- [ ] Enter Worker URL as the MCP endpoint
- [ ] Complete OAuth consent flow
- [ ] Test: "remember that I prefer dark mode"
- [ ] Test: have a conversation, verify `memory_log` fires every turn
- [ ] Verify data appears on Mini after poller runs

### 10. Connect Claude
- [ ] Claude > Settings > Connectors > Add remote MCP server
- [ ] Enter same Worker URL
- [ ] Complete OAuth consent flow
- [ ] Test same as ChatGPT

### 11. Directory Submissions (when ready)
- [ ] Privacy policy at `/docs/privacy` (real content, not placeholder)
- [ ] Terms of service
- [ ] Security disclosure at `/docs/security` (real content)
- [ ] Submit to ChatGPT Apps Directory (OpenAI)
- [ ] Submit to Anthropic Connectors Directory
- [ ] Developer verification with both platforms

### 12. Start Poller Daemon
The poller needs to run continuously to pick up cloud drops.
- [ ] Add `--chatgpt` awareness to existing poller LaunchAgent, or
- [ ] Confirm `--watch` mode covers both channels (it does)
- [ ] Verify poller is running: `node dist/poller.js --status`

---

## Architecture Direction

Three features, one product:
1. **Memory** ... remember, search, forget. One SQLite DB. Any AI tool.
2. **Bridge** ... local agent-to-agent communication. All messages saved to crystal.
3. **Relay** ... multi-device sync. Remote agents communicate and share memory.
4. **Cloud** ... ChatGPT + Claude MCP server. Relay to Mini. Six surfaces.

All writes go to the crystal. Always. No matter which layer.

## Backlog (not blocking ship)

- [ ] Absorb lesa-bridge into Memory Crystal as Bridge feature
- [ ] Absorb context-embeddings into Memory Crystal (retire plugin)
- [ ] Remove LanceDB dual-write
- [ ] `crystal backfill` for ~115 historical sessions
- [ ] Point Dream Weaver at `~/.ldm/` transcripts
- [ ] Tier 2: CloudCrystal class (D1 + Vectorize), mirror sync, real search
- [ ] Tier 2: wip-agent-pay integration at consent page
- [ ] QR pairing wizard (`crystal pair` ... key + relay URL + done)

## Completed

- [x] Cloud MCP server: 6 tools, OAuth 2.1, PKCE, consent page ... 2026-02-28
- [x] Poller: chatgpt channel, 4 drop types, attachment decryption ... 2026-02-28
- [x] Relay worker: chatgpt + chatgpt-attachments channels ... 2026-02-28
- [x] System instructions for Custom GPT / Claude connector ... 2026-02-28
- [x] PR #10 created ... 2026-02-28
- [x] Push `mini/phase2-relay` ... 2026-02-26
- [x] Create PR #2, squash-merge to main ... 2026-02-26
- [x] Deploy build to `~/.ldm/extensions/memory-crystal/` ... 2026-02-27
- [x] Migrate crystal.db to `~/.ldm/memory/crystal.db` (159K+ chunks, symlink at old path) ... 2026-02-26
- [x] Fix lesa-bridge session routing (`user: "claude-code"` for dedicated TUI-visible session) ... 2026-02-27
