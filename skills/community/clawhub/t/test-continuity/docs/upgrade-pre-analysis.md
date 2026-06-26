# OpenClaw Upgrade Pre-Analysis

Created: 2026-04-07
Current: v2026.3.24 (host A + host B)
Target: v2026.4.5 (not yet installed)
Status: analysis only, no upgrade executed

---

## 1. Dependency Map

### 1.1 Directory Structure (HIGH impact)

| Dependency | Code Location | Detail |
|-----------|---------------|--------|
| WORKSPACE_DIR | L25 | `SCRIPT_DIR.parents[2]` — assumes skill at `workspace/skills/*/scripts/` |
| sessions.json | L55 | `WORKSPACE_DIR.parent / "agents" / "main" / "sessions" / "sessions.json"` |
| cron/jobs.json | L56 | `WORKSPACE_DIR.parent / "cron" / "jobs.json"` |
| openclaw.json | L58 | `WORKSPACE_DIR.parent / "openclaw.json"` |
| runtime-src | L7949 | `WORKSPACE_DIR.parent / "runtime-src"` — scans `openclaw-v*` dirs |
| TypeScript sources | L7963-65 | `src/auto-reply/reply/get-reply.ts`, `get-reply-run.ts`, `src/channel/send.ts` |

All paths can be overridden via env vars (`PERSONAL_HOOKS_*`), mitigating risk.

### 1.2 Session Architecture (HIGH impact)

| Dependency | Detail |
|-----------|--------|
| Session key tokens | `:heartbeat`, `:direct:`, `:slash:`, `:cron:`, `:run:`, `:subagent:`, `:node-`, `:acp:` |
| `session_role_for_key()` | L7055-7073, classifies session as frontstage/control/unknown by key pattern |
| sessions.json schema | Root dict, key → entry dict with `sessionFile`, `updatedAt`, `lastHeartbeatText`, `lastHeartbeatSentAt` |
| Heartbeat detection | `":heartbeat" in session_key` — bypass all prompt injection |

### 1.3 Adapter Lifecycle Hooks (HIGH impact)

| CLI Command | Called By | Purpose |
|------------|-----------|---------|
| `preagent-sync` | Adapter (before model generation) | Intercept inbound user text, run decision loop |
| `runtime-context` | Adapter (prompt assembly) | Inject pending topics / preferences / schedule / setup into model context |
| `frontstage-guard` | Adapter (before outbound send) | Filter output for frontstage safety |

Adapter integration depends on:
- Anchor markers in TypeScript source (e.g. `"runtime-context"` string in `get-reply-run.ts`)
- JSON stdin/stdout contract (command → JSON output)
- Field names in runtime-context response (10+ prompt fields)

### 1.4 Heartbeat (MEDIUM impact)

| Dependency | Detail |
|-----------|--------|
| `HEARTBEAT_OK` token | Recognized as system token, early-returned from guard |
| `:heartbeat` session bypass | All prompt injection skipped for heartbeat sessions |
| `lastHeartbeatText` / `lastHeartbeatSentAt` | Read from sessions.json for dispatch awareness |
| Heartbeat isolation | Expects `heartbeat.isolatedSession=true` in openclaw.json |

### 1.5 Config Schema (MEDIUM impact)

| Path in openclaw.json | Purpose |
|----------------------|---------|
| `plugins.entries["memory-lancedb-pro"].config.embedding` | Embedding provider credentials (apiKey, model, baseURL) |
| `agents.defaults.heartbeat.*` | Heartbeat interval, isolation, directPolicy |

### 1.6 Outbound / Channel Routing (LOW impact)

| Dependency | Detail |
|-----------|--------|
| `PERSONAL_HOOKS_TARGET_CHANNEL` env var | Render channel selection |
| `PERSONAL_HOOKS_TARGET_TO` env var | Dispatch target |
| Render command output | `target_channel` field in render payload |

All parameterized via env vars — no hardcoded channel assumptions.

### 1.7 Tool / Command Interface (LOW impact)

- 30+ argparse subcommands, all output JSON to stdout
- Adapter parses specific fields from `runtime-context`, `preagent-sync`, `frontstage-guard`
- Other commands (profile-show, setup-check, etc.) are standalone utilities

---

## 2. Upgrade Blockers (evidence-based)

### BLOCKER-1: Plugin config path migration
- **Evidence**: v2026.3.22 changelog — "Plugin SDK surface is `openclaw/plugin-sdk/*`; `openclaw/extension-api` is removed"
- **Impact**: If v2026.4.x moves plugin config out of `plugins.entries`, `load_memory_lancedb_embedding_config()` (L2896) breaks
- **Bucket**: A (shared code reads this path)

### BLOCKER-2: Session key format changes
- **Evidence**: `session_role_for_key()` hardcodes 10+ token patterns
- **Impact**: If v2026.4.x changes session key naming convention, frontstage/control classification breaks → wrong content reaches wrong sessions
- **Bucket**: A (shared code)
- **Note**: No evidence v2026.4.x changes this, but no changelog available locally to confirm

### BLOCKER-3: TypeScript source path changes
- **Evidence**: `_resolve_openclaw_runtime_dir()` and `runtime_anchor_exists()` scan `src/auto-reply/reply/get-reply-run.ts`
- **Impact**: If runtime source reorganized, anchor detection fails → capability_state reports partial/missing
- **Bucket**: A (shared), but graceful degradation (returns "partial" not crash)

### BLOCKER-4: Adapter lifecycle hook invocation
- **Evidence**: Three CLI commands (`preagent-sync`, `runtime-context`, `frontstage-guard`) called by adapter at specific lifecycle points
- **Impact**: If adapter removes/renames these integration points, skill becomes inert
- **Bucket**: B (adapter patches are per-host)
- **Note**: v2026.3.24 added `before_dispatch` hook — may provide alternative integration path

---

## 3. Non-Blockers

| Item | Why not a blocker |
|------|------------------|
| Directory layout | All paths have env var overrides |
| Channel routing | Fully parameterized via env vars |
| Heartbeat timing | Config-driven, not hardcoded |
| Locale / i18n | Self-contained in skill, no OpenClaw dependency |
| Setup guide system | Fully internal, no runtime dependency |
| Dispatch awareness | Reads sessions.json but gracefully handles missing data |
| Node version floor | v2026.3.24 lowered to 22.14+; no skill impact |
| Browser changes | Skill has no browser dependency |
| Auth mode changes | Skill has no auth dependency |

---

## 4. Relevant v2026.3.22-3.24 Changes

| Change | Version | Impact on Skill |
|--------|---------|----------------|
| Plugin SDK overhaul | 3.22 | `openclaw/extension-api` removed — skill doesn't import this, but adapter patches might |
| `before_dispatch` hook | 3.24 | New lifecycle hook — potential alternative to current adapter patches |
| Cron heartbeat prompt suppression | 3.24 | Cron runs no longer read HEARTBEAT.md — aligns with skill's heartbeat isolation |
| Heartbeat direct delivery default change | 3.22→3.24 | Flipped twice — current default is `allow`; skill's heartbeat dispatch assumes this |
| Memory-lancedb proxy fix | 3.24 | Fixes proxy environments; no behavioral change for skill |
| `MEMORY.md` wins over `memory.md` | 3.22 | No impact — skill doesn't use MEMORY.md |

---

## 5. Upgrade Pre-Check Checklist

### Phase 1: Non-destructive (run before upgrade)
- [ ] Download v2026.4.5 changelog and search for BREAKING changes affecting: session key format, heartbeat, plugin config, hooks API
- [ ] Check if `plugins.entries["memory-lancedb-pro"].config.embedding` path still valid in v2026.4.5 config schema
- [ ] Check if `src/auto-reply/reply/get-reply-run.ts` still exists in v2026.4.5 runtime source
- [ ] Check if sessions.json schema unchanged (key format, field names)

### Phase 2: Isolated test (after installing v2026.4.5 alongside existing)
- [ ] `python3 personal_hooks.py init` — store initializes without error
- [ ] `python3 personal_hooks.py setup-check` — returns valid JSON
- [ ] `python3 personal_hooks.py runtime-context --session-key test --user-text "hello" --is-new-session` — returns valid JSON with all prompt fields
- [ ] `python3 personal_hooks.py frontstage-guard --text "測試訊息"` — returns valid JSON
- [ ] `python3 personal_hooks.py preagent-sync --text "測試"` — returns valid JSON
- [ ] `_resolve_openclaw_runtime_dir()` finds v2026.4.5 directory
- [ ] `load_memory_lancedb_embedding_config()` returns valid config or empty dict (not crash)

### Phase 3: Live smoke (after adapter reconnection)
- [ ] Heartbeat still fires (`:heartbeat` session created)
- [ ] `HEARTBEAT_OK` response not blocked
- [ ] `runtime-context` output injected into model prompt (check via test message)
- [ ] `frontstage-guard` still called on outbound messages
- [ ] `preagent-sync` still called on inbound messages
- [ ] Proactive dispatch still works (care_message / followup)
- [ ] Carryover summary persists across `/new`
- [ ] Dispatch awareness prompt appears in direct sessions after cron dispatch
- [ ] Setup prompt appears for unconfigured profile

### Phase 4: Regression (after 24h)
- [ ] No English template rendering (locale resolution correct)
- [ ] No frontstage guard false-positive kills
- [ ] Hook GC runs without error
- [ ] followup_trace.jsonl entries are clean

---

## 6. Recommended Test Order

1. **Phase 1 first** — zero risk, just read changelogs
2. **Phase 2 on staging** — install v2026.4.5 to a separate `runtime-src/openclaw-v2026.4.5/` directory without activating
3. **Phase 3 on one host** — upgrade the simpler host first (fewer hooks)
4. **Phase 4 wait** — 24h observation before upgrading the more complex host

---

## 7. Bucket Classification

| Layer | Bucket | Rationale |
|-------|--------|-----------|
| CLI command interface | A | Shared code, same commands everywhere |
| Session key parsing | A | Shared code in `session_role_for_key()` |
| Plugin config reading | A | Shared code in `load_memory_lancedb_embedding_config()` |
| Adapter patches (TypeScript) | B | Per-host, version-specific runtime patches |
| Manifest / locale config | B | Per-host configuration files |
| openclaw.json heartbeat config | B | Per-host config, not in skill code |
| Persona / SOUL.md | C | Not an upgrade concern |
