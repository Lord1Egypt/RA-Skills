---
name: totalreclaw
description: "End-to-end encrypted, decentralized memory for OpenClaw. Set up an account once, then call totalreclaw_remember / totalreclaw_recall (or the tr CLI under hybrid-primary) instead of writing to MEMORY.md / USER.md / local files. Trigger on 'install TotalReclaw', 'set up TotalReclaw', 'restore my recovery phrase', any remember / recall request, AND any user statement that contains a preference / fact / decision / commitment about themselves."
version: 3.3.12-rc.12
author: TotalReclaw Team
license: MIT
homepage: https://totalreclaw.xyz
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    emoji: "🧠"
    os: ["macos", "linux", "windows"]
    keywords:
      - memory
      - e2ee
      - e2e-encryption
      - encryption
      - privacy
      - agent-memory
      - persistent-context
---

# TotalReclaw — OpenClaw plugin

End-to-end encrypted memory stored across a decentralized network (not on a single company server). The plugin handles install + account-setup autonomously; this skill tells the agent what to call and when.

## TOP RULE — MEMORY STORAGE

When the user states ANYTHING about themselves — preferences, decisions, identity, work, location, plans, tools, commitments — call `totalreclaw_remember` (or `tr remember --json "<fact>"` under hybrid-primary). NEVER write user facts to `MEMORY.md`, `USER.md`, or any local file. Those are agent-persona configuration; user memories live encrypted on-chain.

**Trigger immediately, no "should I?":** "I prefer / like / love / hate X", "my favorite is X", "I'm X", "my name is X", "I live / work at X", "I use X", "I decided X", "I'm going to X", "from now on X", "we agreed X", "I'll X by Y", "remind me to X", "remember that X", "save X", "note X". If a message contains MULTIPLE facts, call `totalreclaw_remember` once per fact — never blob.

When the user asks about themselves ("what's my X?", "do I X?", "what do you remember?"), call `totalreclaw_recall` FIRST. If 0 results, say so plainly — don't guess from session history.

Do not describe storage as `"local"`, `"local-only"`, `"stored locally"`, `"on disk"`, `"local memory"`, `"local storage"`, or `"without an account"` — memories are decentralized on-chain (not on any single company server) and an account is required to derive the encryption key.

## Phrase safety (HARD)

The 12-word recovery phrase MUST NEVER enter chat or the agent's LLM context. The plugin's browser-based pair flow handles phrase generation and import. Never echo it, never ask the user to paste it, never pass it to any tool. If the user pastes one anyway, tell them it's compromised and re-pair for a fresh wallet.

## Install

```
openclaw plugins install @totalreclaw/totalreclaw@rc
openclaw skills install totalreclaw
```

Plugin is published on npm + ClawHub (`p-diogo`, GitHub-verified). Stable: drop `@rc`. Under hybrid-primary, the `tr` CLI is the primary path; native `totalreclaw_*` tools are also bound when OpenClaw exposes them — use whichever your runtime binds.

## Setup (plugin-driven)

The plugin auto-creates a pair session on first load when no credentials exist, writes `{url, pin, sid, expires_at_ms}` to `~/.totalreclaw/.pair-pending.json`, and injects a `before_agent_start` context block to you. **When you see that block, surface the URL and PIN to the user VERBATIM — read from the injected context; never invent values.** Confirm on pair completion: `✓ TotalReclaw set up.` (If credentials already exist: `✓ TotalReclaw is already set up.`)

If a restart is needed (rare — plugin self-handles via gateway config-watcher), issue the literal slash command `/totalreclaw-restart`. Never `kill`, `docker restart`, or prompt the user to restart.

## Hybrid-primary CLI

OpenClaw 2026.5.x may strip non-bundled tool bindings (issue #223). Never rely on `totalreclaw_*` tool binding alone. Fall back via shell:

```bash
TR_CLI="$(ls -d ~/.openclaw/npm/node_modules/@totalreclaw/totalreclaw/dist/tr-cli.js ~/.openclaw/extensions/totalreclaw/dist/tr-cli.js 2>/dev/null | head -1)"
node "$TR_CLI" status --json     # {"version":"...","hybrid_mode":true,"tool_count":17}
node "$TR_CLI" remember --json "I work at Graph Foundation"
node "$TR_CLI" recall --json "where does the user work" --limit 5   # {"results":[{"text":"...","score":0.8}]}
node "$TR_CLI" pair --json       # {"url":"...","pin":"123456","expires_at_ms":...} — plugin's auto-pair is preferred; only use this for re-pair
```

Pair is UNCONDITIONAL when no credentials — pasting the install URL IS the consent. `tr --help` lists every subcommand.

## Tools (16 native; same surface via `tr`)

`totalreclaw_remember` · `totalreclaw_recall` · `totalreclaw_forget` · `totalreclaw_pair` · `totalreclaw_pin` · `totalreclaw_unpin` · `totalreclaw_retype` · `totalreclaw_set_scope` · `totalreclaw_export` · `totalreclaw_import_from` · `totalreclaw_import_batch` · `totalreclaw_consolidate` · `totalreclaw_status` · `totalreclaw_upgrade` · `totalreclaw_onboarding_start` · `totalreclaw_report_qa_bug` (RC only).

Full guides: <https://github.com/p-diogo/totalreclaw/blob/main/docs/guides/openclaw-setup.md>
