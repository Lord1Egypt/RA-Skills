---
name: token-safety-checker
description: Find and fix leaked API keys, tokens and passwords in your AI agent's config, long/short-term memory and session transcripts (OpenClaw + Claude Code). Use when the user asks to check token or secret safety, scan for leaked credentials, audit agent memory, MEMORY.md, CLAUDE.md or chat history for secrets, move plaintext tokens in openclaw.json to env vars, or stop secrets from being written into memory. Also use after editing openclaw.json or when setting up a new OpenClaw instance. Secret values are never printed.
license: MIT
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/safeclaw.py scan *), Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/safeclaw.py memory *), Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/safeclaw.py verify *)
metadata: {"author": "maoisdamao", "version": "3.0.2", "homepage": "https://github.com/maoisdamao/token-safety-checker", "openclaw": {"emoji": "🔐", "homepage": "https://github.com/maoisdamao/token-safety-checker", "requires": {"bins": ["python3"]}}}
---

# Token Safety Checker 🔐 (tightlip)

Find leaked secrets in agent **config**, **long-term memory**, **short-term memory** and **transcripts**,
migrate config secrets to env vars, and install a guard that stops new leaks.
Everything runs locally with the Python standard library. No network calls.

**Script:** `scripts/safeclaw.py` inside this skill's folder.
Skill folder — OpenClaw: `{baseDir}` · Claude Code: `${CLAUDE_SKILL_DIR}` (use whichever is an absolute path).
Below, `SC` means `python3 <skill folder>/scripts/safeclaw.py`.

## Hard rules (secret hygiene)

1. Never `cat`, `grep`, `head` or otherwise open a file the scanner flagged, and never echo a secret.
   Doing so copies the secret into this conversation's transcript — a new leak.
2. Only show the user what the script prints: paths, line numbers, detector names, lengths,
   `sha256:` fingerprints. These are safe. The script never prints secret values.
3. Never pass secret values on the command line. `migrate` reads them from disk itself.
4. Ask for explicit confirmation before `migrate` or `install-guard` (they change files).

## Pick the workflow

| User asks about… | Run |
|---|---|
| "check token safety", openclaw.json, OpenClaw setup | **A. Config** (OpenClaw only) |
| memory, MEMORY.md, CLAUDE.md, chat history, transcripts, "did I leak a key?" | **B. Memory** |
| "stop this from happening again", prevention | **C. Guard** |
| full audit | A + B (`SC scan --memory`), then offer C |

On Claude Code without OpenClaw, skip A — there is no openclaw.json.

## A. Config secrets (OpenClaw `openclaw.json`)

1. **Scan**: `SC scan` (add `--deep` to also check git history of the config).
   Exit 0 = clean → report and stop. Exit 1 = findings. Exit 2 = no config found.
   Output: `findings[]` with `path`, `env_var`, `length`, `risk` (🔴 HIGH / 🟡 MEDIUM / 🟢 LOW), `fingerprint`.
   `checks.file_permissions` (should be 600) and `checks.format` (JSON5 configs can be scanned, not migrated).
2. **Confirm**: show a table `path | env_var | risk`. Let the user rename env vars. Do not proceed without a yes.
3. **Dry run**: `SC migrate --findings '<findings JSON from step 1>' --dry-run` and show the plan.
4. **Migrate**: `SC migrate --findings '<findings JSON>'`
   It re-scans from disk, writes a timestamped backup created with mode 600 (`openclaw.json.bak-<time>`),
   appends `export` lines to a **private secrets file** (`~/.openclaw/tightlip.env`, mode 600 before any
   value is written; exact-name dedupe; refuses if a var exists with a different value), adds one line to the
   shell profile that loads that file (no secret values in the profile; `--no-profile` to skip, `--profile`
   / `--secrets-file` to choose paths), replaces values with `{"source":"env","provider":"default","id":"VAR"}`
   and runs the read-only `verify`.
5. **Reload**: shell-launched gateway → `source ~/.openclaw/tightlip.env` then `openclaw gateway restart`.
   systemd → put the vars in `EnvironmentFile=`. Docker → `-e` / `environment:`.
6. **Verify**: `SC verify` (exit 0 = clean). `SC verify --clean-backup` deletes backups once rollback is not needed.
7. **Rollback**: `SC migrate --restore` (newest backup), `SC migrate --list-backups`,
   `SC migrate --restore --backup <file>`.

## B. Memory + transcript secrets (OpenClaw and Claude Code)

`SC memory` — read-only. Auto-detects `~/.openclaw` and `~/.claude`.
Options: `--platform openclaw|claude|all`, `--project <dir>` (default: cwd, for CLAUDE.md / .claude/rules),
`--no-transcripts` (memory files only — faster), `--claude-dir`, `--openclaw-dir`.

What it scans:

| Scope | OpenClaw | Claude Code |
|---|---|---|
| `long_term` | workspace `MEMORY.md`, `USER.md`, `DREAMS.md`, `SOUL.md`, `AGENTS.md`, `TOOLS.md`…, `memory/imports/` | `~/.claude/CLAUDE.md`, `~/.claude/rules/`, auto memory `~/.claude/projects/*/memory/`, project `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/`, `AGENTS.md` |
| `short_term` | daily notes `memory/YYYY-MM-DD*.md` (written by the pre-compaction memory flush) | `~/.claude/history.jsonl` (prompt history) |
| `transcript` | `agents/*/sessions/*.jsonl`, `agents/*/agent/*.sqlite` | `~/.claude/projects/*/*.jsonl`, tool results |
| `log` | `logs/*.jsonl` (e.g. `config-audit.jsonl`, which recorded `openclaw config set` arguments up to OpenClaw 2026.6) | — |

Output `memory.secrets[]` — one entry per unique secret: `detector`, `risk`, `fingerprint`, `length`,
`occurrences`, `scopes`, `locations[]` (`file`, `line`; sqlite rows show `table:rowid=N`), `live_match`
(set when it equals a secret currently used in openclaw.json or a SecretRef env var — rotate these first), `rotate`.

Report to the user:
1. Summary: unique secrets, how many are HIGH, how many are live.
2. Table: `risk | detector | fingerprint | ×occurrences | scopes | first location`.
3. **Rotation is mandatory.** Anything in memory or a transcript has already been sent to a model provider;
   deleting the file does not un-send it. Use each entry's `rotate` hint.
4. Cleanup: the user removes the lines by hand (redaction is planned for a later release). Claude Code
   transcripts can also be deleted per session file. Do not open the files yourself.
5. Offer workflow C so it does not happen again.

## C. Guard — stop new leaks

`SC install-guard --platform claude|openclaw|all` — the platform must be named explicitly; confirm it with the
user first, because this installs a persistent hook.

- **Claude Code**: adds a `PreToolUse` hook (`Write|Edit|MultiEdit|NotebookEdit`) to `~/.claude/settings.json`
  that denies writing a detected secret into memory / instruction files (CLAUDE.md, auto memory,
  `.claude/rules`, MEMORY.md, …). `--scope all` guards every file write. Existing settings and hooks are kept,
  a settings backup is written, and the hook script is copied to `~/.claude/hooks/token-safety-guard.py`.
  New sessions pick it up.
- **OpenClaw**: adds a git `pre-commit` hook to git-backed workspaces that blocks committing secrets.
  An existing non-guard pre-commit hook is never overwritten (manual instructions are printed instead).

Remove with `SC uninstall-guard --platform claude|openclaw|all`.

## SecretRef format (OpenClaw)

```json
{ "source": "env",  "provider": "default", "id": "MY_ENV_VAR" }
{ "source": "file", "provider": "default", "id": "/path/to/token-file" }
{ "source": "exec", "provider": "default", "id": "command --prints --secret" }
```

`env` suits most setups; prefer `file` (chmod 600) or `exec` (password manager) for higher security.
