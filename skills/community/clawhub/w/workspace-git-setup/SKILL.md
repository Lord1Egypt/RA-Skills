---
name: workspace-git-setup
description: "One-command Git tracking setup for any working directory, with a security-focused .gitignore (credentials, TLS/SSH private keys, tokens, runtime caches & PIDs, node_modules, Python caches, build artifacts, editor temp files), a large-file guard (>10MB), and a read-only --audit mode that detects tracked secrets, untracked files, and core.autocrlf misconfiguration. Three modes: (1) init — git init + safe .gitignore + first commit; (2) --audit — read-only health check (no mutations); (3) --dry-run — preview every change without applying. Reads Git identity from GIT_AUTHOR_NAME/GIT_AUTHOR_EMAIL env vars > existing git config > interactive prompt; falls back to the email prefix when only the email is provided. Workspace path resolution: CLI arg > WORKSPACE_DIR env var > current directory. Default branch is main; sets core.autocrlf=input to avoid CRLF false diffs. Trigger this skill when the user says any of: 'add git to my project', 'init git', 'git init', 'track my changes', 'version history', 'back up my workspace', 'is my repo healthy', 'audit my git repo', 'any secrets in git', 'find untracked files', 'fix git config', 'workspace git setup', 'workspace-git-setup' — or 「给项目加 git」「初始化 git」「记录我的改动」「追踪变更历史」「保存历史版本」「项目怎么做版本管理」「我改了很多东西怕丢，帮我备份」「检查 git 有没有问题」「巡检 git」「有没有敏感文件进 git」「检测漏跟踪的文件」「.gitignore 规则过期了」「修复 git 配置」 — or any other phrasing that expresses the intent to add version tracking, audit a repo's health, or guard against accidental secret leaks."
license: MIT
metadata:
  author: Evan Song
  version: "1.0.3"
---

# workspace-git-setup

One command to set up safe, sensible Git tracking for any working directory — with a built-in security audit.

A zero-dependency Bash script that initializes Git version control for a project, ships a battle-tested security `.gitignore`, warns about large files before your first commit, and can audit an existing repo for leaked secrets and untracked files.

**Pure `bash` + `git`. No Python, no npm, no third-party packages.**

- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills
- **License**: MIT

## Usage

```bash
# Initialize / align config (defaults to current directory; auto-uses dir name as project name)
bash scripts/setup.sh

# Specify workspace path and project name
bash scripts/setup.sh /path/to/project "MyProject"

# Audit mode (read-only): detects sensitive files / untracked files / config
bash scripts/setup.sh --audit

# Dry-run mode: preview every action without applying anything
bash scripts/setup.sh --dry-run
```

## Path & identity resolution

| Item | Priority |
|------|----------|
| Workspace path | CLI argument > `WORKSPACE_DIR` env var > current directory |
| Git identity | `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` env vars > existing git config > interactive prompt |

> When only an email is provided, the email prefix is used as the username (you can change it later with `git config`).

## Three modes

| Mode | What it does | Mutates? |
|------|--------------|----------|
| *(default)* init / align | git init + writes safe .gitignore + large-file warning + first commit | ✏️ yes |
| `--audit` | read-only health check: tracked secrets / untracked files / core.autocrlf | 👀 no |
| `--dry-run` | preview every change without applying | 👀 no |

## Default flow (init mode)

1. **Resolve path** — CLI arg > `WORKSPACE_DIR` > current directory
2. **Infer project name** — workspace basename (override with the 2nd argument)
3. **Read identity** — env vars → existing git config → interactive prompt
4. **git init** — skipped if a repo already exists (idempotent); sets `core.autocrlf=input` to unify line endings; default branch `main`
5. **Write `.gitignore`** — if one exists, shows a diff and asks before overwriting
6. **Large-file warning** — scans files >10MB to be tracked and asks for confirmation
7. **First commit** — auto-stages and commits
8. **Summary** — shows project name, path, git identity, and audit usage

## Default `.gitignore` rules (general-purpose security)

| Category | Patterns |
|----------|----------|
| Credentials | `.env`, `.env.*`, `*.pem`, `secrets/`, `.credentials/`, `*token*.json`, `*secret*.json` |
| TLS / SSH keys | `**/certs/*.key`, `id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`, `*.p12`, `*.keystore` |
| Temp / cache | `tmp/`, `*.tmp`, `*.cache`, `*.log`, `*.pid` |
| OS / editor | `.DS_Store`, `._*`, `Thumbs.db`, `.vscode/`, `.idea/`, `*.swp`, etc. |
| Dependencies | `node_modules/`, `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.pytest_cache/` |
| Build output | `output/`, `dist/`, `build/`, `out/`, `*.egg-info/` |

> Note: private-key ignores are scoped to `**/certs/*.key` (instead of a blanket `*.key`) so legitimate `.key` files elsewhere are not hidden.

## Audit mode (`--audit`)

Read-only run that outputs three checks, **never modifies anything**:

1. **Sensitive file detection** — lists private keys / tokens / credentials already tracked by Git. Warns only, gives human-review guidance, no destructive commands.
2. **Untracked file detection** — lists files that are neither added nor ignored.
3. **Config check** — whether `core.autocrlf` is sane and `.gitignore` exists.

## Notes

- Pure local Git, no remote; add one yourself when ready: `git remote add origin <url>`
- Script is idempotent and safe to re-run; existing config is preserved.
- If a `.gitignore` already exists, a diff is shown and you choose whether to overwrite.
- Audit only warns on tracked sensitive files — you decide how to remove them.
- When no Git identity is found in env vars or git config, the script falls back to interactive prompts (cannot run unattended without env vars).

## Dependencies

- `git` (required) — https://git-scm.com/downloads
- `bash` 4.0+
- `coreutils` (`numfmt`/`stat`/`realpath`) — preinstalled on most Unix-like systems; `numfmt` is optional (falls back to raw byte counts when absent).

> Pure bash + git implementation, no Python or third-party packages required.
