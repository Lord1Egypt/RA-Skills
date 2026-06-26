# SafeHub

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SafeHub** is an open source OpenClaw skill that scans other OpenClaw skills for malware and security issues before you install them. It uses Semgrep for static analysis and Docker for sandboxed execution so you can see what a skill does and whether it’s safe to use.

---

## What SafeHub Does

- **Static analysis** — Runs Semgrep rules to find outbound network calls, filesystem writes, `eval`/`exec`, env access, and obfuscation.
- **Sandbox run** — Executes the skill in an isolated Docker container (no network, read-only filesystem except `/tmp`) and observes behavior.
- **Trust score** — Produces a 0–100 score and a clear recommendation: safe to install, install with caution, or not safe.

---

## Prerequisites

SafeHub requires these binaries on your PATH (declared in skill metadata):

- **Node.js 18+**
- **Semgrep** (required for the scan command):  
  `npm install -g semgrep` or `brew install semgrep`
- **git** (required when scanning a GitHub URL):  
  used to clone repos; usually already installed.

**Optional:**

- **Docker** — used for sandbox execution. If Docker is not available, use `--no-sandbox` for static-only scanning.

---

## How to use

### 1. Install SafeHub

**Option A — From ClawHub (recommended):**

```bash
npm install -g clawhub
clawhub login
clawhub install safehub
```

SafeHub is installed into `./skills/safehub` (or your configured skills dir). Run it with Node:

```bash
node ./skills/safehub/index.js scan web-scraper
node ./skills/safehub/index.js scan ./my-local-skill --no-sandbox
node ./skills/safehub/index.js report web-scraper
node ./skills/safehub/index.js update
```

**Option B — Global CLI via npm:**

```bash
npm install -g safehub
```

Then from anywhere:

```bash
safehub scan web-scraper
safehub scan ./my-local-skill
safehub scan https://github.com/someone/their-skill
safehub report web-scraper
safehub update
```

**Option C — Local development:**

```bash
git clone https://github.com/sumeetghimire/safehub.git && cd safehub
npm install
npm link
safehub scan ./test-fixtures/risky-skill --no-sandbox
```

### 2. Run a scan

Replace `<target>` with a ClawHub skill name, a local path, or a GitHub URL (no angle brackets):

```bash
safehub scan web-scraper
safehub scan .
safehub scan ./some-skill
safehub scan https://github.com/user/repo
```

Use `--no-sandbox` to skip Docker and run static analysis only:

```bash
safehub scan https://github.com/user/repo --no-sandbox
```

### 3. View last report or update rules

```bash
safehub report <skill-name>
safehub update
```

---

## Commands

### Scan a skill

Scan a skill by **name** (from ClawHub), **local path**, or **GitHub URL**:

```bash
safehub scan web-scraper
safehub scan ./my-local-skill
safehub scan https://github.com/someone/their-skill
```

To skip Docker and run only static analysis (e.g. if Docker is not installed):

```bash
safehub scan ./my-local-skill --no-sandbox
```

**Example output:**

```
Scanning web-scraper v1.2.0...
─────────────────────────────
STATIC ANALYSIS:
✅ No outbound network calls detected
✅ No filesystem writes outside /tmp
⚠️  process.env access in index.js line 18
❌ eval() call in utils.js line 7

SANDBOX BEHAVIOR:
✅ No network connections attempted
✅ No suspicious syscalls
⚠️  Attempted to read /etc/passwd

TRUST SCORE: 42/100 ❌ NOT SAFE TO INSTALL
─────────────────────────────
RECOMMENDATION: Do not install this skill.
3 issues found. See full report above.
```

### Show last report

Show the last scan report for a skill without rescanning:

```bash
safehub report web-scraper
```

### Update scanner rules

Download the latest Semgrep rules from the SafeHub repo (or your fork):

```bash
safehub update
```

See [Environment variables](#environment-variables) below for `SAFEHUB_RULES_REPO`, `SAFEHUB_RULES_BRANCH`, and other options.

---

## Environment variables

All are optional. No secrets or API tokens are required by default.

| Variable | Default | Effect |
|----------|---------|--------|
| **SAFEHUB_RULES_REPO** | `safehub/safehub` | GitHub repo (owner/repo) used by `safehub update`. The updater **fetches and overwrites** local rule files in `./rules` from this repo. Only set this to a repo you trust. |
| **SAFEHUB_RULES_BRANCH** | `main` | Branch used when fetching rules. |
| **SAFEHUB_DATA_DIR** | `~/.safehub` | Directory for cached scan reports. |
| **SAFEHUB_SANDBOX_IMAGE** | `node:18-alpine` | Docker image for the sandbox. |
| **SAFEHUB_SANDBOX_TIMEOUT_MS** | `30000` | Sandbox timeout in milliseconds. |
| **SAFEHUB_NO_TYPING** | (unset) | Set to `1` to disable typing-effect output (e.g. CI/pipes). |

**Important:** `SAFEHUB_RULES_REPO` controls where rules are downloaded from and overwrites local `./rules`; only point it at a trusted repo.

---

## How to release

Use this flow to cut a new version and publish it to GitHub and ClawHub.

### 1. Bump version

Set the new version (e.g. `1.0.2`) in all of:

- `package.json` → `"version": "1.0.2"`
- `SKILL.md` → frontmatter `version: 1.0.2`
- `clawhub.json` → `"version": "1.0.2"`
- `skill.json` → `"version": "1.0.2"`

### 2. Commit and push

```bash
git add package.json SKILL.md clawhub.json skill.json
git commit -m "chore: release 1.0.2"
git push origin main
```

### 3. Create and push a git tag

```bash
git tag v1.0.2
git push origin v1.0.2
```

Use the same version as above (e.g. `v1.0.2` for version `1.0.2`).

### 4. Publish to ClawHub

```bash
npm install -g clawhub
clawhub login
clawhub publish . --slug safehub --name "SafeHub" --version 1.0.2 --changelog "Short description of changes" --tags latest
```

Replace `1.0.2` and the changelog text with your release version and notes.

### First-time ClawHub setup

- Sign up at [clawhub.ai](https://clawhub.ai) → Developer Account, verify email (GitHub account at least one week old).
- Add 3–5 screenshots in `screenshots/` (1920×1080 or 1280×720 PNG) if the listing asks for them.

---

## Contributing

We welcome contributions, especially **new Semgrep rules** to improve detection.

- **[CONTRIBUTING.md](CONTRIBUTING.md)** — How to add and test new rules, and the pull request process.
- **[/rules](rules/)** — Semgrep rule files. Add or edit `.yml` files here and open a PR.

---

## Implementation status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Folder structure, README, LICENSE, skill.json, package.json | Done |
| 2 | Static scanner (Semgrep) + 5 rule files (network, filesystem, obfuscation, execution, env) | Done |
| 3 | Docker sandbox (no network, read-only root, limits) | Done |
| 4 | Trust score calculator (0–100, SAFE / CAUTION / NOT SAFE) | Done |
| 5 | Commands wired: scan pipeline, report formatter, cached reports in `~/.safehub/reports` | Done |
| 6 | Update command: pull latest rules from GitHub (`SAFEHUB_RULES_REPO`) | Done |

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).
