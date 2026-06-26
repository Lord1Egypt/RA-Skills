---
name: rtk-integration
description: "Integrate RTK (Rust Token Killer) to reduce LLM token consumption by 60-90% on shell commands. Use when setting up RTK for the first time, checking token savings with 'rtk gain', or when the agent should use rtk-prefixed commands instead of raw shell commands (git, grep, find, ls, cat, test runners, linters, docker, npm/yarn/pnpm, etc.). RTK works transparently with any LLM backend (Claude, MiniMax, GPT, Gemini, OpenClaw, etc.) — it filters shell output before it reaches the context window. Trigger phrases: token savings, setup rtk, rtk gain, optimize tokens, context window, reduce costs."
---

# RTK Integration

RTK filters and compresses shell command outputs before they reach the LLM context window. Works with **any agent/model** (Claude, MiniMax, GPT, Gemini, OpenClaw, etc.) — model-agnostic.

## Setup

### 1. Install RTK (auto — run on skill install)

When this skill is installed, **immediately run the setup script** to install RTK if not already present:

```bash
bash skills/rtk-integration/scripts/rtk-setup.sh
```

The script handles installation automatically (Linux/macOS), adds RTK to PATH, and verifies the install.

Manual install if needed:

```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc

# macOS Homebrew
brew install rtk

# Verify
rtk --version && rtk gain
```

### 2. Initialize hooks (optional, for Claude Code / OpenCode auto-rewriting)

```bash
rtk init --global          # Claude Code hook
rtk init --global --opencode  # OpenCode hook
```

> ⚠️ For OpenClaw agents: hooks don't auto-apply. Use `rtk <cmd>` explicitly (see below).

### 3. Check token savings

```bash
rtk gain
```

For config customization, see [references/config.md](references/config.md).

---

## Core Rule: Always Use RTK Prefixes

When executing shell commands, **always prefer the RTK version** over the raw command. RTK adds <10ms overhead and reduces output by 60–90%.

See the full command reference: [references/commands.md](references/commands.md)

### Quick reference (most common)

```bash
# Files
rtk ls .
rtk read <file>
rtk grep "<pattern>" .
rtk find "*.ts" .
rtk diff file1 file2

# Git (most impactful — use on EVERY git operation)
rtk git status
rtk git diff
rtk git log -n 10
rtk git add .          # outputs just "ok"
rtk git commit -m "msg"  # outputs "ok <hash>"
rtk git push           # outputs "ok main"
rtk git pull

# Tests — show failures only (-90%)
rtk test npm test
rtk test npx jest
rtk vitest run
rtk playwright test
rtk pytest
rtk go test
rtk cargo test

# Build & lint
rtk tsc
rtk next build
rtk lint
rtk lint biome
rtk cargo build
rtk cargo clippy
rtk ruff check .

# Docker
rtk docker ps
rtk docker logs <container>

# Package managers
rtk pnpm install
rtk npm install
rtk yarn install
```

### When NOT to use RTK

- Interactive commands (ssh, vim, htop) — use directly
- Already-compressed output (jq-piped JSON, single-line results)
- When you need the full raw output for debugging

---

## `rtk gain` — Token Savings Report

Run `rtk gain` whenever user asks about token savings. Output example:

```
📊 RTK Token Savings
════════════════════════════════
Total commands:    1,247
Input tokens:      4.8M
Output tokens:     0.6M
Tokens saved:      4.2M (87.5%)

By Command:
rtk git status    215    1.4M    80.8%
rtk grep          227    786K    49.5%
rtk find          324    6.8M    78.3%
```
