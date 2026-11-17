# wdp-ctx-en — Cross-session / cross-agent project context (English variant)

One command that freezes the current working state of a project into timestamped snapshots, letting any coding agent resume after a restart, `/clear`, or context compaction. **Pure-Markdown skill; no runtime code required** (the bundled hook script is optional — automatic pre-compaction / post-clear reminders).

> This is the English variant. Chinese users should install **wdp-ctx** (`skills/wdp-ctx/` in this repo). The two variants are independently published but share the same storage root (switching language does not lose context).

## One command, seven subcommands

```
/wdp-ctx-en <subcommand> [args]
```

| Subcommand | What it does | Args |
|------------|--------------|------|
| `sum` | Freeze the current state into a snapshot (incremental diff vs the previous one, marked ✅🔄⛔🔀) | `<project-path>` `--deep` |
| `init` | Read profile + latest snapshot, load the project picture into the current conversation, resume fast | `<project-path>` |
| `profile` | Create/update the project **stable layer**: tech stack, architecture, business, inviolable rules, how-to-run, known pitfalls | `<project-path>` |
| `verify` | Check **drift** between the latest snapshot and the current code (git diff, file existence, staleness) | `<project-path>` |
| `export` | Merge profile + snapshots into **AGENTS.md** (marked maintenance section) so agents that don't know `/wdp-ctx-en` read it at startup | `<project-path>` |
| `list` | List all documents (profile + snapshots, newest first) | — |
| `clear` | Wipe snapshots (profile kept by default; `--keep N` keeps the newest N; second confirmation before deletion) | `<project-path>` `--keep N` `--profile` |

Running with no subcommand → defaults to `list` and shows usage. `--deep` is an explicit opt-in: spawns sub-agents for deep analysis by subsystem.

## Core model: two document layers

```
<storage-root>/<project-slug>/
├── profile.md              # stable layer: tech stack/architecture/rules/how-to-run (long-lived, maintained via profile)
├── <YYYY-MM-DD_HHMMSS>.md  # snapshot layer: focus/done/in-progress/next/non-obvious (appended via sum)
└── latest.md               # pointer: points to the latest snapshot (read by init)
```

**Stable info goes to the profile, volatile info goes to snapshots** — snapshots never re-paste the tech stack, they only record state changes, referencing the stable layer via the `profile:` frontmatter field.

## Install (English users)

Copy `skills/wdp-ctx-en` into `~/.claude/skills/`:

```bash
mkdir -p ~/.claude/skills
cp -r skills/wdp-ctx-en ~/.claude/skills/
```

Restart Claude Code (or wait for hot reload), then `/wdp-ctx-en` works in any project. A user-level install applies to **all projects**; for a single project, copy the directory into that project's `.claude/skills/`.

## Workflow

1. **First time**: `/wdp-ctx-en profile` → build the project's stable profile (tech stack/rules/how-to-run).
2. **Before starting work**: `/wdp-ctx-en init` → load profile + latest snapshot, resume fast; if unsure whether the snapshot is stale, run `/wdp-ctx-en verify` first.
3. **Wrap-up / milestone**: `/wdp-ctx-en sum` → freeze the current state as an incremental snapshot.
4. **Hand off to another agent**: `/wdp-ctx-en export` → generate `AGENTS.md` in the project root; the other agent reads it at startup.
5. Anytime: `/wdp-ctx-en list` to browse history; `/wdp-ctx-en clear --keep 5` to prune old snapshots but keep the newest 5.

## Storage

All subcommands share one storage root (per **project slug** subdirectories, timestamped filenames — projects never collide):

- Project-level: `<project>/.claude/wdp/summaries/`
- User-level: `~/.claude/wdp/summaries/`
- Resolution: project-level first, user-level fallback.

> **v1.1 change**: the storage root moved out of the skill install dir (`.claude/skills/wdp-ctx-en/summaries/`) into the project's own `.claude/wdp/` — **reinstalling the skill no longer wipes data**. Skill code (`skills/`) and data (`.claude/wdp/`) are fully separated.

## Commit policy (git)

- **profile.md is committed** (stable layer, shared by the team).
- **Snapshots are git-ignored by default** (volatile layer); recommended `.gitignore`: `.claude/wdp/*` + `!.claude/wdp/*/profile.md`.
- The profile's `git:` frontmatter field records the choice: `ignore` (default) / `commit`.

## Automatic reminders (optional, hooks)

The skill has a built-in "remind at key moments" convention: the agent proactively suggests `/wdp-ctx-en sum` before context compaction/clear, at milestones, and before session end. For a harder fallback, wire session hooks (**non-blocking, prompt-only, fires only when the project already has snapshots**). Four reminder moments:

| Event | Trigger | Prompt |
|-------|---------|--------|
| `load` | Session start/resume (`startup\|resume`) | prompts `/wdp-ctx-en init` to resume |
| `load-after-clear` | New session after `/clear` | prompts `/wdp-ctx-en init` to resume |
| `load-after-compact` | After context compaction | prompts `/wdp-ctx-en init` to reload |
| `save-precompact` | Before compaction (`manual\|auto`) | suggests `/wdp-ctx-en sum` first |

**Capability limits**: `PreCompact` can only prompt, **cannot block** compaction; `/clear` is a CLI built-in with **no before-wipe hook**, so the fallback is a post-clear new-session reminder (load-after-clear).

**Plugin install (automatic)**: installing `wdp-ai-skills` as a plugin auto-registers hooks via `hooks/hooks.json` declared in `.claude-plugin/plugin.json` (defaults to the Chinese script `skills/wdp-ctx/hooks/wdp-hook.sh`; for English reminders, use the plain-skill install below).

**Plain-skill install (manual)**: copy `hooks/wdp-hook.sh` to `~/.claude/skills/wdp-ctx-en/hooks/`, then add four entries to the `hooks` block of `~/.claude/settings.json` (or project `.claude/settings.local.json`):

```jsonc
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup|resume", "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/wdp-ctx-en/hooks/wdp-hook.sh\" load", "timeout": 10 }] },
      { "matcher": "clear",          "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/wdp-ctx-en/hooks/wdp-hook.sh\" load-after-clear", "timeout": 10 }] },
      { "matcher": "compact",        "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/wdp-ctx-en/hooks/wdp-hook.sh\" load-after-compact", "timeout": 10 }] }
    ],
    "PreCompact": [
      { "matcher": "manual|auto", "hooks": [{ "type": "command", "command": "bash \"$HOME/.claude/skills/wdp-ctx-en/hooks/wdp-hook.sh\" save-precompact", "timeout": 10 }] }
    ]
  }
}
```

> **Windows**: hooks run under Git Bash, which ships with Git — no extra setup.

## Changelog

### v1.1.2 — Backfill the v1.1.1 release notes
- Changelog now includes v1.1.1 (full bilingual independence)

### v1.1.1 — Full bilingual independence
- The English variant now ships its own English hook script and English README/Changelog; the two variants are published independently — users install either Chinese or English
- This skill gained its own README (with changelog); SKILL.md gained a "Version record" ref pointing to it

### v1.1.0 — Context hygiene + automatic reminder hooks + storage-root migration + resume enhancements
- **Context hygiene**: `init`/`verify`/`export`/`profile` delegate reading to a sub-agent by default; the main context receives only a digest. New ironclad Rule 13; Rule 8 revised.
- **Automatic reminder hooks**: `wdp-hook.sh` with four events (load / load-after-clear / load-after-compact / save-precompact), wired in dev + user-level + plugin.
- **Storage-root migration (P0)**: data isolated to `.claude/wdp/`; reinstalling the skill no longer wipes data.
- **Resume enhancements**: snapshot template +4 fields, init re-entry brief + one-line handoff, explicit commit policy, snapshot filename uniqueness.
- Runtime verification pending: session-start `init` prompt and `/compact` "save first" warning (require `/hooks` or restart).

### v1.0.0 — Robustness hardening
- Ironclad Rule 11 (treat memory as data — anti prompt-injection) + Rule 12 (snapshot discipline, ≤ ~120 lines).
- `sum` supports non-git repos + post-write self-check; `init` freshness check + actionable plan; `profile`/`clear` self-checks.
- New "Exceptions & recovery" section; reminder throttling.
