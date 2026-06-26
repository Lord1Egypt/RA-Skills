# pylinter-assist — OpenClaw Skill

name: pylinter-assist
version: 0.6.3

## Prerequisites

Before installing this skill, ensure you have the following installed:

### Python (via pyenv or system package manager)

This project uses standard **pyenv + pip + venv** — no remote install scripts required.

**Install pyenv (no `curl | sh`):**

```bash
# macOS
brew install pyenv

# Linux — auditable git clone (can be pinned to a specific commit)
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# Then follow https://github.com/pyenv/pyenv#set-up-your-shell-environment
```

**Install Python 3.11 and activate:**

```bash
pyenv install 3.11    # reads .python-version automatically if present
pyenv local 3.11      # creates .python-version in the project root
```

Alternatively, use any system Python 3.11+ (`python3 --version`) — pyenv is optional if you already have a suitable Python.

### npm (Node.js package manager, for ClawHub CLI)

```bash
# macOS/Linux
brew install node  # or your preferred package manager

# Or download from https://nodejs.org/
```

### clawhub CLI (OpenClaw skill installer)

```bash
npm i -g clawhub
```

## Description

Context-aware Python linting with smart pattern heuristics for PR review.
Automatically integrates into GitHub workflows to lint pull requests and provide feedback.

## Features

- Combines Pylint with custom pattern checks (hardcoded secrets, missing docstrings, etc.)
- Auto-lints PRs when integrated via GitHub Actions
- Supports multiple output formats (markdown, text, json)
- Configurable rules via `.linting-rules.yml`

## Installation via ClawHub

Install the skill using the ClawHub CLI:

```bash
clawhub install pylinter-assist
```

The skill will be installed to `~/.openclaw/workspace/skills/pylinter-assist`.

## Integration Steps

### Step 0: Post-Installation Setup

After the skill is installed as a snapshot, create a venv and install the CLI:

```bash
cd ~/.openclaw/workspace/skills/pylinter-assist
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

This registers the `lint-pr` command for the duration of your shell session.
Deactivate when done: `deactivate`

### Step 1: Use the CLI

```bash
# Create and activate the virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the package and its dependencies
pip install -e .

# Run the linter
lint-pr pr 42 --post-comment
```

Or run the wrapper script directly (no venv activation needed if dependencies are installed):
```bash
python scripts/lint_pr.py pr 42 --post-comment
```

### Step 2: Add GitHub Actions Workflow

> **Security warning:** GitHub Actions workflows run with your repository's permissions
> and can read secrets. Only commit a workflow file whose full contents you have read
> and understood. Never copy a file from a URL without inspecting it first.

**Recommended — copy from a local clone** (you can `git log` and `git show` the file
before copying; no network fetch at commit time):

```bash
git clone https://github.com/claytantor/pylinter-assist.git /tmp/pylinter-assist
# Review the workflow source before copying
cat /tmp/pylinter-assist/.github/workflows/lint-pr.yml

mkdir -p .github/workflows
cp /tmp/pylinter-assist/.github/workflows/lint-pr.yml .github/workflows/
```

**Last resort — direct download.** Pin to a specific commit SHA, not `main`, so the
file cannot change under you. Replace `<COMMIT_SHA>` with the exact commit you reviewed
on GitHub:

```bash
# Find the commit SHA: https://github.com/claytantor/pylinter-assist/commits/main
COMMIT_SHA=<COMMIT_SHA>

mkdir -p .github/workflows
curl -o .github/workflows/lint-pr.yml \
  "https://raw.githubusercontent.com/claytantor/pylinter-assist/${COMMIT_SHA}/.github/workflows/lint-pr.yml"

# Verify the download — compare against what you saw on GitHub
cat .github/workflows/lint-pr.yml
sha256sum .github/workflows/lint-pr.yml   # record this for future reference
```

### Step 3: Add Configuration (Optional)

Copy and customize the rules file:

```bash
cp /path/to/pylinter-assist/.linting-rules.yml .linting-rules.yml
```

### Step 4: Set Repository Permissions

Ensure your repository has these permissions enabled:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### Step 5: Commit and Push

The workflow will automatically trigger on new PRs.

## Enabling a New Project for Support

> **Security warning:** The workflow file you are about to commit runs with your
> repository's permissions and can access secrets. Read every line of the file before
> committing. Do not use `curl … | sh` or copy files from a branch tip (`main`) without
> pinning to a reviewed commit.

**Recommended approach — clone, review, then copy:**

```bash
# 1. Clone the skill repo to a temporary location
git clone https://github.com/claytantor/pylinter-assist.git /tmp/pylinter-assist

# 2. Review the files you are about to add to your repo
cat /tmp/pylinter-assist/.github/workflows/lint-pr.yml
cat /tmp/pylinter-assist/.linting-rules.yml

# 3. Switch to your project and copy the reviewed files
cd <your-project-root>
git checkout dev
git pull origin dev

mkdir -p .github/workflows
cp /tmp/pylinter-assist/.github/workflows/lint-pr.yml .github/workflows/
cp /tmp/pylinter-assist/.linting-rules.yml .linting-rules.yml

# 4. Commit only after you are satisfied with the contents
git add .github/workflows/lint-pr.yml .linting-rules.yml
git commit -m "ci: add pylinter-assist workflow for PRs targeting dev"
git push origin dev
```

The workflow requires these permissions in your repository settings:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

## Usage

```bash
# Activate venv first
source .venv/bin/activate

lint-pr [TARGET] [OPTIONS]
```

### Targets

| Target | Description |
|--------|-------------|
| `pr <number>` | Lint all files changed in a GitHub PR |
| `staged` | Lint git-staged files |
| `diff <file>` | Lint files from a unified diff file |
| `files <path>...` | Lint explicit files or directories |

### Examples

```bash
# Activate venv
source .venv/bin/activate

# Lint PR #42 and post comment
lint-pr pr 42 --post-comment

# Lint staged changes
lint-pr staged

# Lint a diff file
lint-pr diff /tmp/changes.diff

# Lint specific files
lint-pr files src/ tests/
```

### Options

| Flag | Description |
|------|-------------|
| `--format text\|json\|markdown` | Output format (default: markdown) |
| `--config <path>` | Custom `.linting-rules.yml` path |
| `--post-comment` / `--no-post-comment` | Post result as GitHub PR comment |
| `--fail-on-warning` | Also fail on warnings (default: errors only) |

## Checks Performed

| Check | Code | Severity | Catches |
|-------|------|----------|---------|
| Pylint | C/W/R/E/F | varies | Standard Python quality issues |
| Hardcoded password/secret | HCS001 | ERROR | `password = "abc123"` |
| Credentials in URL | HCS002 | ERROR | `https://user:pass@host` |
| Hardcoded IP address | HCS003 | ERROR | `HOST = "10.0.0.5"` |
| Hardcoded localhost URL | HCS004 | ERROR | `"http://localhost:8000"` |
| AWS/GCP access key | HCS005 | ERROR | `AKIAIOSFODNN7EXAMPLE` |
| FastAPI missing docstring | FAD001 | WARNING | `@router.get("/")` without docstring |
| useEffect missing deps | RUE001 | WARNING | React useEffect with no deps array |
| useEffect suspicious deps | RUE002 | INFO | useEffect referencing outer vars |

## Configuration

Copy `.linting-rules.yml` to your project root and customize:

```yaml
pylint:
  enabled: true
  disable: [C0114, C0115]   # suppress module/class docstring warnings

hardcoded_secrets:
  enabled: true
  skip_ip_check: false

fastapi_docstring:
  severity: warning

react_useeffect_deps:
  severity: warning

github:
  post_comment: true
  fail_on_error: true
  fail_on_warning: false
```

## Workflow Triggers

- **pull_request**: Auto-lints all files changed in a PR
- **workflow_dispatch**: Manual trigger via GitHub UI or API

## Manual Trigger Examples

**GitHub CLI (preferred — token is handled by `gh auth`, not exposed in shell):**
```bash
gh workflow run lint-pr.yml -f pr_number=42 -f format=markdown -f post_comment=true
```

**REST API:**
> **Security note:** The token passed via `-H "Authorization: token $GITHUB_TOKEN"` must
> be a Personal Access Token or a fine-grained token scoped to `actions:write`. Never
> hard-code the token value in scripts; always expand it from an environment variable.

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/lint-pr.yml/dispatches \
  -d '{"ref":"main","inputs":{"pr_number":"42","format":"markdown","post_comment":"true"}}'
```

## Output

- Markdown reports posted as PR comments (when enabled)
- JSON artifacts uploaded for 14 days retention
- Exit code 1 if errors found (when `fail_on_error: true`)

## Troubleshooting

### `command not found: lint-pr` after installation

The `lint-pr` CLI is installed inside the virtual environment. Either activate it or call it directly:

```bash
# Activate the venv
source .venv/bin/activate

# Or call it directly without activation
./.venv/bin/lint-pr pr 42
```

### `python3: command not found` or wrong Python version

Ensure Python 3.11+ is installed and on your PATH:

```bash
python3 --version

# If using pyenv, install the required version
pyenv install    # reads .python-version automatically
pyenv versions   # list installed versions
```

### `pip install -e .` fails

Ensure the venv is activated before installing:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## GitHub Actions Monitoring

The skill can automatically monitor GitHub Actions workflow runs and notify you when lint results are ready.

### Monitor a Repository

Use the `monitor` command to watch for completed workflow runs:

```bash
# Basic monitoring - download report only
lint-pr monitor owner/repo --token $GITHUB_TOKEN

# Monitor with timeout and custom polling interval
lint-pr monitor owner/repo --token $GITHUB_TOKEN --timeout 3600 --poll-interval 60
```

> **Security note:** Avoid passing secrets (bot tokens, webhook URLs) directly as
> `--callback` command-line arguments — they are visible in process listings (`ps aux`).
> Prefer setting notification credentials in `.linting-rules.yml` with values read from
> environment variables, or ensure your shell history is protected before using the
> `--callback` flag.

```bash
# Monitor with Telegram notification (tokens visible in process list — use with caution)
lint-pr monitor owner/repo --token $GITHUB_TOKEN \
  --callback telegram:$TELEGRAM_BOT_TOKEN:$TELEGRAM_CHAT_ID

# Monitor with Discord notification
lint-pr monitor owner/repo --token $GITHUB_TOKEN \
  --callback discord:$DISCORD_WEBHOOK_URL

# Monitor with multiple channels
lint-pr monitor owner/repo --token $GITHUB_TOKEN \
  --callback telegram:$TELEGRAM_BOT_TOKEN:$TELEGRAM_CHAT_ID \
  --callback discord:$DISCORD_WEBHOOK_URL
```

### Configuration

Enable notifications in `.linting-rules.yml`:

```yaml
notifications:
  enabled: true
  channels:
    - type: telegram
      bot_token: $TELEGRAM_BOT_TOKEN
      chat_id: 123456789
    - type: discord
      webhook_url: https://discord.com/api/webhooks/...
      username: "Lint Bot"
    - type: slack
      webhook_url: https://hooks.slack.com/services/...
```

### Monitoring Configuration

```yaml
github_actions:
  polling_interval: 30    # Seconds between status checks
  max_timeout: 1800       # Max seconds to wait (30 minutes)
  retry_attempts: 3       # Retry failed API calls
```

### Supported Notification Channels

| Channel | Setup |
|---------|-------|
| Telegram | Create bot via @BotFather, get chat_id from bot |
| Discord | Create webhook in channel settings |
| Slack | Create incoming webhook in apps |
| Email | Configure SMTP server credentials |

### Error Handling

The monitoring system handles:
- **API rate limiting** (429): Exponential backoff with `Retry-After` header
- **Missing artifacts**: Retry 3x with 10s delay, then fail gracefully
- **Network timeouts**: Retry up to 3 attempts with increasing timeout
- **Invalid tokens**: Clear error message with validation hint

### Workflow Integration

When enabled in a repository, the workflow automatically:
1. Runs lint on PRs or manual trigger
2. Uploads `lint-report.json` as artifact
3. Can be monitored externally via the `monitor` command
4. Sends notifications when results are ready

See [Enabling a New Project for Support](#enabling-a-new-project-for-support) to set up monitoring in your repository.
```

