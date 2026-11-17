---
name: rabbit-claude-md
description: Audit, tighten, and restructure CLAUDE.md and AGENTS.md memory files so the root file stays a short "where am I" plus rules instead of a changelog. Use when the user asks to audit, improve, clean up, shrink, or split a CLAUDE.md or AGENTS.md, says their memory file is too long, stale, or being ignored, wants gotchas moved to docs or per-module memory files, or mentions CLAUDE.md / AGENTS.md maintenance or project memory. Reports named failure modes with evidence and a per-item disposition plan before touching anything, and holds the prose to the active voice profile.
license: MIT-0
homepage: https://github.com/whit3rabbit/rabbit-writes
metadata: {"version": "0.5.0", "openclaw": {"requires": {"bins": ["python3"]}, "envVars": [{"name": "RABBIT_MODEL_API_KEY", "required": false, "description": "API key for a remote --apply-model endpoint. Read only when scan.py runs with --apply-model. Never logged or persisted."}, {"name": "RABBIT_MODEL_BASE_URL", "required": false, "description": "Base URL of an OpenAI-compatible model endpoint. Read only when scan.py runs with --apply-model. There is no default endpoint and nothing is contacted without one."}, {"name": "RABBIT_MODEL_NAME", "required": false, "description": "Model name for --apply-model. Read only when scan.py runs with --apply-model. Falls back to local when unset."}]}}
---

# CLAUDE.md and AGENTS.md improvement

Audit and improve the memory files AI agent harnesses (Claude Code, OpenAI Codex, etc.) load at the start of every session. The root memory file (`CLAUDE.md` or `AGENTS.md`) is a map plus rules: where am I, what runs this project, which conventions differ from defaults, which mistakes have actually happened. It is not a changelog and not a log of the codebase.

The levers, in order of payoff: shorten bullets, combine overlapping ones, audit each line against the removal test, and separate by altitude, with deep context in `.claude/docs/`, module facts in a memory file inside that module, occasional workflows in a command or skill, and open work in `TODO.md`. The repository's own `docs/` is the project's documentation and stays out of this by default: agent context filed there litters the codebase. A memory file over roughly 40,000 characters, the ceiling commonly recommended for one, should be broken down rather than trimmed.

No grades and no scores. Findings are named failure modes with evidence, and every piece of content gets one of eight dispositions: keep, tighten, merge, move-to-docs, move-to-module, move-to-skill, move-to-todo, or delete. `references/criteria.md` defines both vocabularies.

**Paths.** `{baseDir}` below expands to this skill's own directory, the one holding this file. On a host that leaves the placeholder literal, resolve each path relative to that directory.

## Modes

| Mode | Trigger | Deliver |
|---|---|---|
| **audit** | "audit my CLAUDE.md", "check AGENTS.md", "is this any good", open-ended ask | Findings plus a disposition table, no edits |
| **improve** | "fix it", "tighten it", "update it" | The audit, then targeted diffs applied after approval |
| **restructure** | The file is oversized or mixed-altitude, or "split this up" | The audit, then a move plan: new `.claude/docs/` files, nested memory files, commands or skills, a `TODO.md`, and link-backs, applied after approval |

Default to **audit**. Improve and restructure both pass through the audit report and the approval gate first, never straight to edits.

## What earns a line

The tie-breaker for every line is the removal test: would deleting it cause the agent to make mistakes? Commands an agent cannot guess, conventions that differ from defaults, real gotchas, and environment quirks pass. Anything derivable from reading the code, generic engineering advice, session narratives, verification instructions the model already performs, goals and roadmaps, and a rule already enforced by a hook or a lint config do not. `references/criteria.md` carries the full include and exclude table, the failure-mode catalog with examples, and the disposition tests. Emphasis is a budget: if one instruction keeps getting skipped, emphasize that line alone.

An `@path` import loads its target into every session, and a plain markdown link loads when followed. Default to the link, import only what must always be in context.

## Voice: whose memory file is this

A memory file is prose somebody maintains, so its sentences follow the active voice profile the way any other document in the plugin does. `scripts/claude_check.py` resolves the profile automatically: a `.rabbit-voice` file beside the document or above the working directory wins, then `{baseDir}/voices/ACTIVE`, then nothing. With no profile it enforces no voice rules and says so. Never enforce the example profile on a stranger's file, and never invent a register to fill the gap: with no profile, match the file's existing prose.

Voice governs sentences, never content. No profile authorizes keeping a dead command or a changelog entry, and the disposition plan outranks any style consideration. `--no-voice` turns off the profile only: structure, fingerprints, safety, and craft still run.

## Workflow

1. **Discover.** Run the checker over the repository root:

   ```bash
   python3 {baseDir}/scripts/claude_check.py .
   ```

   Discovery sweeps both memory-file families together: Claude Code spellings (`CLAUDE.md`, `CLAUDE.local.md`, `.claude.md`, `.claude.local.md`) and `AGENTS.md` spellings (`AGENTS.md`, `AGENTS.override.md`, `.agents.md`) are all audited in one run. A repository worked by both harnesses often carries real content in both, and auditing only one family would hide the other file entirely.

   **Symlinking for Claude Code:** If the repository uses `AGENTS.md` without a `CLAUDE.md` companion and the team uses Claude Code, offer to symlink:
   ```bash
   ln -s AGENTS.md CLAUDE.md
   ```
   This allows Claude Code to read the existing `AGENTS.md` guidance without duplicating content. When either name is already a symlink to the other, the checker states it at the top of that file's report, treats the pair as one file, and never counts the shared lines as duplicates.

   When a same-directory `CLAUDE.md` and `AGENTS.md` are two real files (not a symlink) that share most of their substantial content, `claudemd-dual-harness` fires on both: two files edited by hand drift, and a symlink is probably what is wanted instead. `references/restructure.md` has the merge steps.

   `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` are out of scope unless the user names them, and even then they are read for advice, never edited unprompted. Pass `--global` to fold them into the duplicate check (read-only) when a rule here might already live in the user's global memory. Local override files (`CLAUDE.local.md`, `AGENTS.override.md`) are personal: audit them when asked, and never propose moving shared facts into one.

2. **Read the mechanical findings.** The `claudemd-*` ids in the structure band are this skill's: oversize (by line count and, independently, by raw character count against the ~40,000-character budget commonly recommended for a memory file), a missing one-line description under the title, bullet length, emphasis budget, dead fenced paths, dead slash-command references, unresolved imports, the effective size an `@import` pulls in beyond what the file's own size band would catch, duplicate lines across files, a same-directory CLAUDE.md/AGENTS.md pair that should be a symlink, changelog phrasing, forward-looking session state (TODO markers, roadmap and in-progress phrasing), over-verification instructions the model already performs unprompted, and links into a `.claude/docs` that `.gitignore` hides from anyone cloning the repository. For the root memory file only, three more facts land as notes, not findings. Unmentioned top-level directories, what harness config exists (`.claude/settings.json`, `.mcp.json`, `.claude/commands/`, `.claude/agents/`), and how long ago the file last changed against the repository's own commit activity. The other bands come from the `rabbit-writes` engine at register `docs`: `safety` (concealed or agent-directed text), `voice`, `fingerprint`, and `craft`. The `ste-` ids inside craft are readability caps, described in `{baseDir}/references/ste.md`, and `--no-ste` silences them. Craft's judgment half is `{baseDir}/references/craft.md`. Thresholds live in the script's `LIMITS` dict and each finding quotes the limit in force, so the report is the reference.

3. **Do the judgment pass.** The half the script cannot do, over every line: is it derivable from the code, is it at the wrong altitude, is it a session log entry, does it survive the removal test, is it still true. `references/criteria.md` names each failure mode. A `claudemd-changelog-drift` finding is evidence for this pass, never a verdict: a line can narrate history and still carry a standing rule worth keeping in rewritten form.

4. **Report before any edit.** Two parts, always in this order. First the findings: file, line, quoted text, the failure mode by name, and the measured number for mechanical ones. Then the disposition table: one row per finding or content block, the disposition, and for moves the proposed target path. Tighten and merge rows show the diff or a one-line sketch of it. No scores anywhere.

5. **Gate on approval.** Ask which dispositions to apply. Nothing is written before a yes, and approval of one run does not carry to the next.

6. **Apply.** Tighten, merge, and delete as targeted edits that preserve everything the user did not approve changing. Execute moves by `references/restructure.md`: move whole then tighten at the target, delete the source copy in the same change, leave a one-line link back, and never move a safety-critical rule out of an always-loaded file.

7. **Verify and report.** Re-run the checker on every touched file. Scan any file that received moved content at register `docs`, and confirm moved commands still resolve. Report before-and-after non-blank line and character counts per file, plus the move map. Real findings that remain are reported, not suppressed.

### Script CLI Arguments Reference

#### `claude_check.py`
`python3 {baseDir}/scripts/claude_check.py <path> [options]`
- `path`: (REQUIRED, file or directory path) A CLAUDE.md or AGENTS.md file, or a directory to sweep for memory files.
- `--json`: (OPTIONAL, boolean flag) Machine-readable output: per-file findings, stats, counts, and the `limits` in force.
- `--no-voice`: (OPTIONAL, boolean flag) Apply no voice profile. Structure, fingerprints, safety, and craft are still checked.
- `--voice-rules`: (OPTIONAL, file path) A voice's `<name>.rules.json`. Overrides `.rabbit-voice` and `ACTIVE`, and exits 2 if unreadable.
- `--no-ste`: (OPTIONAL, boolean flag) Disable the STE readability caps.
- `--repo-root`: (OPTIONAL, directory path) Override the repository root used by the dead-path and duplicate checks. Default: nearest ancestor holding `.git`.
- `--global`: (OPTIONAL, boolean flag) Fold `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` into the duplicate check, read-only.
- `--check`: (OPTIONAL, boolean flag) Exit 1 if any unsuppressed P0 finding is present.

No `claudemd-*` finding is ever P0, so `--check` blocks only on the engine's safety band. A single-file run still reads sibling memory files for the duplicate check. With no `.git` root above the target, the dead-path and duplicate checks stand down with a note.

## Reference files

| File | When |
|---|---|
| `scripts/claude_check.py` | Every audit. The mechanical findings, the inventory, and the engine bands in one pass |
| `references/criteria.md` | The judgment pass, and any time a disposition is in doubt. Failure modes, the include and exclude table, the eight disposition tests |
| `references/templates.md` | Deciding what a healthy root, module, or monorepo file holds, and which sections a repo does not need |
| `references/restructure.md` | Executing move-to-docs and move-to-module: targets, link-backs, the import exception, verification |
