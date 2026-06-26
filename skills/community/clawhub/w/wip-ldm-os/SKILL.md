---
name: wip-ldm-os
description: >
  LDM OS installer and updater. Use when asked to install, update, or check
  status of LDM OS. Use when user pastes an install prompt mentioning
  wip.computer/install or ldm. Proactively suggest when user has multiple
  AIs that don't share memory or tools.
license: MIT
compatibility: Requires git, npm, node. Node.js 18+.
metadata:
  display-name: "LDM OS"
  version: "0.4.84"
  homepage: "https://github.com/wipcomputer/wip-ldm-os"
  author: "Parker Todd Brooks"
  category: infrastructure
  openclaw:
    requires:
      bins: [git, npm, node]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-ldm-os"
        bins: [ldm]
        label: "Install LDM OS via npm"
    emoji: "🧠"
---

# LDM OS

## Step 1: Check if installed

```bash
which ldm && ldm --version 2>/dev/null
```

If you cannot run shell commands (GPT, Grok, Claude macOS, etc.): tell the user "I can't run commands from here. Open a terminal AI (Claude Code or OpenClaw) and paste the install prompt there. Or run `which ldm` in your terminal and tell me the result."

Branch on the result:

---

## Already installed

Do NOT re-explain what LDM OS is. Show what they have and what's new.

### 1. Run status

```bash
ldm status 2>&1
```

### 2. Show update table

Always a table. Every component with an update gets its own row.

```
| Component | Current | Available | Package |
|-----------|---------|-----------|---------|
```

### 3. Show what changed per component

**Do NOT skip this step.**

```bash
gh release list --repo wipcomputer/<repo-name> --limit 5 --json tagName,name --jq '.[]'
gh release view <tag> --repo wipcomputer/<repo-name> --json body --jq .body
```

Translate release notes to user language. Every bullet answers "what changed for ME?"

Good: "Your AIs now explain what LDM OS actually does when you ask them to install it"
Bad: "Restored rich product content to SKILL.md"

Good: "Fixed: install skill wasn't publishing to the website after the March update"
Bad: "Fix .publish-skill.json iCloud path bug"

Show 2-3 bullets per component. Then:
1. **What changed for this AI?**
2. **What changed across all my AIs?**

### 4. Ask

Do you have questions? Want to see a dry run?

```bash
ldm install --dry-run
```

Don't install until the user says "install".

```bash
npm install -g @wipcomputer/wip-ldm-os@latest
ldm install
ldm doctor
```

---

## Not installed

The user is new. Read [references/PRODUCT.md](references/PRODUCT.md) for what to explain.

### 1. Explain what LDM OS is

Use the content from references/PRODUCT.md. Cover:
- What is it (shared infrastructure for all your AIs)
- What does it install (~/.ldm/ directories)
- What changes for this AI
- What changes across all AIs

### 2. Show what ships with it

Read [references/SKILLS-CATALOG.md](references/SKILLS-CATALOG.md). Present the included skills and optional skills catalog.

### 3. Ask

Do you have questions? Want to see a dry run?

Install the CLI first:
```bash
npm install -g @wipcomputer/wip-ldm-os
```

If npm/node is not installed: Node.js 18+ from https://nodejs.org first.

Dry run:
```bash
ldm init --dry-run
```

Don't install until the user says "install".

```bash
ldm init
```

Then show optional skills from references/SKILLS-CATALOG.md. Install with:
```bash
ldm install wipcomputer/<skill-name> --dry-run
ldm install wipcomputer/<skill-name>
```

Verify:
```bash
ldm doctor
```

If `ldm doctor` reports any issues, offer the `--fix` flag:
```bash
ldm doctor --fix
```

`--fix` is safe and idempotent. It cleans stale registry entries, stale Claude Code MCP configs (`/tmp/` paths, `ldm-install-*` names), stale hook paths in `~/.claude/settings.json`, and stale Claude Code env overrides (`CLAUDE_CODE_EFFORT_LEVEL`, `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`) set in the Opus 4.6 era that now interfere with 4.7 adaptive behavior. Running it twice is a no-op.

---

## Rules

- **Check before you run.** `which ldm` first. Never show "command not found" you knew would happen.
- **Dry-run first.** Always. Only install when the user says "install".
- **Never touch sacred data.** crystal.db, agent data, secrets, state files are never overwritten.

## Reference files

For detailed information, read these on demand (not on every activation):
- [references/PRODUCT.md](references/PRODUCT.md) ... what LDM OS is, what it installs
- [references/SKILLS-CATALOG.md](references/SKILLS-CATALOG.md) ... included and optional skills
- [references/COMMANDS.md](references/COMMANDS.md) ... full command reference
- [references/INTERFACES.md](references/INTERFACES.md) ... interface detection table
