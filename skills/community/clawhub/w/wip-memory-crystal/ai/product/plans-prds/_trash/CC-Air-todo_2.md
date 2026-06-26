# CC-Air ... Memory Crystal To-Do

**Updated:** 2026-03-02

---

## To Do

### LDM Setup
- [ ] Run `crystal init --agent cc-air` on MacBook Air (scaffolds ~/.ldm/, deploys capture script, installs cron)
- [ ] Verify cron running: check `/tmp/ldm-dev-tools/crystal-capture.log`

### Relay Setup (blocked: R2 + deploy)
- [ ] Verify relay key at `~/.openclaw/secrets/crystal-relay-key`
- [ ] Verify env vars: `CRYSTAL_RELAY_URL`, `CRYSTAL_RELAY_TOKEN`, `CRYSTAL_AGENT_ID=cc-air`
- [ ] Test cc-hook relay mode: run a session, verify encrypted drop at Worker
- [ ] Test mirror-sync pull: verify crystal.db mirror downloads and decrypts

### Plugin Deploy
- [ ] Deploy Memory Crystal plugin to `~/.openclaw/extensions/memory-crystal/` on Air (if OpenClaw runs there)
- [ ] Deploy cc-hook to Claude Code settings on Air

---

## Done

- [x] Phase 2 relay code built (cc-hook relay mode, crypto, poller, mirror-sync) ... 2026-02-26
- [x] Branch `cc-air/phase2-relay` merged into `mini/phase2-relay` ... 2026-02-26
- [x] All HOME fallbacks fixed (no hardcoded paths) ... 2026-02-26

---

## Deprecated

- ~~LDM scaffolding code~~ ... completed by cc-mini (ldm.ts, crystal init). cc-air just runs it. (2026-02-26)
- ~~Poller expansion~~ ... completed by cc-mini during relay merge. (2026-02-26)
- ~~Three file types (JSONL, MD, crystal.db)~~ ... completed by cc-mini. (2026-02-26)
- ~~Manual relay setup (env vars, keys)~~ ... crystal init + crystal pair handles most of this now. (2026-03-02)
