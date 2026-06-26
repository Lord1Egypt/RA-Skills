# Memory Dreaming — Full Protocol

Signal-driven memory consolidation in three phases.

---

## Prerequisites

- `MEMORY.md` exists at workspace root
- `memory/dream-log.md` exists (create an empty file if missing)
- `memory/.dreams/short-term-recall.json` — created automatically by OpenClaw when `memory_search` is used; may not exist on a brand-new agent (see Phase 1 fallback)

---

## Before Starting: Guardian Check (automated runs only)

Read `memory/dream-log.md` to find the last dream timestamp by locating the most recent `## 🌙 Dream #` heading.

**First run** (no Dream entries found): bypass the guardian entirely and proceed to Phase 1.

**Skip condition**: last dream was `< 20 hours ago` AND no new `memory/YYYY-MM-DD*.md` files exist with dates after the last dream.

If skipping: use `exec` to append `<!-- SKIP · YYYY-MM-DD HH:MM · reason -->` to `<WORKSPACE_ROOT>/memory/dream-log.md` and stop. Always use absolute paths — never `~`.

Manual triggers always bypass the guardian.

---

## Phase 1 · Sense — Read Only, No Writes

**Goal**: build a priority list without touching any file.

**Distinguishing file types:**
- **Daily logs**: match `memory/YYYY-MM-DD*.md` (e.g. `2026-04-13.md`, `2026-04-13-clash-fix.md`)
- **L2 topic files**: `memory/<topic>.md` files that do NOT match a date pattern (e.g. `memory/clash-verge.md`, `memory/business.md`)
- **⛔ Not daily logs**: `memory/dreaming/**` (built-in memory-core Dreaming output, 2026.4.15+ separate mode) — do NOT process these as daily logs or L2 files; skip entirely

### 1. Read recall signals

If `memory/.dreams/short-term-recall.json` exists:
- Parse the JSON, extract all entries
- Sort by `totalScore` descending, take top 10
- Note each entry's `path`, `totalScore`, and `queryHashes`
- **High-value threshold**: `totalScore > 0.8` AND `len(queryHashes) >= 2`

If the file does **not** exist (new agent, never used memory_search):
- Skip signal ranking entirely
- Fall back to processing all daily logs since the last dream, ordered newest-first

### 2. Scan recent logs

- List all daily log files (`memory/YYYY-MM-DD*.md`) — **exclude** anything under `memory/dreaming/**` (built-in Dreaming output; not user session notes)
- Determine the last dream date from dream-log.md by finding the most recent `## 🌙 Dream #` heading and reading its timestamp
- **First run** (dream-log.md is empty or has no Dream entries): treat all existing daily logs as candidates; last dream date = epoch (process everything)
- Identify files with date-based names **on or after** the last dream date (use `>=` not `>` — same-day logs must be included)
- If a daily log contains `## Light Sleep` or `## REM Sleep` blocks (built-in Dreaming `inline` mode output, pre-2026.4.15 or opted in), **skip those sections** — they are not user session notes

### 3. Identify L2 update candidates

- Match high-score snippets and recent log content to existing L2 topic files
- Flag L2 files likely needing updates

### 4. Check MEMORY.md size

- If > 8KB → flag for trimming in Phase 3

**Output (held in memory, nothing written)**: ranked recall list, new log list, L2 update list, trim flag.

---

## Phase 1.5 · Plan Quality Gates — Read Only, No Writes

Before touching any memory file, make an explicit consolidation plan and check it against these guards:

### 1. Topic identity guard

Do **not** merge records just because names are similar. Split or preserve separate L2 files when any of these differ materially:

- owner / customer / friend group
- environment or host (IP, domain, machine, OS user, cloud account)
- project lifecycle (legacy vs current, prototype vs production)
- world / database / repo / app ID / claim ID / other durable identifier

If old and new material share a broad label, prefer:

- `memory/<topic-current>.md` for the active project
- `memory/<topic-legacy>.md` for historical material
- `memory/<topic>.md` as a short disambiguation index, if needed

### 2. Lifecycle state guard

Classify every candidate as one of: **active**, **waiting**, **done**, **archived**, **closed**, or **snowed/paused**.

- Closed / archived / snowed projects must not be reintroduced as active TODOs.
- If a daily log says the human closed a line of work, update L2 + MEMORY.md to reduce future resurfacing.
- Historical facts may remain, but phrase them as reference/archive, not action items.

### 3. Secret propagation guard

Never copy secrets from daily logs into L2, MEMORY.md, or dream-log.md. Treat these as sensitive by default:

- API keys, tokens, OAuth strings, cookies, private keys
- passwords, invite/player/server passwords, recovery codes
- signed URLs or URLs containing access tokens
- private SSH keys or full credential-bearing command lines

If a source log contains a suspected live secret, do **not** quote it. Record only: `sensitive value omitted; source file needs manual review` and alert in the final response / dream summary.

### 4. Write plan

List the exact files you expect to touch. Phase 2 may touch only L2 files plus backups under `<WORKSPACE_ROOT>/.backup/memory-dreams/`. Phase 3 may touch only `MEMORY.md`, backups under `<WORKSPACE_ROOT>/.backup/memory-dreams/`, and `memory/dream-log.md`.

If the plan requires editing daily logs, system config, or files outside the workspace, stop and ask the human for explicit approval.

---

## Phase 2 · Consolidate — Write L2 Files Only

Process the priority list from Phase 1. **Do not modify MEMORY.md, dream-log.md, or any daily log file in this phase.**

### 0. Back up touched L2 files first

Before modifying an existing L2 file, copy it to:

`<WORKSPACE_ROOT>/.backup/memory-dreams/YYYYMMDD-HHMM/<relative-path-from-workspace-root>.bak`

Example: `memory/clash-verge.md` → `.backup/memory-dreams/20260426-1100/memory/clash-verge.md.bak`.

Keep dream backups **outside `memory/`** and use a non-`.md` final suffix (`.bak`) so memory indexing does not recall stale states or old TODOs from backups.

Create parent directories as needed. If backup creation fails, stop before writing.

For a newly created L2 file, no pre-existing backup is required; include it in the dream-log as `created`.

### High-score recall entries → L2 promotion

- If a snippet's knowledge is not yet in any L2 file: add it to the appropriate topic file
- If it updates an existing L2 entry: revise that entry

### Recent log entries → L2 extraction

- Read relevant new daily logs
- Extract decisions, config changes, resolved issues, new knowledge
- Write or update the appropriate `memory/<topic>.md`
- If no matching L2 file exists for a topic, create one (e.g. `memory/network-setup.md`)

### Relative time correction (conservative)

- Only correct clear expired expressions: "today"/"this week" in L2 files → absolute dates
- Do not guess at vague expressions

### L2 write quality rules

- Prefer small, source-grounded edits over broad rewrites.
- Keep active and legacy material clearly separated; add a one-line pointer instead of duplicating long history.
- Do not add TODOs unless the source explicitly implies continuing action.
- Preserve security posture: write `password not stored`, `token omitted`, or `credential managed in env` instead of values.
- If an `edit` attempt fails twice for the same block, stop trying that block; use a safer whole-file rewrite only after re-reading the file, or leave a blocker in the final summary.

---

## Phase 3 · Settle — Write Index + Diary

### 1. Back up MEMORY.md

Copy current MEMORY.md content → `<WORKSPACE_ROOT>/.backup/memory-dreams/YYYYMMDD-HHMM/MEMORY.md.bak`.

**⚠️ Path guidance**: Always use absolute paths derived from the workspace root (e.g. `/path/to/workspace/MEMORY.md`). Never use `~`-prefixed paths in tool calls — isolated sessions may not resolve them. Use the workspace root passed in the task message.

### 2. Rewrite/trim MEMORY.md

- Target: ≤ 8KB (hard cap; note in dream-log if approaching 10KB — manual cleanup may be needed)
- Update project states from Phase 2 findings
- Sync TODO states: mark completed ✅ items as done, add newly discovered todos
- Preserve lifecycle state: closed / archived / snowed items belong in archive/reference wording, not active sections
- Each section: one-line status + 2–4 bullets + L2 pointer (a reference to the relevant L2 file, e.g. `**Details**: memory/clash-verge.md`)
- Move fully completed/archived projects to a short footer section

### 3. Determine dream number

Count the number of `## 🌙 Dream #` lines in dream-log.md. The new entry is N+1.

### 4. Append to dream-log.md (Markdown — not JSON)

**⚠️ Tool guidance**: Use `exec` with a heredoc to append — **never** use the `edit` tool for appending (it requires exact text replacement and will fail on append). Replace `<WORKSPACE_ROOT>` with the absolute path from the task message.

```bash
cat >> <WORKSPACE_ROOT>/memory/dream-log.md << 'DREAM_EOF'

## 🌙 Dream #<NUMBER> · YYYY-MM-DD HH:MM

**Trigger**: <auto|manual>
**Duration**: ~<MINS> minutes

### Signal summary
- Top recall score: <SCORE> (memory/<path>.md)
- New logs since last dream: <LOG_COUNT> files

### What changed
- Updated L2: <filename> — <one-line description>
- Synced <TODO_COUNT> TODO items
- MEMORY.md: <BEFORE>KB → <AFTER>KB

### Note
(One honest sentence about what was found or how it felt)
DREAM_EOF
```

### 5. Trim dream-log.md

If total `## 🌙 Dream #` entries exceed 30, delete the oldest entry.
Boundary rule: delete from the start of the oldest `## 🌙 Dream #` heading up to (but not including) the start of the next `## 🌙 Dream #` heading. Do not use `---` as a boundary — it may appear inside dream content.

### 6. Post-write audit

Run a small verification pass before finalizing:

- `MEMORY.md` is ≤ 8KB, or the final summary clearly says it is over target
- `memory/dream-log.md` remains Markdown and has no malformed duplicate heading for the new dream
- touched L2 files still separate current vs legacy/archived material correctly
- touched files contain no obvious credential-bearing values

This is a **lightweight sanity check**, not a full DLP or exhaustive secret scanner. It catches common high-signal credential patterns, but the secret propagation guard still relies on careful review and redaction.

Use filename-only scans where possible so secrets are not echoed into chat/logs, for example:

```bash
grep -IlrE '(github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|[0-9]{8,12}:AA[A-Za-z0-9_-]{30,}|mfa\.[A-Za-z0-9_-]{20,}|-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----)' <TOUCHED_FILES>
```

This skill also includes a helper script for the common checks:

```bash
<SKILL_DIR>/references/dream-audit.sh <WORKSPACE_ROOT> [touched-file ...]
```

Pass relative or absolute paths for touched files. The helper reports suspected secret filenames only; it does not print matched values. It is intentionally conservative and lightweight, not a replacement for a dedicated secret-scanning/DLP tool.

If a possible secret is found after writing, restore from the relevant backup where possible, then report the file path without quoting the secret.

---

## Safety Rules

| Rule | Detail |
|------|--------|
| Guardian runs before Phase 1 | Skip condition check; skip writes only to dream-log.md |
| Phase 1 is read-only | Error in Sense = no files touched |
| Never archive daily logs | Moving `YYYY-MM-DD*.md` breaks memory_search indexing |
| Always back up before rewriting | `<WORKSPACE_ROOT>/.backup/memory-dreams/YYYYMMDD-HHMM/MEMORY.md.bak` before touching MEMORY.md |
| dream-log.md = Markdown | Append text; never parse or write as JSON |
| L2 files are permanent | Never delete or archive `memory/<topic>.md` files |
| Phase 2 = L2 only | MEMORY.md changes happen in Phase 3, not Phase 2 |
| Backup before L2 edits | Existing L2 files get timestamped backups in `<WORKSPACE_ROOT>/.backup/memory-dreams/` before modification |
| No secret propagation | Never promote credentials from logs; redact/omit and alert instead |
| Lifecycle is sticky | Closed/archived/snowed items stay non-active unless the human explicitly reopens them |

---

## Scoring Reference

`totalScore` in `short-term-recall.json` is a composite of:

| Signal | Weight | Meaning |
|--------|--------|---------|
| Relevance | 0.30 | Search match quality |
| Frequency | 0.24 | Times returned |
| Query diversity | 0.15 | Distinct queries |
| Recency | 0.15 | Time-decayed freshness |
| Consolidation | 0.10 | Multi-day recurrence |
| Conceptual richness | 0.06 | Concept-tag density |

Entries with `totalScore > 1.0` have been recalled multiple times across different queries — strong long-term candidates.
