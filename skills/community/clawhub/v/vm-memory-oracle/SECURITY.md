# Security Policy

## Scope

This document describes the security properties of the `vm-memory-oracle` skill
for ClawHub reviewers and users evaluating this skill for deployment.

## Security Properties

### What this skill does

- Reads and writes files under a single configurable directory (`data_path`,
  default `/data/memory/`).
- Creates and manages cron jobs under `/etc/cron.d/openclaw-vm-memory-oracle`.
- Processes JSON and Markdown files using `jq` and standard shell utilities.

### What this skill does NOT do

- **No network access.** This skill never opens sockets, makes HTTP requests,
  performs DNS lookups, or communicates with any external service. All data
  remains on the local filesystem.
- **No credential handling.** This skill never reads, writes, stores, or
  transmits API keys, tokens, passwords, SSH keys, wallet keys, browser cookies,
  session tokens, or any other authentication material.
- **No privilege escalation.** This skill never uses `sudo`, `su`, `pkexec`,
  `doas`, or any other mechanism to elevate privileges.
- **No code obfuscation.** All logic is in plain Markdown instructions and
  shell scripts. No Base64-encoded payloads, hex-encoded commands, string
  concatenation tricks, eval(), or dynamic code generation.
- **No binary execution.** This skill does not download or execute binaries.
  The only binary file it manages is the embedding index (`index.bin`), which
  is generated locally from source facts and is never executed.
- **No system modification.** This skill does not modify system configuration
  files, kernel parameters, firewall rules, or user accounts.
- **No container escape.** This skill does not interact with container runtimes,
  Docker sockets, or orchestration APIs.

## Filesystem Scope

All file operations are confined to:

| Path | Operations | Purpose |
|---|---|---|
| `{data_path}/` | Read, Write, Create | Memory data storage |
| `{data_path}/backups/` | Write, Delete | Pre-maintenance backups (7-day retention) |
| `/etc/cron.d/openclaw-vm-memory-oracle` | Write | Cron job registration |
| `/var/log/openclaw/` | Write | Log output from cron jobs |

No other paths are accessed.

## Dependencies

| Dependency | Source | Purpose |
|---|---|---|
| `jq` | System package manager | JSON parsing and validation |
| `cron` | System package manager | Scheduled task execution |

No third-party packages, pip/npm modules, or remote dependencies are installed
or required at runtime.

## Reporting Vulnerabilities

If you discover a security issue in this skill, please open an issue on the
GitHub repository or contact the author directly. Do not publish details of
security vulnerabilities before they are addressed.
