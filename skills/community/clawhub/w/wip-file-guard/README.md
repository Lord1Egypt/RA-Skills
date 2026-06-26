###### WIP Computer

[![npm](https://img.shields.io/npm/v/@wipcomputer/wip-file-guard)](https://www.npmjs.com/package/@wipcomputer/wip-file-guard) [![CLI / TUI](https://img.shields.io/badge/interface-CLI_/_TUI-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-file-guard/guard.mjs) [![OpenClaw Plugin](https://img.shields.io/badge/interface-OpenClaw_Plugin-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-file-guard/openclaw.plugin.json) [![Claude Code Hook](https://img.shields.io/badge/interface-Claude_Code_Hook-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-file-guard/guard.mjs) [![Claude Code Skill](https://img.shields.io/badge/interface-Claude_Code_Skill-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-file-guard/SKILL.md) [![Universal Interface Spec](https://img.shields.io/badge/Universal_Interface_Spec-black?style=flat&color=black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md)

# File Guard

PreToolUse hook that blocks destructive edits to protected files. When an AI agent tries to overwrite or strip content from files like CLAUDE.md, SHARED-CONTEXT.md, or SOUL.md... it gets blocked with a clear explanation of what went wrong.

## The Problem

AI agents replace content instead of extending it. After context compaction, behavioral rules like "don't delete things" vanish. The agent rewrites your CLAUDE.md, strips 30 lines from SHARED-CONTEXT.md, or replaces your SOUL.md with a shorter version. Every time.

File Guard is a technical guardrail. It doesn't ask the agent to be careful. It blocks the operation before it happens.

## How It Works

Two rules:

1. **Write is blocked** on protected files outside shared state paths. Use Edit instead.
2. **Edit is blocked** when it removes more than 2 net lines from a protected file (20 for shared state).
3. **Shared state paths** (e.g. `~/.openclaw/workspace/`) are always writable. These are live agent workspace files, not code.

The agent gets a deny message explaining what happened and telling it to re-read the file and add content instead of replacing it.

### Protected Files

| File | What it protects |
|------|-----------------|
| `CLAUDE.md` | Project instructions, boot sequence, system docs |
| `SHARED-CONTEXT.md` | Cross-agent shared state |
| `SOUL.md` | Agent identity |
| `IDENTITY.md` | Agent identity (alternate format) |
| `CONTEXT.md` | Current state snapshot |
| `TOOLS.md` | Tool and workflow rules |
| `MEMORY.md` | Persistent memory and preferences |

## Install

Open your AI coding tool and say:

```
Read the README at github.com/wipcomputer/wip-file-guard.
Then explain to me:
1. What is this tool?
2. What does it do?
3. What would it change or fix in our current system?

Then ask me:
- Do you have more questions?
- Do you want to integrate it into our system?
- Do you want to clone it (use as-is) or fork it (so you can contribute back if you find bugs)?
```

Your agent will read the repo, explain the tool, and walk you through integration interactively.

Also see **[wip-release](https://github.com/wipcomputer/wip-release)** ... one-command release pipeline for agent-native software.

See [REFERENCE.md](REFERENCE.md) for manual install instructions (Claude Code, OpenClaw, CLI).

## Four Interfaces

One core, four interfaces into the same guard logic.

| Interface | File | What it does |
|-----------|------|-------------|
| **Core** | `guard.mjs` | Pure guard logic. Reads stdin JSON, decides allow/deny. |
| **Claude Code** | `guard.mjs` (PreToolUse hook) | Hooks into CC's PreToolUse event. Blocks before the edit happens. |
| **OpenClaw** | `openclaw.plugin.json` | Lifecycle hook for OpenClaw agents. Same rules, different runtime. |
| **CLI** | `guard.mjs --list`, `test.sh` | Testing and inspection from the command line. |

See [REFERENCE.md](REFERENCE.md) for customization (adding protected files, changing thresholds).

## Tests

```bash
bash test.sh
```

```
wip-file-guard tests
===================

PASS: Block Write to CLAUDE.md
PASS: Block Write to SHARED-CONTEXT.md
PASS: Allow Write to random file
PASS: Block Edit removing 5 lines from CLAUDE.md
PASS: Allow Edit adding lines to CLAUDE.md
PASS: Allow Edit on non-protected file (even removing lines)
PASS: Allow Edit with small removal (2 lines)
PASS: Block Edit with 4 line removal from SOUL.md
PASS: Block Write to IDENTITY.md
PASS: Block Write to TOOLS.md
PASS: Allow Write to ~/.openclaw/workspace/TOOLS.md (shared state)

Results: 11 passed, 0 failed
```

## Why This Exists

Context compaction erases behavioral rules. An agent that was told "never delete content from CLAUDE.md" forgets that instruction after compaction. It then proceeds to replace 50 lines with 10, confident it's improving the file.

This happened five times in one session. The fix isn't better prompting. It's a hook that blocks the operation before it executes. Behavioral rules degrade. Technical guards don't.

---

## License

```
CLI, OpenClaw plugin, hooks                    MIT    (use anywhere, no restrictions)
Hosted or cloud service use                    AGPL   (network service distribution)
```

AGPL for personal use is free.

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
