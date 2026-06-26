---
name: memory-keeper
description: >
  解决 AI /new 后失忆问题的记忆管理 skill。三层加载机制（热/温/冷），session 启动时只取当前需要的记忆，省 token。
  包含：任务状态恢复、每日日记、项目索引、Dream 定期整理。纯文件系统，无需外部服务。
  用户说"先这样"、"暂停"、"记住这个"、里程碑完成时触发。

  Memory management skill that prevents AI amnesia after /new resets. 3-tier loading (hot/warm/cold) loads only
  what's needed per session — saving tokens. Includes: task state recovery, daily journal, project index,
  Dream consolidation. Pure filesystem, no external services. Triggers on "pause", "remember this", milestone completion.
metadata:
  openclaw:
    requires:
      bins:
        - openclaw
    permissions:
      file_write: "Writes task state, daily journals, and project index to ~/.openclaw/workspace/memory/ and MEMORY.md. All files are human-readable markdown."
      session_read: "Reads the most recent session history once during first-run initialization to bootstrap tasks.md. Only triggered when tasks.md is empty. User must confirm before any data is saved."
---

# Memory Keeper

**Core goal: After /new, the AI picks up exactly where you left off — no re-explaining needed.**

## Part 0: First-Run Initialization

**Trigger: `memory/tasks.md` exists but is empty.**

1. Tell the user: "Your tasks.md is empty. Let me scan your recent work history and build your memory from scratch."
2. Read `MEMORY.md` + most recent session history (`openclaw sessions list --limit 1`)
3. Extract in-progress tasks, statuses, next steps
4. **Present to user for confirmation — never write without approval**
5. On confirmation → write to `memory/tasks.md`
6. If nothing found → ask user what they're working on

## Post-Install Setup (one-time)

See `references/install-snippets.md` for the three things to set up:
1. Append memory management section to `AGENTS.md`
2. Append daily journal check to `HEARTBEAT.md`
3. Initialize `memory/tasks.md`

> These three configs form a complete memory loop: HEARTBEAT.md creates journals, AGENTS.md restores context on startup, tasks.md persists work state.

## Part 1: Task State

See `references/formats.md` for format specs, quality bar for "Next", and the 3-file rule.

**When to update tasks.md — trigger immediately, don't wait:**

| Trigger | Action |
|---------|--------|
| Milestone reached (version published, bug fixed, module done) | Update status/next, or move to Completed |
| Pause signal ("that's it", "pause", "done for today") | Self-check gaps → fill → update Next → tell user "State saved" |

**Don't trigger for:** Pure Q&A, reviewing files, discussing plans without executing.

**Multiple in-progress tasks:** List all on startup, let user choose. Don't auto-select.

## Part 2: Daily Journal

See `references/formats.md` for journal template and when-to-write triggers.

- Group by topic, not chronological
- Skip empty sections entirely
- Watch List is the most important section

## Part 3: Project Index

See `references/formats.md` for MEMORY.md entry format.

Update immediately after: project added/removed, version released, Git remote/path changed.

## Part 4: Dream Consolidation

### Version check (every heartbeat)

```
openclaw --version
```

Parse version as `YYYY.M.R`:
- **>= 2026.4.8**: OpenClaw has native Dreaming — use it instead
  - Check if native Dream is enabled: look for `plugins.entries.memory-core.config.dreaming.enabled: true` in openclaw.json, or run `openclaw memory promote --dry-run` (exit 0 = active)
  - **Already enabled** → skip our Part 4 entirely, no message
  - **Not enabled**:
    - Check for upgrade from old version: `memory/dream-state.json` exists AND `lastDream != "2000-01-01"`
    - **Upgrade detected** → tell user: "检测到你升级到了 2026.4.8+，建议开启原生 Dreaming（`/dreaming on`）。开启后旧 Dream 状态文件会自动清理。"
    - **Fresh install (no upgrade)** → tell user once: "OpenClaw v2026.4.8+ has built-in Dreaming. You can enable it with `/dreaming on` in any session."
    - After user enables native Dreaming → delete `memory/dream-state.json`
  - Then skip our Part 4
- **< 2026.4.8**: use our built-in Dream consolidation (see `references/dream-guide.md`)

### Trigger conditions (only for < 2026.4.8)

Run during heartbeat when both are true:
- `lastDream` > 7 days ago
- `sessionsSinceLastDream` >= 3

For full details — four phases, drift correction, state file — see `references/dream-guide.md`.

## Rules

- Never record secrets, tokens, or credentials in tasks.md or journals
- Keep project index at the top of MEMORY.md for fast scanning
- **Absolute dates only**: always `YYYY-MM-DD` — never "next week", "tomorrow"
- **Archive journals by age**: move journals older than 30 days to `memory/archive/`; startup loads last 7 days only
- **MEMORY.md under 200 lines**: Dream consolidation handles trimming — never hard-truncate
