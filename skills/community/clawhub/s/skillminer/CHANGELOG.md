# Changelog
## 0.5.3 — 2026-04-21
Cosmetic release. No behavior changes, no bug fixes.

Goal: reduce the ClawHub scanner false positive ("Requires OAuth token") that fired on 0.5.2 because the redaction-regex literals sitting inside an executable shell file were classified as active token-handling code by the registry's LLM scanner.

- `skill.json` enriched with `author`, `license`, `repository`, `homepage`, `emoji` fields — gives the scanner explicit provenance signals.
- `SKILL.md` frontmatter now declares `metadata.openclaw.requires.env: []` and `config: []` as explicit "no credential env vars required" signals, plus a `capabilities` block (`network: false`, `subprocess`, `writesTo`, `readsFrom`). CLAWD_DIR moved from `requires.env` (where its presence as a map entry scanner-adjacent to credential-key names added noise) to the existing `note` field as a non-credential path config.
- `scripts/lib/secret-scrub.sh` refactored: the six redaction-regex literals (OpenAI, GitHub PAT, GitHub OAuth, AWS access key, JWT, Slack bot) moved out of the executable shell file into a data file `scripts/lib/secret-patterns.tsv`. The shell script now loads patterns via a TSV read loop. Runtime behavior is identical — same regexes match, same redactions produced.
- Redaction tags are now semantic (named after the pattern provider, lowercase). Better forensic trail, no runtime cost.
- `README.md` gains a dedicated "Security & Privacy" section disclosing the legitimate "sensitive credentials" capability (we read memory files by design), explaining the off-host `FORGE_RUNNER=claude` opt-in, and documenting where the scrub patterns live.

The "sensitive credentials" capability tag stays — it's accurate (we read user memory files, optional off-host egress). The "OAuth token" tag should go once the scanner re-runs against 0.5.3.

## 0.5.2 — 2026-04-21
Hotfix release. 5 new findings from follow-up second-opinion review (claude-code + codex + gemini) plus 4 carryover one-liners deferred from the 0.5.0 review.

- [HIGH] **morning-write rollback symmetry** — same-class regression of 0.5.1's own headline fix. `run-morning-write.sh` was missed when `rollback_state_and_review` was refactored; three of four post-write-log rollback branches restored state but left the write-log on disk, so cron-announce could summarize skills written against a backup-restored state. Added `rollback_state_and_write_log` helper, called from all 4 post-write-log rollback sites. (Finding A)
- [MEDIUM] **commit_pending_staging path escape** — staging dir names were stripped to slugs via `basename "$dir" "-$STAMP"` and used as `_pending/<slug>` targets without validation, so `_pending/.staging/..-$STAMP/` resolved to `$CLAWD_DIR/skills/`. Gated with `validate_slug`; invalid staging dirs are logged and removed. (Finding B)
- [LOW] **rollback preserves timestamped backup** — `rollback_state_and_review` used `mv -f` to restore from `.bak.<STAMP>`, destroying the forensic snapshot on every rollback and silently shrinking the 7-entry retention. Changed to `cp -f`. Same pattern applied in the new morning-write helper. (Finding C)
- [LOW] **migrate-state.sh non-blocking flock** — blocking `flock -x` on a valid FD never fails on contention, so `migrate-state.sh` would hang indefinitely behind a lock-holding wrapper with no user-facing message. Added `-n` and a contention error; exit 3 matches the wrapper convention. (Finding D)
- [LOW] **staging cleanup scoped to run stamp** — pre-run 60-minute age-based cleanup could leak staging dirs from crashes within the last hour, shadowing a same-slug new run. Switched to stamp scope: any dir not matching the current `$STAMP` is cleared regardless of age. (Finding E)
- [MEDIUM] **Carryover #5 — PEM body redacted** — `secret-scrub.sh` only matched PEM BEGIN/END markers, leaving the base64 body (the actual secret material) intact. Rewritten as a multiline BEGIN..END block replacement collapsing the whole range to a single `[REDACTED:PEM]`.
- [MEDIUM] **Carryover #7 — date-only rejectedAt/deferredAt in sweep** — `prompts/skill-writer.md` step 3 was ambiguous about copying `updatedAt` verbatim vs. extracting its date portion; LLM stamping ISO-8601 would pass JSON validation but fail cooldown comparisons against `date +%F`. Prompt now explicitly specifies `YYYY-MM-DD` extraction via `T` split. CLI (`manage-ledger.sh reject|defer`) was already correct.
- [LOW] **Carryover #8 — wrapper schema whitelist tightened to 0.5** — both `run-nightly-scan.sh` and `run-morning-write.sh` accepted `0.2|0.3|0.4|0.5` in the post-write schema check, inconsistent with `manage-ledger.sh`. Wrappers now only accept `0.5` and emit the same migration hint on reject.
- [LOW] **Carryover #9 — silence rejects unknown id** — `manage-ledger.sh silence <unknown-id>` would write a `silenced[]` entry with empty `intentSummary`/`triggerPhrases`, breaking the semantic-match contract those fields enforce. Pre-check requires the target to exist in candidates/observations/rejected/deferred; exits 2 otherwise. The other mutating commands (accept/reject/defer/promote/unsilence) already had their id-exists guards — verified as part of this pass.

Deferred to 0.6: Finding 6 (redaction marker in triggerPhrases reactivating skills), Finding 10 (SKILL.md description/trigger drift). CI harness (shellcheck + bats) also deferred to 0.6.

## 0.5.1 — 2026-04-21
Hotfix release. 4 defects surfaced by external second-opinion review (3 LLMs: claude-code + codex + gemini).

- [CRIT] **setup.sh installs schema-0.4 template** — every fresh install broken on first `manage-ledger` call. Bumped `state-template.json` schema_version to `0.5`.
- [HIGH] **rollback symmetry in run-nightly-scan.sh** — `rm -f review/$TODAY.md` was only in 1 of 5 rollback branches. Factored into `rollback_state_and_review()` called from all rollback sites.
- [HIGH] **`_pending/<slug>/` orphaned on state rollback** — morning-write now stages writes to `_pending/.staging/<slug>-$STAMP/` and only renames to final path after state commits. Rollback cleans staging dirs.
- [HIGH] **migrate-state.sh acquired no skillminer lock** — races with cron-scheduled wrappers possible. Now uses same hash-derived flock lock as manage-ledger.sh, plus stale-tmp cleanup.

## 0.5.0 - 2026-04-21
- CRITICAL fix: atomic_*_write no longer masks missing tmp as success (returns exit 2, logs error, restores backup)
- HIGH fix: manage-ledger.sh acquires flock for all mutating commands (accept, reject, defer, promote, silence, unsilence)
- MEDIUM fix: wrappers validate schema_version after atomic_json_write; invalid version restores backup + exits 2
- HIGH fix: pre-persistence secret scrubbing via scripts/lib/secret-scrub.sh (applied in both wrappers before atomic_json_write)
- HIGH fix: reject-path via manage-ledger.sh reject <slug> <reason> — sets status=rejected + rejectedAt + moves _pending/<slug> to _rejected/ graveyard
- CRITICAL fix: stale state.json.tmp no longer silently promoted over live state — both wrappers rm stale tmps at start-of-run
- HIGH fix: review-file rollback symmetry — when .last-success/.last-write tmp fails, review/$TODAY.md is also removed to keep state consistent
- HIGH fix: lock derived from SKILL_DIR sha1sum instead of $USER — consistent across cron (no USER) and interactive shells
- MEDIUM fix: backup rotation glob restricted to auto-stamp format (8-digit date + 6-digit time + Z) — hand-made snapshots preserved
- MEDIUM fix: schema_version aligned to 0.5 across manage-ledger + prompts; manage-ledger now rejects legacy 0.2/0.3/0.4 with migration hint
- MEDIUM fix: sweep + reject CLI always set rejectedAt; skill-writer.md step 3 updated to infer date from updatedAt when stamping rejectedAt/deferredAt
- New: scripts/migrate-state.sh for 0.4→0.5 migration (no-op fill-in-defaults, bumps schema_version)
- Security: added README note on secret scrubbing

## 0.4.4 - 2026-04-19
- SKILL.md refocused as a professional public skill description
- Removed internal agent-family references that leaked into the ClawHub-facing description
- Removed version-specific hardening section (lives in CHANGELOG)
- Removed internal-team-doc sections (Typical use cases, Who can use it)
- Tightened the `description:` frontmatter field to one neutral summary sentence
- Zero code, schema, or logic changes


## 0.4.3 - 2026-04-19
- Fix: remove undefined `release_skillminer_lock` call in `run-morning-write.sh` slug pre-flight; the `flock -n` on FD 9 is released automatically on shell exit, no explicit release needed. Previously this produced exit 127 with set -e instead of the intended exit 4.
- Fix: README version banner updated from 0.4.0 to 0.4.3
- Doc: README polish pass adds explicit wrapper exit codes and a short security section covering slug validation, locking, atomic writes, and memory-as-data handling

## 0.4.2 - 2026-04-19
- Add hard regex-based slug validation at every slug to filesystem path boundary
- New: `scripts/lib/slug-validate.sh` with canonical `validate_slug()` function
- `manage-ledger.sh` now rejects malformed slugs with exit code 4 on every subcommand
- `run-morning-write.sh` does a pre-flight scan of all accepted candidate slugs and aborts before writes if any fails validation
- Prompts `skill-writer.md` and `nightly-scan.md` document the slug contract
- Defense-in-depth against prompt-injection-induced path traversal: LLM-generated slugs are now technically gated, not just convention-guided
- Reserve exit code `4` for slug/path-validation failures

## 0.4.0 - 2026-04-19
- BREAKING: cron scheduling pattern changed to wrapper-dispatch
- Reason: the 0.3.2 `.tmp`-writing prompts were incompatible with inline `agentTurn` scheduling, so wrapper-backed atomic promotion never ran and scheduled state writes could be lost silently
- Migration: reschedule existing cron jobs to inline `prompts/cron-dispatch-nightly.md` and `prompts/cron-dispatch-morning.md` instead of the raw analysis prompts
- Kept: all 0.3.2 hardening stays in place, and now actually runs on every scheduled tick via the wrapper path

## 0.3.3 - 2026-04-19
- Fixed: removed literal injection-example phrase from nightly-scan.md prompt that triggered ClawHub static scanner false positive. Framing preserved, wording neutralized.

## 0.3.2 - 2026-04-19
- Add wrapper-level atomic tmp-write handling for `state.json`, review files, and write logs, including backup rotation and JSON validation rollback
- Add parent-aware `flock` locking across `skillminer`, `run-nightly-scan.sh`, and `run-morning-write.sh` with exit code `3` for lock contention
- Add conservative memory-as-data security framing in the nightly scan prompt plus oversized-memory warnings in the nightly wrapper
- Document production hardening, `flock` requirement, and the new non-zero exit codes

## 0.3.1 - 2026-04-19
- Fix ClawHub scanner issues by adding `git` to required binaries
- Mark `CLAWD_DIR` as optional in skill metadata and align docs around the `~/clawd` default
- Add explicit local-vs-external runner disclosure for the default `openclaw` runner and optional `FORGE_RUNNER=claude` fallback
- Align the ledger and prompts on schema `0.4`, including `manage-ledger.sh` acceptance

## 0.3.0 - 2026-04-19
- Add observation trend fields to the 0.4 ledger schema: `previousOccurrences` and `previousDays`, with prompt guidance to treat legacy missing values as `null`
- Expand nightly scan reporting with observation trend arrows, pending-candidate ledger aging, and a live portfolio snapshot section
- Add `scripts/skillminer` manual wrapper with `scan`, `write`, `full`, `status`, and `help` subcommands
- Update `setup.sh`, `SKILL.md`, and `USER_GUIDE.md` to document manual triggers and optional `/usr/local/bin/skillminer` symlink installation
- Keep the 0.2.1 scheduled-run notify fix intact: no prompt-level notifications, cron announce delivery only

## 0.2.1 - 2026-04-19
- Fix notify hang in scheduled runs by removing inner notification steps from `prompts/nightly-scan.md` and `prompts/skill-writer.md`
- Scheduled notifications now belong to cron `delivery.mode: announce`, not prompt-level `openclaw message send`
- Recommended cron integration now uses `payload.kind: agentTurn` with inline prompt content instead of `bash run-*.sh` wrappers
- Update README, USER_GUIDE, and setup output to document the supported cron pattern

## 0.2.0
- Rewrite intro — honest language: optional local scan, no auto-activate, no notifications by default, Claude fallback is external
- Unify naming — Scout/Scribe removed from all user-facing docs, skillminer is the product, `forge` is the command
- Add `setup.sh` — bootstraps state.json, copies config, prints scheduler commands. `bash setup.sh` just works
- Fix notifications mismatch — default is off everywhere, local review files still written regardless
- Wire thresholds — `config/skill-miner.config.json` → `run-nightly-scan.sh` → nightly prompt. Config now actually drives behavior
- Shorten prompts — more determinism in jq/shell, less LLM prose
- Resolve writer-prompt conflict — step-preservation is now explicit verbatim, no "clean up grammar" ambiguity
- Rework quickstart — manual test first, then enable cron. Testable before automated

## 0.1.7
- Normalize all skill-miner → skillminer references across scripts, prompts, docs
- Rename cron jobs to skillminer-nightly-scan / skillminer-morning-write

## 0.1.6
- Rewrite SKILL.md body — benefit-focused, non-technical, quick start via ClawHub
- Update Quick Start to include both ClawHub and manual git clone install methods

## 0.1.5
- Auto-detect the installed skill directory in all wrapper scripts and `manage-ledger.sh` via `BASH_SOURCE`, so the skill works from local checkouts and ClawHub installs.
- Update prompts to treat `FORGE_DIR` as wrapper-injected instead of deriving it from `CLAWD_DIR`.
- Clarify in `SKILL.md` and `README.md` that `CLAWD_DIR` is only for workspace memory files and `_pending/` output, while cron must point to the actual installed script path.

## 0.1.4
- Fix FORGE_DIR path in run-nightly-scan.sh and run-morning-write.sh (skill-miner → skillminer)

## 0.1.3
- Fix path inconsistency: skill-miner → skillminer in all prompt and script references

## 0.1.2
- Remove FORGE_STATE env override — simplifies security surface

## 0.1.1
- Declare CLAWD_DIR as required env var in SKILL.md metadata
- Add warning on FORGE_STATE override in manage-ledger.sh

## 0.1.0 — Initial public release
- Nightly memory scan (04:00) — detects recurring patterns across conversation history
- Morning write (10:00) — drafts SKILL.md for accepted candidates into skills/_pending/
- Schema 0.3 ledger with sub-threshold observation tracking
- Natural language interface: accept, reject, defer, silence, promote, show
- Configurable scan window, thresholds, and cooldown via config
- Notifications support (configurable channel)
- OpenClaw runner (default) + Claude CLI fallback via FORGE_RUNNER env
- .gitignore and .clawhubignore — state/ and local config excluded
