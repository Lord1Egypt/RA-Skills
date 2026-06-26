# Parker ... Memory Crystal To-Do

**Updated:** 2026-03-02

---

## To Do

### Approve and Publish
- [ ] Approve PR #11 (`cc-mini/cloud-mcp` -> main)

### Testing (after publish)
- [ ] Local Memory: `crystal search` returns results, `crystal remember` works
- [ ] Multi-Device Sync: test encrypted drop + pickup between Mini and Air
- [ ] Cloud Memory: test OAuth flow from Claude web
- [ ] Import Memories: test Total Recall against one AI account
- [ ] Memory Consolidation: run Dream Weaver on a small memory set
- [ ] AI-to-AI Communication: verify Bridge messages save to Crystal
- [ ] Agent install flow: paste README onboarding prompt into fresh Claude Code session

### Blockers
- [ ] Enable R2 on Cloudflare dashboard (1 min, free tier ... CC-Mini can't do this)
- [ ] AirDrop `~/.openclaw/secrets/op-sa-token` to Air (physical transfer)

---

## Done

- [x] README review: feature naming, status markers, section reorg ... 2026-03-02
- [x] Doc updates: RELAY.md, TECHNICAL.md, README-ENTERPRISE.md match README ... 2026-03-02
- [x] Security audit: no hardcoded tokens in source code ... 2026-03-02
- [x] Step 1: Cloudflare Account ID in 1Password ... 2026-03-01
- [x] Step 2: Cloudflare API Token created, rolled, saved in 1Password ... 2026-03-01
- [x] Create 1Password item "Parker - Cloudflare Memory Crystal Keys" ... 2026-02-28
- [x] OpenAI API key in 1Password ... pre-existing
- [x] Review branch `mini/phase2-relay` ... 2026-02-26
- [x] Approve PR #2, squash-merge to main ... 2026-02-26

---

## Deprecated

- ~~Step 6: Test from devices (ChatGPT, Claude web)~~ ... blocked by R2 + deploy. Moved to Testing. (2026-03-02)
- ~~Remove LanceDB dual-write~~ ... Parker uses both. Dual-write stays. (2026-03-01)
- ~~Run migrate-db manually~~ ... CC-Mini handles this. (2026-03-01)
- ~~Deploy updated plugin manually~~ ... CC-Mini handles builds and deploys. (2026-03-01)
- ~~Generate encryption key manually~~ ... CC-Mini generates it. (2026-03-01)
- ~~Run wrangler commands~~ ... CC-Mini runs all wrangler via API token. (2026-03-01)
- ~~Set env vars on Mini and Air~~ ... CC-Mini handles env config. (2026-03-01)
- ~~Run deploy script~~ ... CC-Mini runs deploy. (2026-03-01)
- ~~Test health/OAuth endpoints via curl~~ ... CC-Mini does verification. (2026-03-01)
- ~~Wrangler login (browser auth)~~ ... API token works directly. (2026-03-01)
