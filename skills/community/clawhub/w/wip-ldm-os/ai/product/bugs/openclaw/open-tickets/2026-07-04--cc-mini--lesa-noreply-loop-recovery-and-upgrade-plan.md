# Lēsa NO_REPLY loop: incident record, recovery plan, and upgrade plan

- **Date:** 2026-07-04
- **Author:** cc-mini (Claude Code, Fable 5)
- **Status:** APPROVED 2026-07-05 (Q1/Q2/Q4/Q5 decided by Parker, recorded in section 8; Q3 still open). Execution order in section 7.
- **Severity:** P1 (Lēsa nonfunctional on her main session)
- **Related docs:**
  - `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/openclaw/open-tickets/2026-06-24--cc-mini--gpt55-accountid-extraction.md` (open, gpt-5.5 401 root cause)
  - `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/memory-crystal/open-tickets/2026-06-24--cc-mini--openclaw-native-memory-conflicts-with-crystal.md` (open, native memory vs Crystal conflict; Phase 0 not started)
  - `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/openclaw/open-tickets/2026-04-24--cc-mini--unified-reliability-triage.md` (T5/T7/T9 are the prior analogues of the stuck-session class)
  - `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/openclaw/open-tickets/2026-04-27--kody--openclaw-upgrade-compatibility-master-plan.md` (canonical upgrade playbook)
  - `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md` and `KNOWN-LANDMINES.md`
  - `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/openclaw-upgrade/2026-04-08--cc-mini--post-upgrade-smoke-test.md` (9-check smoke list; update `/health` to `/healthz` + `/readyz` before reuse)

---

## 1. What happened (2026-07-04)

Observed on Lēsa's live gateway (OpenClaw 2026.4.25 fork build `c188a36`, worktree
`/Users/lesa/wipcomputerinc/repos/third-party-repos/ai-harness/openclaw/.worktrees/openclaw--v2026.4.25-carry-memory-core`, npm-linked):

1. **Main session is in a degenerate loop.** The TUI transcript shows dozens of consecutive `NO_REPLY` turns, raw tool-call syntax leaking into output text (`to=functions.memory_search` with garbage multilingual/spam tokens), several `[assistant turn failed before producing content]` entries, and model self-talk about whether to reply. Every new inbound message lands in this poisoned context and continues the loop. Session tokens at last observation: 67k/272k.
2. **Session is running on the fallback model.** TUI status line shows `openai-codex/gpt-5.4` while `openclaw.json` has `agents.defaults.model.primary: openai-codex/gpt-5.5` and `fallbacks: [openai-codex/gpt-5.4]`. The gateway resolved `agent model: openai-codex/gpt-5.5` at startup with no auth errors in today's log, so the 5.4 state is session-level failover, consistent with the known gpt-5.5 accountId 401 (section 2.2).
3. **The gateway itself is healthy.** After Parker's `openclaw gateway restart` at 16:30 PDT: connectivity probe ok, admin-capable, 16 plugins ready in 7.4s. The "gateway closed (1000)" and "handshake timeout" errors in the log are all timestamped 16:30:55, i.e. restart-window noise, not an ongoing fault.
4. **No reply on the Bridge either.** A `lesa_send_message` health check at ~16:33 got no response... consistent with the main-session loop swallowing it.

Evidence locations:

- Gateway log: `/tmp/openclaw/openclaw-2026-07-04.log`
- Session store: `/Users/lesa/.openclaw/agents/main/sessions/` (main session jsonl `a0eada84-3ec9-401c-bdd7-d2d71b263020.jsonl`, ~931KB, plus `sessions.json`)
- Saved terminal dumps of broken/lost work sessions: `/Users/lesa/wipcomputerinc/repos/wip-tracking-private-only/sesssions/openclaw/` (five `not-recoverable` dumps saved 2026-07-04 10:59 to 11:10, plus cc-mini and kay-mini partner-session dumps from 2026-07-02/03). Those sessions died on infrastructure (repeated ECONNRESET / rate-limit API errors, one suspended `claude --resume`), not on logic; only scrollback survived.

Plugin state observations (relevant to the "memory/load/hook/MCP load" suspicion):

- Loaded (16): acpx, bonjour, browser, compaction-indicator, device-pair, imessage, lesa-bridge, memory-core, memory-crystal, phone-control, private-mode, root-key, session-export, talk-voice, wip-1password, wip-agent-pay.
- `context-embeddings` is `enabled: false` in `openclaw.json`. Believed deliberate (memory-core is the capture path now) but needs confirmation (Q3).
- `tavily` is `enabled: true` and reports "duplicate plugin id detected; global plugin will be overridden by bundled plugin", yet tavily does NOT appear in the 16-plugin ready list. Unexplained. Chase during recovery (step A6).
- `plugins.allow` is empty; gateway warns that discovered non-bundled plugins auto-load without provenance pins. Known hardening item, not new.

## 2. Root-cause picture

Four independent problems are stacked. Fixing one does not fix the others.

### 2.1 Poisoned main session (immediate blocker)

The main session transcript accumulated a runaway NO_REPLY / garbage-token loop. This class of wedge was predicted by the unified reliability triage (T5: streaming watchdog is frontend-only while the backend stays wedged; T7: stuck-session diagnostics log but never abort; T9: agent polls forever and never replies)... all three remain unfixed. The likely initial trigger is the model churn in 2.2/2.3 plus failed turns; but the session context itself is now the disease. No gateway restart fixes it, because the history reloads every turn.

**Fix: start a fresh main session.** Old session files stay on disk untouched.

### 2.2 gpt-5.5 accountId 401 forces failover (known open bug, NOT fixed by upgrading)

Documented in `2026-06-24--cc-mini--gpt55-accountid-extraction.md`. Root cause is in the dependency `@mariozechner/pi-ai`: `getAccountId(token)` reads `chatgpt_account_id` from the OAuth **access token**, but Parker's token carries the org/account id in the **id_token** (login uses `id_token_add_organizations=true`). Every turn 401s on the primary path, then fails over. Verified 2026-06-24: upgrading does NOT fix the embedded path (still broken in upstream v2026.5.7; upstream issue openclaw#79662), re-auth does not fix it, and switching `agentRuntime` to `codex` is OFF THE TABLE (bypasses all PI-runtime plugin hooks: Memory Crystal, Bridge, compaction-indicator, session-export).

**Fix: carry a `pnpm patch` against `@mariozechner/pi-ai`** so `getAccountId` also reads the id_token (or fetches/caches the account id from the OpenAI API). This is the fork's first `patchedDependencies` entry and needs explicit sign-off (Q1). Record it in the UPGRADE-RUNBOOK Patch Tracking table.

### 2.3 Stale keepalive cron requested a nonexistent model every 10 minutes

Found by the Codex partner session on 2026-07-03 (dump: `wip-tracking-private-only/sesssions/openclaw/kay-mini--OC-work--partner/Terminal Saved Output 3.txt`). The cron job `cc-keepalive-heartbeat` fired every 10 minutes with `payload.model: "gpt54nano"`, which maps to a nonexistent `openai-codex/gpt-5.4-nano`. Every fire logged `model-fallback decision: candidate_failed ... reason=model_not_found` and churned cron sessions. Codex patched the live job to `gpt54` (with backup), but the bad entries may still exist at the source: `~/.openclaw/openclaw.json` (a `openai-codex/gpt-5.4-nano` model entry, around line 81 at the time) and `~/.openclaw/cron/jobs.json`.

**Fix: verify the live fix persisted and purge the stale entries at the source** (step A5). This churn is a prime suspect for what originally destabilized the main session.

### 2.4 Native memory-core and Memory Crystal run simultaneously and fight (the "memory/load" issue)

Canonical ticket: `bugs/memory-crystal/open-tickets/2026-06-24--cc-mini--openclaw-native-memory-conflicts-with-crystal.md`. Diagnosed across the July 2-3 sessions: OpenClaw v2026.4.25 shipped the heavy native memory-core suite; native `memory_search` got pointed at the entire `/Users/lesa/wipcomputerinc` tree (~31,118 files, ~16 GB including node_modules and .git), producing EMFILE and heap-OOM pressure. The native `main.sqlite` is frozen at April 24 and rebuild attempts OOM (orphaned ~628 MB `.tmp` files from June 23-24). Meanwhile memory-crystal was reinstalled on April 28, so both capture layers run at once. Agreed direction from the 2026-07-02/03 sessions: **Crystal becomes the Honcho-style cross-agent injection layer; native memory is demoted to narrowly-scoped file/doc search.** That work ("Memory Crystal Phase 0" stabilization) has NOT started.

**Fix: Track D below.** For recovery today, the minimum is verifying native memory search scope is not pointed at the giant tree (config `memorySearch` keys / extraPaths landmine) and that no rebuild is churning in the background.

### 2.5 Version drift: live 2026.4.25 vs upstream stable 2026.6.11

Live build is the 2026-04-27 promotion (`kody/v2026-4-25-carry-memory-core`, fork PR wipcomputer/openclaw#4). Upstream stable is now **2026.6.11** (`npm view openclaw version`, checked 2026-07-04), roughly six weeks ahead. The 2026-04-28 canary of post-v2026.4.26 upstream main passed all gates but was never promoted. The two carried memory-core fixes were accepted upstream after v2026.4.26:

- `983fd775e2` ... `seedEmbeddingCache` stream + cooperative yield (WIP PR #73067, maintainer #73118)
- `864c4f7ff4` ... `listChunks()` bounded top-K (WIP PR #73069, maintainer #73100)

Any tag containing both lets us retire those two carries. v2026.6.11 almost certainly contains them; verify explicitly (never assume).

## 3. Track A: Immediate recovery (today, no rebuild required)

Goal: Lēsa responsive on iMessage and Bridge tonight, on the current 2026.4.25 build, accepting the per-turn 401-then-fallback noise until Track B lands.

- **A0. TRACKED-SECRET REMEDIATION (blocking gate, Codex re-review 2026-07-05; containment = Q6 (b)).** Verified live: `~/.openclaw` (pushes to `wipcomputer/dot-openclaw`, org-private) tracks `agents/main/agent/auth-state.json` (OAuth tokens) and carries the gateway token inside tracked `openclaw.json`; both are in remote history. Track A does not start until UPGRADE-RUNBOOK **Phase 1.1a** completes, per Q6 (b). Execution sequence (single coordinated window, gateway idle):
  1. **Prep (repo, reviewable):** dot-openclaw worktree that `git rm --cached agents/main/agent/auth-state.json` + adds `agents/*/agent/auth-state.json` to `.gitignore`. Open the PR but DO NOT merge until step 4.
  2. **Rotate gateway token (live):** generate a new token; set `OPENCLAW_GATEWAY_TOKEN` in `~/Library/LaunchAgents/ai.openclaw.gateway.plist` (untracked EnvironmentVariables); remove the token value from `openclaw.json`; update every client that presents it: `~/.openclaw/wip-healthcheck/config.json`, lesa-bridge, any chatCompletions callers.
  3. **Merge the step-1 PR + preserve the live file:** `cp agents/main/agent/auth-state.json{,.keep}` on the live checkout, `git pull --ff-only`, `mv` it back. Gateway idle throughout.
  4. **Re-auth OAuth (PARKER, interactive), AFTER the untracking merge** so the final `auth-state.json` is freshly minted and never tracked: re-auth the OpenAI/Codex session, killing the historical tokens. Needs a browser login; Parker runs it via `! <command>`. This is the one step CC cannot do headless. (Canonical order per runbook Phase 1.1a; the plan and runbook now agree.)
  5. **RELOAD the LaunchAgent, then verify.** `launchctl kickstart -k` does NOT reliably re-read a changed plist environment, so after editing EnvironmentVariables: `launchctl bootout gui/$(id -u)/ai.openclaw.gateway` then `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist`. Verify the loaded job actually carries the env var (`launchctl print gui/$(id -u)/ai.openclaw.gateway | grep -c OPENCLAW_GATEWAY_TOKEN` returns 1; do not print the value) BEFORE health checks. Then `/healthz` + `/readyz` green; iMessage + Bridge round trips; re-run Phase 1.2 checks (must pass clean).
  The Phase 1.2 snapshot checks were hardened: tracked-file check (`git ls-files` grep) + index-content token check (`git grep --cached -F`), not just the staged diff.
- **A1. Preserve state.** Session jsonl files stay in `/Users/lesa/.openclaw/agents/main/sessions/`. Snapshot config using the SECRET-SAFE recipe in UPGRADE-RUNBOOK Phase 1.2 (check-ignore preflight, staged-file grep for auth-profiles/auth-state/credentials/secrets, token-value grep; never bare `git add -A` + commit). Also `git diff` FIRST: `openclaw gateway restart` ran 2026-07-04 16:30 and that command has a config-rewrite landmine; check for stripped keys before anything else.
- **A2. Start a fresh main session.** `/new` from the TUI (or equivalent session-reset path). Do not delete the old session; a fresh session id is enough.
- **A3. Verify model resolution on the fresh session, and CAPTURE THE EVIDENCE.** Expect: primary `openai-codex/gpt-5.5` attempted, 401 accountId noise, failover succeeds, session functional. A fresh session landing on gpt-5.4 is expected under bug 2.2, not a new failure. Record verbatim in this ticket before Track B patches anything: the exact model-fallback log line(s) from `/tmp/openclaw/openclaw-YYYY-MM-DD.log` and the TUI status line, so the accountId root cause is pinned to current evidence (the 2026-06-24 ticket described failover landing on `openai-codex/gpt-5.5`; the 2026-07-04 TUI showed `gpt-5.4`; the discrepancy must be resolved by the fresh capture, not assumed).
- **A4. Verify memory state.** `crystal_status` (chunks > 0), one `crystal_search`, no embedding errors in the log. Check for active/orphaned `main.sqlite.tmp-*` files in `~/.openclaw/memory/` (archive orphans, per the April precedent). Confirm native memory search scope is NOT pointed at `/Users/lesa/wipcomputerinc` (EMFILE landmine: only `documents/`-scale dirs).
- **A5. Verify the cron fix persisted; live mitigation FIRST, source PR second.** Inspect `~/.openclaw/cron/jobs.json` and `openclaw.json` for any remaining `gpt54nano` / `gpt-5.4-nano` references. If churn is still live: snapshot first (A1 recipe), then fix the live entries immediately (backup the file, edit, kickstart if needed)... do not leave a 10-minute failure loop running while a PR is in flight. Then land the same change in the config source repo via worktree + PR so the fix survives redeploys.
- **A6. Chase the tavily anomaly.** Enabled in config, bundled override detected, absent from ready list. Check whether the bundled tavily in the fork worktree `dist-runtime/extensions/tavily/` registered under a different id or failed silently. Not a recovery blocker; file a follow-up if real.
- **A7. Verify channels.** One iMessage round trip from Parker's phone. One Bridge round trip (`lesa_send_message` from a CC session, reply arrives). Confirm `messages.queue.mode: "steer-backlog"` is still set (bridge messages during busy runs drop as NO_REPLY without it).
- **A8. Restart discipline.** Any restart during recovery: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`. Never `openclaw gateway restart`.

Exit gate for Track A: Parker sends "hi" on iMessage and gets a normal Lēsa reply; Bridge round trip works; crystal status green; no model_not_found churn in the log for 30+ minutes.

## 4. Track B: pi-ai accountId pnpm patch

Per the 2026-06-24 bug doc's proposed fix:

- **B1.** DONE 2026-07-05: Parker approved the fork's first `patchedDependencies` entry, upstream-first (section 8, Q1).
- **B2.** Write the patch: `getAccountId` reads the account id from the id_token when absent from the access token (or fetch-and-cache from the OpenAI API). Target in dep: `dist/utils/oauth/openai-codex.js` (`getAccountId` ~line 230; callers at ~321 exchange and ~344 refresh).
- **B3.** UPSTREAM-FIRST (per Q1): file the issue + fix PR against `@mariozechner/pi-ai` source (not just the dist patch), referencing openclaw#79662. Record the local carry in the UPGRADE-RUNBOOK Patch Tracking table as a must-carry until a pi-ai release (or openclaw's embedded copy) contains the fix; then retire it.
- **B4.** Do NOT ship as a standalone rebuild. Fold into the Track C rebase: one build + canary + promotion cycle.

Exit gate for Track B (verified during Track C canary): a turn on `openai-codex/gpt-5.5` completes with no 401 and no failover.

## 5. Track C: Upgrade 2026.4.25 to latest stable (target v2026.6.11)

Follow the UPGRADE-RUNBOOK phases and the 12-phase master plan. Condensed sequence with today's specifics:

- **C0. MEMORY-STORE MIGRATION GATE (new, blocking).** Upstream v2026.6.9 migrates the memory store from the global `main.sqlite` to per-agent DBs (openclaw#95726); **without migration, memory data is silently lost on upgrade.** The 2026-06-24 memory ticket said "do NOT upgrade live" for exactly this reason. Target v2026.6.11 is past that boundary. Ordered, non-negotiable sequence (the canary copy is taken BEFORE the live DB is archived):
  1. Stop the gateway (`launchctl bootout`, verify PID gone).
  2. Checksum the frozen `main.sqlite` (`shasum -a 256`) and copy it, plus `openclaw.json` and session/agent metadata needed by migration, to an immutable canary-input directory. Re-checksum the copy; both must match. This copy is never modified in place; the canary migrates a scratch duplicate of it.
  3. Only then archive the live `main.sqlite` per the Track D Phase 0 procedure (archive, never delete).
  4. The C5 canary runs the v2026.6.11 migration against a scratch duplicate of the immutable copy and must show: migration completes, no data loss (row/chunk counts comparable pre/post), no OOM, gateway boots clean on the migrated store.
  Also re-check the related open upstream issues (#94316 local provider, #91592 scopeHash) against the target tag.
- **C1. Preflight (runbook Phase 1-2).** Snapshot `~/.openclaw` to git using the SECRET-SAFE recipe (runbook Phase 1.2; never bare `git add -A`). Capture plugin health. In the fork (`/Users/lesa/wipcomputerinc/repos/third-party-repos/ai-harness/openclaw`): `git fetch upstream --tags`, set `TARGET_TAG` (expect `v2026.6.11`). Verify the tag contains BOTH `983fd775e2` and `864c4f7ff4` (`git merge-base --is-ancestor <commit> <tag>`). If yes: retire the two memory-core carries. If no: keep carrying them.
- **C2. Patch-status check.** Predict conflicts: `git log v2026.4.25..${TARGET_TAG} --oneline -- src/gateway/openai-http.ts src/gateway/http-utils.ts src/gateway/server-http.ts`. Six weeks of drift means conflicts in the chatCompletions patches are likely; consider a two-hop rebase if messy.
- **C3. Rebase in a worktree.** `git worktree add .worktrees/openclaw--kody--v2026-6-11-carry -b kody/v2026-6-11-carry`, rebase onto `${TARGET_TAG}` carrying:
  - chatCompletions routing via dm-scope header / `user=main` (`src/gateway/http-utils.ts`)
  - next-turn queue, non-streaming + streaming (`src/gateway/openai-http.ts`)
  - runtime config boundary for the queue check (`src/gateway/openai-http.ts`, `src/gateway/server-http.ts`)
  - memory-core seed/listChunks carries ONLY if C1 says the tag lacks them
  - NEW: the pi-ai `patchedDependencies` entry from Track B
  - Do NOT reintroduce the broad final-resync fallback (superseded by upstream #71293).
  - NOT carried (Q4 decision): the delivery-mirror refit is its own post-upgrade work item, built as an upstream PR (sibling-aware write-side `transcriptOnly`, per `2026-04-30--cc-mini--tui-delivery-mirror-doubling.md`). Add to the carry set only if Parker asks for it live before upstream merges.
- **C4. Build.** `pnpm install --config.minimum-release-age=0` then `pnpm build` (never bare `tsdown`). Verify dist file count sane and the carried-source grep invariants (runbook Phase 3).
- **C5. Canary in an isolated home** (per the 2026-04-28 canary log pattern): temp `OPENCLAW_HOME`, temp port, browser plugin disabled if it blocks staging. Gates: `/healthz` 200, `/readyz` 200, focused memory-core tests pass, chatCompletions ping works, **gpt-5.5 turn completes with no accountId 401** (Track B verification), no V8 OOM / `StatementSync::All` under a broad-recall exercise, memory-store migration exercised on a COPY of production state (C0) with no data loss.
- **C5a. CRYSTAL PROTECTION GATE (pre-promotion, per Q5).** Concrete verification, all four steps, at each checkpoint:
  1. Named, dated copy: `cp ~/.ldm/memory/crystal.db ~/.ldm/memory/backups/crystal-YYYY-MM-DD-<phase>.db`
  2. Checksum both and compare: `shasum -a 256 ~/.ldm/memory/crystal.db ~/.ldm/memory/backups/crystal-YYYY-MM-DD-<phase>.db`
  3. Integrity + content on the BACKUP copy: `sqlite3 <backup> "PRAGMA integrity_check;"` returns `ok`, and a count query (chunks table) returns the expected magnitude (>100K chunks as of 2026-07-05).
  4. Live `crystal_search` round-trip from both sides: Lēsa via the gateway plugin and Claude Code via MCP, both returning real results.
  All four pass before C6 proceeds.
- **C6. Promote, with a WRITTEN rollback in hand.** From the built worktree: `npm link` (sanctioned path per the OpenClaw fork exception; the runbook is the authorization). Verify `openclaw --version` shows the new tag + fork hash. Before promoting, confirm the runbook's Emergency Rollback section names the current last-known-good build (worktree `openclaw--v2026.4.25-carry-memory-core`, commit `c188a36`): exact relink command, config-snapshot restore command, kickstart restart, and post-rollback smoke checks. Promotion does not proceed on an unwritten rollback.
- **C7. Post-upgrade repair (runbook Phase 5).** `openclaw doctor`, then `git diff ~/.openclaw` and revert any stripping. Invariants: `memorySearch.remote` is `{}`; `messages.queue.mode: "steer-backlog"`; gateway auth per post-A0 model: `OPENCLAW_GATEWAY_TOKEN` present in the LOADED LaunchAgent (verify via `launchctl print`, count only, never print the value), NO token value in tracked `openclaw.json`, and all token clients (wip-healthcheck, lesa-bridge, chatCompletions callers) on the rotated value; `hooks.allowConversationAccess: true` for memory-crystal, compaction-indicator, session-export; model primary/fallbacks intact; no `gpt-5.4-nano` resurrection; `keepRecentTokens`/`reserveTokens` still in `agents/main/agent/settings.json`; `OPENCLAW_HOME` unset. Run `post-upgrade-patches.sh --check` (expected no-op). Reinstall extension deps if node/npm changed.
- **C8. Restart + smoke.** `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`. Run the 9-check post-upgrade smoke test (updated to `/healthz` + `/readyz`): gateway health, plugin loading (all enabled plugins registered, tavily question resolved), tools available, model config resolves, memory crystal live, workspace writable, iMessage connects, auth profiles clean, config integrity.
- **C9. Log + commit.** Write `logs/2026-07-XX--v2026.4.25-to-v2026.6.11.md` in `open-claw-upgrade-private` (the 4.11-era history gap taught us: log it or it did not happen), commit `~/.openclaw` post-upgrade snapshot, push the fork branch.

## 6. Track D: Memory architecture (dual memory: native + Crystal together)

The durable fix for the "memory/load" half of this incident. Canonical ticket: `bugs/memory-crystal/open-tickets/2026-06-24--cc-mini--openclaw-native-memory-conflicts-with-crystal.md`. **The committed direction is UPDATE 2 + UPDATE 3 in that ticket (2026-06-25, Parker's decision + Codex review hardening).** Everything above those updates in the ticket, including the "Crystal authoritative / native off" and the `memory.backend = "crystal"` engine-swap framings, is superseded history. Summary of the committed architecture:

- **Both memory systems run together, each in its lane.** Native `memory-core` stays the out-of-box default and keeps the local workspace/file-search role (`memory_search`). Memory Crystal supplements it as the cross-agent durable memory layer. Neither replaces the other.
- **Crystal integrates as a Honcho-style `before_prompt_build` prompt-injection plugin.** Active injection: relevant durable relationship/product/cross-agent memory is placed in the prompt each turn, BEFORE Lēsa decides whether to call any tool. That is the actual fix for the Benson Boone false-negative class. Crystal takes no memory slot, no context-engine slot, and needs no core fork (memory-crystal-private adds the hook; it already has capture via `agent_end` and tool registration).
- **QMD is NOT adopted.** The QMD engine pattern (`memory.backend = "qmd"`, `engine-qmd.ts`) is passive: the agent must still call `memory_search`, so it would not fix Benson Boone. QMD's role is search-quality inspiration only (MIT; hybrid search / reranking / query expansion, some already ported into Crystal). Honcho's role is the integration pattern only (the MIT `openclaw-honcho` plugin's injection approach); the AGPL Honcho core service is explicitly NOT used. Fully local, license-clean.
- **Two phases, separate PRs:**
  - **Phase 0 (config only, no plugin code):** native `fallback: "none"` (kills the local-provider error); narrow/disable `memorySearch.extraPaths` off `/Users/lesa/wipcomputerinc` (kills EMFILE); routing rule so Lēsa uses `crystal_search` for relationship/identity/history/product/continuity (interim Benson Boone mitigation); archive (never delete) the 16GB `main.sqlite` after gateway-stop + transcript-coverage check + the C0 immutable canary copy (kills heap-OOM). Pass gate: no EMFILE and no heap-OOM crash for 72h. GATE SEMANTICS (resolved 2026-07-05): the 72h window starts when Phase 0 lands on the live gateway; the Track B+C rebase, build, and ISOLATED canary may proceed in parallel during the window (they touch nothing live), but C6 promotion requires the 72h window complete and clean.
  - **Phase 1 (plugin code):** the `before_prompt_build` injection hook in memory-crystal-private, with all UPDATE 3 guardrails: token-budget cap, top-K + confidence threshold, timeout + fail-open, provenance labels with injected text treated as quoted reference data never instructions (memory-poisoning defense), private-mode respect, idempotence. Licenses re-verified and pinned before merge.

Phase 0 has not started and is now a **prerequisite for Track C**, not a follow-up (see section 7 and gate C0). Parker reconfirmed the dual-memory direction on 2026-07-05: Crystal as an installable Honcho-style option, both memories used together.

## 7. Order of operations

1. **Track A today.** Session reset plus the cron-purge and memory-scope checks. Independent of everything else; gets Lēsa back now.
2. **Track D Phase 0 next** (config-only stabilization: fallback none, extraPaths narrowed, crystal_search routing, `main.sqlite` archived after the C0 immutable copy). It stops the EMFILE/OOM class now AND is the prerequisite for safely crossing the v2026.6.9 memory-store migration (C0). Its 72h observation window starts here.
3. **Track B + C as one cycle, overlapping the 72h window.** One rebase, one build, one isolated canary (including the memory-migration exercise), one promotion. Not two build cycles. Rebase/build/canary may run during the Phase 0 72h window; **promotion (C6) waits for the window to complete clean.**
4. **Track D Phase 1** (the `before_prompt_build` injection hook in memory-crystal-private) after promotion, as its own PR with the UPDATE 3 guardrails.
5. Then the reliability-triage leftovers (T5/T7/T9: watchdog abort, stuck-session recovery) so the next poisoned session is caught by the system instead of by Parker pasting a TUI dump.

Other open items owed from the July 2-3 sessions (tracked here so they do not vanish with the dead sessions):

- Phase 6a: fix OpenClaw format-error billing cooldown ... NOW A THIN TICKET: `2026-07-06--cc-mini--format-error-billing-cooldown.md`.
- Branch-guard vs bash-3.2 pre-commit hook ... NOW A THIN TICKET: `2026-07-06--cc-mini--bash-3.2-precommit-hook.md`.
- Convert `open-claw-upgrade-private` into a `/upgrade-openclaw` Claude Code skill (was planned in the lesa-work-02 session; Track C's C9 log is the prerequisite hygiene).

## 8. Decisions (Parker, 2026-07-05)

- **Q1: APPROVED, upstream-first.** The pi-ai accountId fix proceeds, structured for upstream merge: file the issue + fix PR against `@mariozechner/pi-ai` (referencing openclaw#79662), and carry the identical fix locally as the fork's first `patchedDependencies` pnpm patch until upstream releases it. Parker's standing rule reaffirmed: every carry must be built so it can merge upstream; the carry rides every rebase until upstream takes it, then retires (same lifecycle as the memory-core fixes).
- **Q2: APPROVED.** Target is stable tag `v2026.6.11`. Process confirmed by Parker in his own words: bring the upgrade down, rebase our not-yet-upstreamed patches onto it locally, build, canary, then install. C1 verification of the two memory-core commits still gates it.
- **Q3: STILL OPEN.** Confirm `context-embeddings: enabled false` is deliberate (memory-core + Crystal are the capture paths). If unconfirmed by upgrade time, default: keep off, record as a config invariant.
- **Q4: DECIDED, fix it properly.** Parker does not want to live with the doubling, and BlueBubbles is permanently off the table (April 2026 evidence: Private API dylib crashed Messages.app; the old imsg wrapper caused the Grok mirror loop; the native iMessage channel replaced both). So the doubling gets the correct fix: the sibling-aware write-side `transcriptOnly` refit from the 2026-04-30 ticket, built as an upstream PR. It is its own work item after the upgrade cycle; it does NOT ride the v2026.6.11 carry set unless Parker wants it live before upstream merges.
- **Q6: DECIDED 2026-07-05 = (b).** Rotate the gateway token and move it to `OPENCLAW_GATEWAY_TOKEN`; untrack + ignore the secret files going forward; AND re-auth the OpenAI/Codex OAuth session so the historical `auth-state.json` material is dead. NOT (c): dot-openclaw is org-private, so a `git filter-repo` history rewrite is higher operational risk than value once both live credentials are rotated. Keep filter-repo as a later hard-purge option only if Parker asks. Execution sequence is in gate A0 above.
- **Q5: CONFIRMED, with an added requirement.** Phase 0 runs before the upgrade. Parker's non-negotiable: Memory Crystal access for BOTH Lēsa and Claude Code stays intact throughout; nothing may be lost. Crystal (`~/.ldm/memory/crystal.db`) is outside the upgrade's blast radius (only the native `~/.openclaw/memory/main.sqlite` is archived/migrated). To make that verifiable, the CRYSTAL PROTECTION GATES are added to sections 3, 5, and 9: verified `crystal.db` backup + `crystal_search` round-trip from both Lēsa (gateway) and Claude Code (MCP), at three checkpoints: before Phase 0, before promotion, after promotion.

## 9. Promotion gates (single checklist)

- `/healthz` 200 and `/readyz` 200 on the live gateway
- All enabled plugins in the ready list (tavily question answered)
- gpt-5.5 turn completes with no accountId 401 and no failover
- Fresh main session responds on iMessage and Bridge
- `crystal_status` chunks > 0, `crystal_search` returns, no embedding errors
- CRYSTAL PROTECTION GATES pass at all three checkpoints (before Phase 0, before promotion, after promotion): verified `crystal.db` backup + `crystal_search` round-trip from both Lēsa (gateway) and Claude Code (MCP)
- No `model_not_found` / cron churn in the log
- `git diff ~/.openclaw` clean after doctor
- Stable gateway PID through a broad-recall exercise (no V8 OOM, no `StatementSync::All`)
- Phase 0 72h window complete and clean (no EMFILE, no heap-OOM) before promotion
- Written rollback current in the runbook's Emergency Rollback section (exact worktree, commit, relink + config-restore + restart commands, post-rollback smoke) BEFORE `npm link` runs
- Upgrade log written to `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/open-claw-upgrade-private/logs/`

## 10. Review record

- **2026-07-05, Codex (kay-mini, gpt-5.5):** structurally sound; four blockers + three should-fixes. All addressed same day: (1) secret-safe snapshot recipe replacing `git add -A` in A1/C1 and UPGRADE-RUNBOOK 1.2/7.1; (2) C0 rewritten with the ordered immutable-copy-before-archive sequence; (3) executable rollback written into the runbook's Emergency Rollback (fork-relink model, c188a36) and gated in C6 + section 9; (4) 72h Phase 0 gate semantics resolved (window overlaps B+C build/canary, blocks promotion). Should-fixes: A3 evidence capture added, C5a made concrete (4-step verification), A5 split into live-mitigation-first then source PR.
- **2026-07-05, Codex re-review (gpt-5.5 high):** prior four blockers confirmed resolved. Two new blockers + one should-fix, all addressed same day: (1) tracked-secret reality: `auth-state.json` tracked + gateway token in the dot-openclaw index/history; runbook gained Phase 1.1a remediation (untrack, rotate, token-to-env, live-file preservation) and this plan gained gate A0 + containment question Q6; (2) token check upgraded from staged-diff grep to index-content `git grep --cached -F`, plus a `git ls-files` tracked-file check; (3) curl token extraction switched to `jq` with env-first fallback. Q6 was decided (b) later the same day.
- **2026-07-06, Codex third review (gpt-5.5 high, reviewer seat):** packet declared coherent; A0 confirmed as the right front gate. Two blockers + three should-fixes, all addressed same day: (1) C7 invariant contradicted Q6 (`gateway.auth.token` present) ... rewritten to the post-A0 env-token model, and the KNOWN-LANDMINES gateway-auth entry updated to match; (2) launchd reload gap ... A0 step 5 and runbook Phase 1.1a now bootout + bootstrap after plist env edits (`kickstart -k` does not reliably re-read plist environment) and verify the loaded env before health checks; (3) re-auth ordering unified to the runbook order (re-auth AFTER the untracking merge + preservation); (4) April compatibility master plan given a 2026-07-06 overlay (target = stable v2026.6.11, verified via npm; umbrella + runbook are the execution layer); (5) this review record's stale "Q6 pending" line fixed. Missing-ticket coverage: format-error billing cooldown and the bash-3.2 pre-commit hook are now thin tickets in this folder (2026-07-06); upstreaming plan track-5 thin tickets remain owed before the umbrella closes. **Remaining before execution: CC review, then the A0 live window.**
