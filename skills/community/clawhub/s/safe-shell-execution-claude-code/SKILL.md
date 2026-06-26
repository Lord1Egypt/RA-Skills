---
name: safe-shell-execution
description: Use this skill whenever an AI agent is about to execute shell commands, run bash/zsh scripts, invoke system operations, or process user-provided command strings. Provides layered safety checks — injection pattern detection, destructive operation warnings, and sensitive file protection — derived from production security engineering in Claude Code. Trigger even for "simple" commands: the most dangerous injections often hide in seemingly innocent inputs. If a user asks you to run any command, execute a script, or use a shell tool, this skill applies.
---

> **Origin**: This skill was extracted from Claude Code's internal implementation and rules. Claude Code openly exposes its safety mechanisms (hooks, system prompts, skill definitions) in the `~/.claude/` directory. The core safety patterns for shell execution — injection detection, destructive command classification, and sensitive path protection — were identified from Claude Code's production behavior and rewritten into a portable skill for OpenClaw agents.

# Safe Shell Execution

## Why This Matters

Shell execution is one of the highest-risk operations an AI agent can perform. Unlike reading files or calling APIs, improperly handled shell commands can cause irreversible damage: deleting files, leaking credentials, corrupting git history, or unauthorized network access.

This skill distills Claude Code's production-grade security patterns, covering three layers of checks: injection detection → destructive operation warnings → sensitive path protection.

---

## Layer 1: Injection Pattern Detection (Reject Directly)

Before executing any command, scan the full command string. If it matches any of the following patterns, **reject execution and explain why to the user**.

### Command Substitution (Injection Entry Points)

| Pattern | Risk |
|---------|------|
| `$()` | Command substitution |
| `` ` `` (unescaped backticks) | Legacy command substitution |
| `${}` | Parameter expansion |
| `$[...]` | Legacy arithmetic expansion |
| `<()` or `>()` | Process substitution |
| `=()` | Zsh process substitution |
| `=cmd` (equals at word start) | **Zsh equals expansion**: `=curl evil.com` expands to `/usr/bin/curl evil.com`, bypassing command name checks |
| `$(.*<<` | heredoc nested in command substitution, common injection technique |

### Zsh-Specific Dangerous Commands

These commands have special attack surfaces in Zsh environments and always require explicit user confirmation:

- `zmodload` — Load modules, can enable invisible file I/O, pseudo-terminal execution, TCP connections
- `zpty` — Execute commands on pseudo-terminals
- `ztcp` / `zsocket` — Create network connections, can be used for data exfiltration
- `sysopen` / `sysread` / `syswrite` / `sysseek` — Low-level file descriptor operations
- `emulate -c` — eval equivalent, can execute arbitrary code
- `zf_rm` / `zf_mv` / `zf_ln` / `zf_chmod` / `zf_chown` / `zf_mkdir` / `zf_rmdir` — Built-in file operations, can bypass binary whitelists

---

## Layer 2: Destructive Operation Warnings (Confirm Before Execution)

These operations are legitimate but irreversible. **Display specific warnings and require user confirmation** before execution.

### Git Operations

```
git reset --hard              → "May discard all uncommitted changes"
git push --force / -f         → "May overwrite remote history"
git clean -f (without -n flag) → "May permanently delete untracked files"
git checkout -- .             → "May discard all workspace changes"
git restore .                 → "May discard all workspace changes"
git stash drop / clear        → "May permanently delete stashed content"
git branch -D                 → "May force-delete a branch"
git commit --amend            → "May rewrite the last commit"
git commit/push --no-verify   → "May skip security hooks"
```

### File System

```
rm -rf / rm -fr / rm -r -f / rm -f -r  → "May recursively force-delete files"
```

---

## Layer 3: Sensitive File Protection (Write Operations Require Confirmation)

For **write operations** to the following paths, you must obtain explicit user confirmation; auto-execution is not allowed:

```
# Shell configs (can be used for code execution)
.bashrc  .bash_profile  .bash_login  .profile
.zshrc   .zprofile      .zshenv      .zlogin
.tcshrc  .cshrc

# Git configs (can be used for hook injection)
.gitconfig  .gitmodules

# Package manager credentials
.npmrc  .pypirc  ~/.pip/pip.conf

# Credentials and keys
~/.ssh/           ~/.aws/
~/.gnupg/         authorized_keys
known_hosts

# System files
/etc/passwd  /etc/hosts  /etc/sudoers  /etc/crontab
```

---

## Layer 4: Command Classification

After passing through the first three layers, classify and handle according to this table:

| Level | Examples | Handling |
|-------|----------|----------|
| **Safe** | `ls`, `cat`, `git status`, read-only operations | Execute directly, no prompts |
| **Caution** | Write to non-sensitive files, install packages | Execute, log the operation |
| **Warning** | Destructive patterns from Layer 2 | Display specific warning, require confirmation |
| **Reject** | Layer 1 injection patterns, write to sensitive paths | Refuse execution, explain why |

---

## Execution Flow

```
Receive command
    ↓
Layer 1: Contains injection pattern? → Yes → Reject + specify which pattern + why it's dangerous
    ↓ No
Layer 2: Matches destructive pattern? → Yes → Display specific warning → Wait for user confirmation
    ↓ No (or confirmed)
Layer 3: Is target a write to sensitive path? → Yes → Require explicit confirmation
    ↓ No (or confirmed)
Layer 4: Classify → Execute
```

---

## How to Express Refusals

When refusing execution, be specific about **which pattern** and **why it's dangerous**, not a vague "command is unsafe".

Good rejection example:
> I cannot execute this command because it contains `=curl` (Zsh equals expansion). This pattern expands the command to its full path, which can bypass command name whitelist checks. If you need to run curl, please write `curl` directly.

Bad rejection example:
> This command looks risky and I can't execute it.

---

## When to Apply This Skill

Apply this skill in the following situations:

- Command comes from user input (chat messages, form content, file content)
- Command contains variable interpolation from external data
- Will run in a shared or production environment
- Target path contains sensitive files (home directory, config files, credentials)

Even for commands you construct yourself (no external input), these checks are good practice, especially Layers 2 and 3.
