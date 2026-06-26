# pylinter-assist

Context-aware Python linting with smart pattern heuristics for PR review.

A soft PR reviewer that combines Pylint with custom pattern checks to catch hardcoded secrets, missing FastAPI docstrings, and other issues traditional linters miss. Complements hard CI tests; branches are assignable by the user.

## Quick Start

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the CLI and dependencies
pip install -e .

# Lint your project
lint-pr files src/ --format markdown
```

Requires Python 3.11+. Install via [pyenv](https://github.com/pyenv/pyenv) (`brew install pyenv` on macOS, `git clone` on Linux) or any system Python 3.11+.

## GitHub Actions (Recommended for PRs)

Automatically lint PRs by adding the workflow to your repository. **Review the file before committing** — it runs with repository permissions.

```bash
# Clone to a temp location and inspect the workflow
git clone https://github.com/claytantor/pylinter-assist.git /tmp/pylinter-assist
cat /tmp/pylinter-assist/.github/workflows/lint-pr.yml

# Copy only after reviewing
mkdir -p .github/workflows
cp /tmp/pylinter-assist/.github/workflows/lint-pr.yml .github/workflows/
```

See [GitHub Actions Integration](#github-actions-integration) for full setup instructions.

## Features

| Check | Code | Severity | Catches |
|-------|------|----------|---------|
| Pylint | C/W/R/E/F | varies | Standard Python quality issues |
| Hardcoded password/secret | HCS001 | ERROR | `password = "abc123"` |
| Credentials in URL | HCS002 | ERROR | `https://user:pass@host` |
| Hardcoded IP address | HCS003 | ERROR | `HOST = "10.0.0.5"` |
| Hardcoded localhost URL | HCS004 | ERROR | `"http://localhost:8000"` |
| AWS/GCP access key | HCS005 | ERROR | `AKIAIOSFODNN7EXAMPLE` |
| FastAPI missing docstring | FAD001 | WARNING | `@router.get("/")` without docstring |
| useEffect missing deps | RUE001 | WARNING | `useEffect(() => { ... })` with no `[]` |
| useEffect suspicious deps | RUE002 | INFO | `useEffect(..., [])` references outer vars |

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install CLI and runtime dependencies
pip install -e .

# For development (includes pytest, ruff)
pip install -e .[dev]
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

### Options

| Flag | Description |
|------|-------------|
| `--format text\|json\|markdown` | Output format (default: markdown) |
| `--config <path>` | Custom `.linting-rules.yml` path |
| `--post-comment` / `--no-post-comment` | Post result as GitHub PR comment |
| `--fail-on-warning` | Also fail on warnings (default: errors only) |

### Examples

```bash
# Lint PR #42 and post a comment
lint-pr pr 42 --post-comment

# Lint staged files before commit
lint-pr staged

# Lint a diff file
lint-pr diff /tmp/changes.diff

# Lint specific files
lint-pr files src/ tests/

# Use custom rules
lint-pr files src/ --config .linting-rules.yml
```

## Configuration

Copy `.linting-rules.yml` to your project root and edit:

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

## Publishing to ClawHub

```bash
# Activate venv
source .venv/bin/activate

# Publish the skill
make publish

# Auto-increment minor version and publish
make publish-bump

# Dry run before publishing
make publish-dry-run
```

## Development

```bash
# Activate venv and install dev dependencies
source .venv/bin/activate
pip install -e .[dev]

# Run tests
pytest

# Format code
ruff format .

# Lint code
pylint pylinter_assist
```

## GitHub Actions Integration

Automatically lint PRs in your project using the provided GitHub Actions workflow.

### Setup

1. **Clone and review the workflow file** (do not use `curl` from the `main` branch)

   ```bash
   git clone https://github.com/claytantor/pylinter-assist.git /tmp/pylinter-assist
   cat /tmp/pylinter-assist/.github/workflows/lint-pr.yml   # review before copying
   mkdir -p .github/workflows
   cp /tmp/pylinter-assist/.github/workflows/lint-pr.yml .github/workflows/
   ```

2. **Add configuration file** (optional)

   ```bash
   cp /tmp/pylinter-assist/.linting-rules.yml .linting-rules.yml
   ```

3. **Commit and push**

   The workflow will automatically trigger on PRs.

### Workflow Triggers

| Trigger | Description |
|---------|-------------|
| `pull_request` | Auto-lints all files changed in a PR |
| `workflow_dispatch` | Manual trigger via GitHub UI or API |

### Manual Trigger via GitHub CLI

```bash
gh workflow run lint-pr.yml \
  -f pr_number=42 \
  -f format=markdown \
  -f post_comment=true
```

### Manual Trigger via API

> Never hard-code the token value — always expand it from an environment variable.

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/lint-pr.yml/dispatches \
  -d '{"ref":"main","inputs":{"pr_number":"42","format":"markdown","post_comment":"true"}}'
```

### Workflow Permissions

The workflow requires these permissions:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### Output Artifacts

Every run generates a `lint-report.json` artifact available for 14 days.

## License

MIT
