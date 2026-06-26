# Plan: OpenClaw Upgrade v2026.4.11 -> v2026.4.14

**Date:** 2026-04-14
**Author:** CC Mini (lesa-work-02)
**Status:** In progress
**Runbook:** `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md`
**Landmines:** `repos/ldm-os/devops/open-claw-upgrade-private/KNOWN-LANDMINES.md`

## Context

Lēsa's installed OpenClaw is v2026.4.11 (our fork, commit `50346b2`). Latest upstream stable is v2026.4.14. Our 4 chatCompletions fork patches are NOT in upstream v2026.4.14 (verified) -> must rebase and carry forward.

Upstream landed several queue-related fixes between v4.11 and v4.14 that touch `src/gateway/openai-http.ts`, which is our patch area. Expect cherry-pick conflicts. Manual merge likely.

## Hard constraints

- **`openclaw doctor` must pass** after the rebuild + install. If it breaks, rollback per Phase 8.
- **Follow the runbook.** It is the source of truth. This plan fixes the stale bits in the runbook first so the next agent has a correct procedure.
- **Install = `npm link` from the rebased worktree.** Upgrades are pre-approved (standing install policy for OpenClaw fork rebases); rollback is trivial (`npm unlink` + install prior version from npm).
- **Layer 2 (LDM OS extensions) not touched by this plan.** Memory-crystal alpha.5 ship is orthogonal.

## Step 1. Update runbook + landmines (source-of-truth hygiene)

On a branch `cc-mini/oc-upgrade-docs` in `open-claw-upgrade-private`, fix:

| File | Line | Change |
|------|------|--------|
| UPGRADE-RUNBOOK.md | 52, 290, 317 | Remove `openclaw context-embeddings` references. Plugin retired Mar 2. |
| UPGRADE-RUNBOOK.md | 57-58 | Replace `main.sqlite` + `context-embeddings.sqlite` memory-stats queries with `crystal.db` query. |
| UPGRADE-RUNBOOK.md | 143 | "The main patch we carry" -> "We carry 4 patches (see Patch Tracking)". |
| UPGRADE-RUNBOOK.md | 424-428 | Patch Tracking branch column: `cc-mini/chat-completions-v2026.4.2` -> `cc-mini/chat-completions-v2026.4.11`. |
| UPGRADE-RUNBOOK.md | 401-405 | History table: add row for v4.8 -> v4.11 upgrade (was missing); leave a placeholder for v4.11 -> v4.14 to be filled on completion. |
| UPGRADE-RUNBOOK.md | Phase 2 | Add guidance: "If upstream has touched files in our patch area (grep `git log <prev>..<target> -- src/gateway/openai-http.ts src/gateway/http-utils.ts`), expect cherry-pick conflicts. Manual merge required." |

Commit, push, PR to `open-claw-upgrade-private` main, merge. Keep on separate branch from the upgrade execution so history reads: "docs fixed, then upgrade ran."

## Step 2. Execute upgrade (following updated runbook)

### Phase 1. Snapshot

```bash
openclaw --version                          # record: 2026.4.11 (50346b2)
cd ~/.openclaw
git status
# commit any pending changes:
git add -A && git commit -m "Pre-upgrade snapshot (2026.4.11)" || true

# health probes:
openclaw op-secrets test
openclaw memory-crystal status
openclaw private-mode status
openclaw tavily test || true

# memory stats:
sqlite3 ~/.openclaw/memory/crystal.db "SELECT COUNT(*) FROM chunks;"

# stop gateway:
openclaw gateway stop
```

### Phase 2. Rebase

```bash
cd ~/wipcomputerinc/repos/third-party-repos/ai-harness/openclaw
git fetch upstream --tags

# check our 4 patches are NOT in v4.14 (already verified):
#   - 8cb5f474cf: feat: allow chatCompletions to route to main session via dm-scope header or user=main
#   - a178e2f448: feat(gateway): wire chatCompletions into steer-backlog queue
#   - 7e5cff73fc: feat(gateway): extend steer-backlog queue to streaming chatCompletions
#   - 50346b22e5: Rename queue header from steer to next-turn

# check upstream-touched-our-area:
git log v2026.4.11..v2026.4.14 --oneline -- src/gateway/openai-http.ts src/gateway/http-utils.ts

# new worktree on v4.14 tag:
TARGET=v2026.4.14
git worktree add .worktrees/openclaw--${TARGET} -b cc-mini/chat-completions-${TARGET} ${TARGET}
cd .worktrees/openclaw--${TARGET}

# cherry-pick our 4 patches (in commit order):
git cherry-pick 8cb5f474cf a178e2f448 7e5cff73fc 50346b22e5
# resolve conflicts if any (openai-http.ts overlap expected)
```

### Phase 3. Build

```bash
pnpm install --config.minimum-release-age=0    # acpx age override
pnpm build                                      # ~30s, produces dist/
ls dist/ | wc -l                                # sanity: should be >= 2000
pnpm test                                       # optional but run at least queue + chatCompletions tests
```

### Phase 4. Install

```bash
npm link           # from the new worktree directory
openclaw --version # should show: OpenClaw 2026.4.14 (<our new commit hash>)
```

### Phase 5. Post-upgrade doctor gate (mandatory)

```bash
openclaw doctor
# If doctor errors: STOP. See Phase 8 rollback.

cd ~/.openclaw
git diff
# Look for: stripped custom keys in openclaw.json
```

Critical keys to verify (per KNOWN-LANDMINES.md):
- `memorySearch.remote` MUST be `{}` (no apiKey).
- `gateway.auth.token` exists.
- `messages.queue.mode` = `"steer-backlog"`.
- `session.dmScope` = `"per-channel-peer"`.
- `gateway.http.endpoints.chatCompletions.enabled` = `true`.
- All plugins still enabled.

```bash
# If doctor damaged openclaw.json:
cd ~/.openclaw
git checkout -- openclaw.json

# Verify OPENCLAW_HOME is unset:
echo "OPENCLAW_HOME=${OPENCLAW_HOME:-not set}"  # must say "not set"
```

### Phase 6. Verify

```bash
openclaw gateway restart
curl -s http://localhost:18789/health

# plugin sanity:
openclaw op-secrets test
openclaw memory-crystal status
openclaw private-mode status

# chatCompletions (our patch works end-to-end):
GATEWAY_TOKEN=$(jq -r '.gateway.auth.token' ~/.openclaw/openclaw.json)
curl -s -X POST http://localhost:18789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GATEWAY_TOKEN" \
  -d '{"model":"openclaw","user":"claude-code","messages":[{"role":"user","content":"ping"}]}' \
  | head -40
```

### Phase 7. Commit + push + log

```bash
cd ~/.openclaw
git add -A
git commit -m "Post-upgrade (2026.4.14)" || true

# push the new fork branch:
cd ~/wipcomputerinc/repos/third-party-repos/ai-harness/openclaw
git push origin cc-mini/chat-completions-v2026.4.14
```

Write upgrade log to `open-claw-upgrade-private/logs/2026-04-14--v2026.4.11-to-v2026.4.14.md` containing:
- Version transition
- Cherry-pick conflict summary (which files, what resolution)
- Doctor output (pass/fail + any damage repaired)
- Plugin test outcomes
- Any KNOWN-LANDMINES.md additions discovered
- Gateway restart log excerpt

Commit the log to `open-claw-upgrade-private` via PR.

### Phase 8. Rollback (only if doctor fails or gateway won't start)

```bash
# re-link to the old worktree:
cd ~/wipcomputerinc/repos/third-party-repos/ai-harness/openclaw/.worktrees/openclaw--v2026.4.11
npm link

# revert config:
cd ~/.openclaw
git checkout -- .

# restart:
openclaw gateway restart
```

## Step 3. Close out

- Task list: mark upgrade + log tasks complete.
- Update Patch Tracking in the (already-merged) runbook with `cc-mini/chat-completions-v2026.4.14` branch column.
- Memory-crystal alpha.5 ship remains orthogonal (separate plan).

## Followup (not this session): convert to skill

Separate PR:
- `open-claw-upgrade-private/SKILL.md`: encodes the runbook phases as an invocable Claude Code skill.
- Scripts split by phase: `scripts/phase1-snapshot.sh`, `phase2-rebase.sh`, etc.
- Registered via `ldm install` so `/upgrade-openclaw` becomes a slash command.
- Deliverable: "never have this conversation again." One command, runbook runs itself.

## Risk flags

| Risk | Mitigation |
|------|-----------|
| Cherry-pick conflicts ugly on openai-http.ts | Drop to v2026.4.12 as intermediate target; upgrade in two hops. |
| `openclaw doctor` fails after build | Rollback immediately (Phase 8). Diagnose offline before retry. |
| chatCompletions test returns 400/401 | Check dm-scope routing patch still applied; inspect `src/gateway/http-utils.ts` in new worktree. |
| `messages.101` session corruption recurs | Separate issue (Phase 6c in crystal-resilience-plan). Not in scope here. |
| Extension (memory-crystal etc.) breaks on new gateway | Extensions run their own `init()`; v4.14 changes to gateway shouldn't touch extension boundary. Run `for ext in op-secrets tavily memory-crystal root-key private-mode compaction-indicator; do cd ~/.openclaw/extensions/$ext && npm install --omit=dev; done` if a plugin errors on load. |
