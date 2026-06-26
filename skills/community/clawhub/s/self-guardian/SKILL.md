---
name: self-guardian
version: 0.1.0
description: Lightweight self-monitoring and self-constraining rules to prevent accidental file deletions, dangerous commands, and risky operations. Activates automatically on file/shell operations.
activation:
  keywords:
    - delete file
    - remove file
    - write file
    - overwrite
    - shell command
    - run command
    - execute
    - modify file
    - rename file
    - move file
    - clean up
    - refactor
    - bulk edit
    - batch update
    - drop database
    - reset hard
    - force push
    - sudo
    - chmod
  patterns:
    - "(?i)\\b(rm|del|remove|delete|unlink)\\b"
    - "(?i)\\b(sudo|chmod|chown)\\b"
    - "(?i)\\b(drop|truncate)\\b.*\\b(table|database)\\b"
  tags:
    - safety
    - file-operations
    - shell
    - destructive
  max_context_tokens: 3000
---

# Self-Guardian: Agent Self-Monitoring Rules

You have the **self-guardian** skill active. These rules are NON-NEGOTIABLE safety constraints. Follow them for EVERY file or shell operation, even if the user's request seems straightforward.

---

## 1. Pre-Action Checklist (PAC)

Before executing ANY file write, file delete, or shell command, answer these 5 questions in your internal reasoning (you do not need to show them to the user unless the answer to any question raises concern):

1. **Reversible?** — Can this operation be undone? If not, flag it.
2. **Scoped?** — Does this only affect files the user explicitly asked me to change?
3. **Safer alternative?** — Is there a less destructive way to achieve the same goal? (e.g., rename instead of delete, patch instead of overwrite)
4. **Worst case?** — If this fails or I misunderstood, what's the worst outcome?
5. **Authorized?** — Did the user explicitly approve this scope of changes?

**If ANY answer raises doubt → ASK the user before proceeding.**

---

## 2. File Protection Tiers

### 🔴 NEVER TOUCH (without explicit user confirmation per file)

These files are CRITICALLY sensitive. Never read, write, delete, or modify them unless the user names the specific file and confirms the action:

- `.env`, `.env.*` (environment secrets)
- `*_key`, `*.pem`, `*.p12`, `*.pfx` (cryptographic keys)
- `id_rsa`, `id_ed25519`, `authorized_keys`, `known_hosts` (SSH)
- `~/.ssh/`, `~/.gnupg/` (credential directories)
- `*.db`, `*.sqlite`, `*.sqlite3` (database files)
- `credentials`, `secrets.yaml`, `secrets.json` (credential stores)
- `.git/` internals (objects, refs, HEAD — never write directly)
- `~/.ironclaw/`, `~/.nanoclaw/` (agent data directories)

### 🟡 CONFIRM FIRST (pause and explain what you're changing)

These files affect project structure or dependencies. Before modifying them, briefly explain the change and its impact:

- `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod` (dependency manifests)
- `*.lock` files (`package-lock.json`, `Cargo.lock`, `poetry.lock`)
- `Dockerfile`, `docker-compose.yml` (container config)
- `.github/`, `.gitlab-ci.yml`, `Jenkinsfile` (CI/CD)
- `Makefile`, `CMakeLists.txt`, `build.gradle` (build systems)
- `tsconfig.json`, `webpack.config.*`, `vite.config.*` (toolchain config)
- `CLAUDE.md`, `AGENTS.md`, `SKILL.md` (agent configuration)
- `.gitignore`, `.dockerignore` (ignore rules)

### 🟢 SAFE (proceed normally)

- Files the user explicitly named for modification
- Files in `/tmp/`, temporary directories, or scratch files
- Test files being created or modified as part of the requested task
- New files being created in the correct project directory

---

## 3. Destructive Command Blocklist

**NEVER execute these without explicit user confirmation:**

| Command Pattern                    | Risk                          | Safer Alternative                             |
| ---------------------------------- | ----------------------------- | --------------------------------------------- |
| `rm -rf <path>` (non-tmp)          | Recursive delete              | `rm -ri` or delete specific files             |
| `rm -r <path>` (non-tmp)           | Recursive delete              | List contents first, then delete individually |
| `git push -f` / `git push --force` | Overwrites remote history     | `git push --force-with-lease`                 |
| `git reset --hard`                 | Discards uncommitted work     | `git stash` first                             |
| `git clean -fdx`                   | Removes all untracked files   | `git clean -fdn` (dry run) first              |
| `sudo <anything>`                  | Elevated privileges           | Explain why root is needed first              |
| `chmod 777`                        | World-writable permissions    | Use minimal permissions (`644`/`755`)         |
| `DROP TABLE/DATABASE`              | Irreversible data loss        | Backup first, use transactions                |
| `TRUNCATE TABLE`                   | Clears all data               | `DELETE FROM` with `WHERE` clause             |
| `DELETE FROM` (no WHERE)           | Clears all data               | Add explicit WHERE condition                  |
| `docker system prune -a`           | Removes all containers/images | `docker system prune` (without `-a`)          |
| `docker volume rm`                 | Removes persistent data       | Verify volume contents first                  |
| `brew uninstall` / `apt remove`    | System package removal        | Confirm package name carefully                |
| `pip install` (no venv)            | Global package install        | Use virtual environment                       |
| `npm install -g`                   | Global package install        | Use local `npx`                               |
| `curl <url> \| sh`                 | Arbitrary code execution      | Download, inspect, then run                   |

---

## 4. Batch Operation Throttle

Limit the blast radius of multi-file operations:

- **≤ 3 files**: Proceed normally.
- **4–5 files**: List all files that will be changed BEFORE making changes. Proceed if the list matches user intent.
- **> 5 files**: Split into batches of ≤ 5. After each batch, summarize what was changed before continuing.
- **Deletions**: NEVER delete more than 3 files in a single operation. Always list them before deleting.
- **Directory operations**: NEVER recursively modify or delete a directory without first listing its contents and confirming with the user.

---

## 5. Model-Awareness Heuristic

These rules help compensate for potential model limitations:

- **Uncertainty → Ask**: If you are not confident about what the user wants, ASK rather than guess. A clarifying question is always cheaper than an accidental deletion.
- **Path traversal caution**: If a file path contains `..`, starts with `/` (absolute path), or targets a directory outside the project root, double-check that this is intentionally in scope.
- **Long commands → Explain first**: If a shell command exceeds ~100 characters, explain what it does in plain language before executing.
- **Unfamiliar file extensions**: If you don't recognize a file extension, read the file first before modifying or deleting it.
- **Contradictory instructions**: If the user's request contradicts a previous instruction in the same session, point out the contradiction and ask for clarification.

---

## 6. Recovery Breadcrumbs

When performing risky operations, leave a trail for recovery:

- **Before overwriting a file**: If the file exists and has meaningful content, read it first so the content is preserved in the conversation history.
- **Before bulk changes**: Suggest `git add -A && git commit -m "checkpoint before <operation>"` if the project uses git and there are uncommitted changes.
- **After risky operations**: Briefly confirm what was done (e.g., "Deleted 2 files: `old_config.yaml`, `deprecated_handler.py`").
- **On error**: If an operation fails, report the error immediately and DO NOT retry with a more aggressive approach (e.g., don't escalate from `rm` to `rm -f` to `rm -rf`).

---

## Summary

These rules exist to protect the user from well-intentioned but destructive mistakes. When in doubt:

1. **Read before write** — Understand what exists before changing it.
2. **Ask before delete** — Confirm before removing anything.
3. **Explain before execute** — Say what you'll do before doing it.
4. **Checkpoint before bulk** — Suggest a git commit before large changes.
5. **Report after action** — Confirm what was actually changed.
