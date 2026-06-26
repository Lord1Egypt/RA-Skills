---
name: safehub
description: Scan OpenClaw skills for malware and security issues before installation. Use when the user wants to verify a skill is safe, audit a ClawHub skill, or check a local or GitHub skill.
version: 1.0.2
author: sumeetghimire
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["node","semgrep","git"]},"os":["darwin","linux","win32"]}}
---

# SafeHub

SafeHub is a security scanner for OpenClaw skills. It runs static analysis (Semgrep) and optional sandbox execution (Docker) on any skill—by name, local path, or GitHub URL—and returns a trust score and a clear recommendation: **safe to install**, **install with caution**, or **not safe**.

## Requirements

These binaries must be on your PATH (declared in registry metadata):

- **Node.js** (18+) — required to run the CLI.
- **Semgrep** — required for the scan command (static analysis). Install with `brew install semgrep` or `npm install -g semgrep`.
- **git** — required when the scan target is a GitHub URL (used to clone the repo).

**Optional:**

- **Docker** — used for sandbox execution. If Docker is not available, use `--no-sandbox` for static-only scanning.

## Environment variables

All of these are optional. No secrets or API tokens are required by default.

| Variable | Default | Effect |
|----------|---------|--------|
| **SAFEHUB_RULES_REPO** | `safehub/safehub` | GitHub repo (owner/repo) used by `safehub update` to fetch and **overwrite** local rule files in `./rules`. Setting this to another repo makes the updater pull rules from that repo — use only repos you trust. |
| **SAFEHUB_RULES_BRANCH** | `main` | Branch name used when fetching rules (with `SAFEHUB_RULES_REPO`). |
| **SAFEHUB_DATA_DIR** | `~/.safehub` | Directory for cached scan reports (e.g. `~/.safehub/reports`). |
| **SAFEHUB_SANDBOX_IMAGE** | `node:18-alpine` | Docker image used for the sandbox when scanning. |
| **SAFEHUB_SANDBOX_TIMEOUT_MS** | `30000` | Timeout (ms) for the sandbox run before the container is killed. |
| **SAFEHUB_NO_TYPING** | (unset) | Set to `1` to disable the typing-effect output (e.g. in CI or pipes). |

**Important:** `SAFEHUB_RULES_REPO` controls where `safehub update` downloads rules from and overwrites local `./rules`; only point it at a repo you trust.

## Commands

All commands are run via the `safehub` CLI (e.g. `safehub scan <target>` or `node index.js scan <target>` from the skill directory).

### scan

Scan a skill by ClawHub name, local path, or GitHub URL.

**Examples:**

```bash
safehub scan web-scraper
safehub scan ./my-local-skill
safehub scan https://github.com/user/their-skill
safehub scan https://github.com/BenedictKing/tavily-web --no-sandbox
```

**Options:**

- `--no-sandbox` — Skip Docker sandbox; run static analysis only (use when Docker is not installed).

### report

Show the last scan report for a skill without rescanning.

**Examples:**

```bash
safehub report web-scraper
safehub report risky-skill
```

### update

Pull the latest Semgrep scanner rules from the SafeHub GitHub repo (or your fork via `SAFEHUB_RULES_REPO`).

**Examples:**

```bash
safehub update
SAFEHUB_RULES_REPO=owner/repo safehub update
```

## Example output

After running `safehub scan <target>`, you’ll see:

- **Static analysis** — Findings from Semgrep (network, filesystem, eval/exec, env, obfuscation).
- **Sandbox behavior** — Whether the skill attempted network access or suspicious actions (when Docker is used).
- **Trust score** (0–100) and recommendation: **SAFE TO INSTALL**, **INSTALL WITH CAUTION**, or **NOT SAFE TO INSTALL**.

## Installation (users)

Install from ClawHub:

```bash
clawhub install safehub
```

Or install the CLI globally from npm:

```bash
npm install -g safehub
```

Then run `safehub scan <target>` (if the CLI is on PATH) or `node index.js scan <target>` from the skill directory.
