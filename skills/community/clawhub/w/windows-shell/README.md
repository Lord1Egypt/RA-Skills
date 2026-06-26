# win-encoding-fix

Windows Shell encoding skill for AI coding assistants. Fixes GBK/UTF-8 encoding issues on Windows 10+ with MSYS2/Git Bash.

Tested and verified on real Windows 10 (code page 936/GBK) environments.

## Problem

On Windows with GBK locale, AI coding assistants (Claude Code, Codex, OpenClaw) frequently produce garbled Chinese output because:

- PowerShell outputs GBK by default, but the terminal expects UTF-8
- Traditional CMD tools (`wmic`, `systeminfo`, etc.) output UTF-16 or GBK
- Python `print()` and `open()` default to GBK
- Node.js `execSync` decodes GBK output as UTF-8
- Git shows Chinese filenames as octal escapes

This skill teaches AI assistants to handle all these cases correctly.

> **A subtle trap this skill solves:** exports written to `~/.bash_profile` are only sourced by *login* shells. AI assistants and scripts run in **non-interactive** shells that source neither `.bash_profile` nor `.bashrc`, so `PYTHONUTF8=1` set there never reaches the Python the agent actually runs (`sys.flags.utf8_mode` stays `0`). v4.1.0 fixes this by setting **Windows User-level environment variables** (inherited by every process) and by having `.bashrc` source `.bash_profile`.

## What's Included

- **8 encoding rules** covering PowerShell/pwsh, CMD, Python, Node.js, and Git
- **Quick reference table** + an environment self-check
- **Code generation rules** ensuring AI-written code handles encoding properly
- **Robust environment setup** — Windows User env vars + bash rc files + git config

## Install

### npx (recommended)

```bash
npx win-encoding-fix install --setup-env
```

### npm global

```bash
npm install -g win-encoding-fix
win-encoding-fix install --setup-env
```

### Manual

Copy `SKILL.md` to:

| Platform | Path |
|----------|------|
| Claude Code | `~/.claude/skills/windows-shell/SKILL.md` |
| Codex | `~/.codex/skills/windows-shell/SKILL.md` |
| OpenClaw | `~/.openclaw/workspace/skills/windows-shell/SKILL.md` |

## Commands

```bash
win-encoding-fix install              # Install to auto-detected platforms
win-encoding-fix install --setup-env  # Also configure bash_profile + git
win-encoding-fix setup-env            # Only configure environment
win-encoding-fix uninstall            # Remove skill files

# Custom install paths (if not using default locations)
win-encoding-fix install --claude=D:\my-claude
win-encoding-fix install --codex=E:\my-codex
win-encoding-fix install --openclaw=E:\.openclaw
```

## Environment Setup

The `--setup-env` flag configures three layers so the fixes apply everywhere:

**1. Windows User environment variables** (inherited by every process — the robust layer; takes effect after restarting the terminal):
```
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
```

**2. bash rc files** (for interactive Git Bash):
```bash
# ~/.bash_profile
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LESSCHARSET=utf-8
# ~/.bashrc — so non-login shells get the same vars
[ -f ~/.bash_profile ] && . ~/.bash_profile
```

**3. Git global config:**
```bash
git config --global core.quotepath false        # Chinese filenames
git config --global core.autocrlf input         # LF on commit
git config --global i18n.commitEncoding utf-8
git config --global i18n.logOutputEncoding utf-8
git config --global core.pager "less -R"
```

## Rules Summary

| # | Rule | Scope |
|---|------|-------|
| 1 | PowerShell/pwsh: UTF-8 prefix + single quotes | Shell |
| 2 | PowerShell: `-Encoding UTF8` for file reads | Shell |
| 3 | Never use legacy CMD tools or `cmd /c` | Shell |
| 4 | Python: prefer `python -X utf8` (don't assume env is loaded) | Shell |
| 5 | Node.js: PowerShell wrapper for `execSync` | Shell |
| 6 | Python codegen: `open()` must have `encoding='utf-8'` | Code |
| 7 | Node.js codegen: explicit `'utf-8'` in fs/child_process | Code |
| 8 | Git: `core.quotepath=false` for Chinese filenames | Git |

## Testing

```bash
npm test    # runs node test/cli.test.js
```

The suite covers install (custom paths, idempotency, content integrity), uninstall,
help, unknown-command fallback, `setup-env` (rc files + git config, isolated from the
real environment), and SKILL.md frontmatter validity.

## License

MIT
