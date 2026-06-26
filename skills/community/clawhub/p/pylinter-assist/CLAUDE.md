# pylinter-assist — OpenClaw Skill

## Skill: `/lint-review`

A soft PR reviewer that combines Pylint with context-aware pattern heuristics to catch
things traditional linters miss. Complements hard CI tests; branches are assignable by
the user.

---

### Invocation

```
/lint-review [TARGET] [OPTIONS]
```

**TARGET** (optional, default: current staged changes)
- `pr <number>` — lint all files changed in a GitHub PR
- `staged` — lint git-staged files
- `diff <file>` — lint files from a unified diff file
- `files <path>...` — lint explicit files or directories

**OPTIONS**
| Flag | Description |
|------|-------------|
| `--format text\|json\|markdown` | Output format (default: markdown) |
| `--config <path>` | Custom `.linting-rules.yml` path |
| `--post-comment` / `--no-post-comment` | Post result as GitHub PR comment |
| `--fail-on-warning` | Also fail on warnings (default: errors only) |

---

### What it checks

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

---

### Usage examples

```bash
# Create venv, install dependencies and CLI
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Lint PR #42 and post a comment
lint-pr pr 42 --post-comment

# Lint staged changes
lint-pr staged

# Lint a diff file
lint-pr diff /tmp/changes.diff

# Lint specific files
lint-pr files src/ tests/

# Use custom rules
lint-pr files src/ --config .linting-rules.yml
```

---

### Configuration

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

---

### Triggering the GitHub Action as an agent

The `lint-pr.yml` workflow supports `workflow_dispatch`, so it can be triggered
programmatically via the GitHub CLI or API:

**Via GitHub CLI:**
```bash
gh workflow run lint-pr.yml \
  -f pr_number=42 \
  -f format=markdown \
  -f post_comment=true
```

**Via REST API:**

> **Security note:** Never hard-code the token value; always expand it from an environment
> variable. The token must be scoped to `actions:write` for the target repository.

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/lint-pr.yml/dispatches \
  -d '{"ref":"main","inputs":{"pr_number":"42","format":"markdown","post_comment":"true"}}'
```

### Enabling a new project for support

To enable a new project for pylinter-assist support, follow these steps on the `dev` branch.
**Review each downloaded file before committing** — GitHub Actions workflows run with
repository permissions and can access secrets.

```bash
cd <your-project-root>
git checkout dev
git pull origin dev

mkdir -p .github/workflows

# 1. Download files
curl -o .github/workflows/lint-pr.yml \
  https://raw.githubusercontent.com/claytantor/pylinter-assist/main/.github/workflows/lint-pr.yml

curl -o .linting-rules.yml \
  https://raw.githubusercontent.com/claytantor/pylinter-assist/main/.linting-rules.yml

# 2. Review before committing (required — do not skip)
cat .github/workflows/lint-pr.yml
cat .linting-rules.yml

# 3. Commit only after review
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

---

### GitHub Actions Monitoring

The skill can monitor workflow runs and notify when lint results are ready:

> **Security note:** Avoid embedding secret values (bot tokens, webhook URLs) directly in
> `--callback` arguments — they appear in process listings. Use environment variables
> in the argument value (e.g. `$TELEGRAM_BOT_TOKEN`) or configure channels in
> `.linting-rules.yml` instead.

```bash
# Monitor a repository's workflow runs
lint-pr monitor owner/repo --token $GITHUB_TOKEN --callback telegram:$TELEGRAM_BOT_TOKEN:$TELEGRAM_CHAT_ID

# Configuration in .linting-rules.yml:
github_actions:
  polling_interval: 30    # seconds between checks
  max_timeout: 1800       # max wait time (seconds)

notifications:
  enabled: true
  channels:
    - type: telegram
      bot_token: $TELEGRAM_BOT_TOKEN
      chat_id: 123456
    - type: discord
      webhook_url: $DISCORD_WEBHOOK_URL
```

---

### Extending with custom checks

Implement the `PatternCheck` protocol in `pylinter_assist/checks/`:

```python
from pylinter_assist.checks.base import CheckResult, PatternCheck, Severity
from dataclasses import dataclass

@dataclass
class MyCustomCheck:
    name: str = "my-check"
    enabled: bool = True

    def check(self, file_path: str, source: str, config: dict) -> list[CheckResult]:
        results = []
        # ... your logic here ...
        return results
```

Register it in `pylinter_assist/linter.py` → `Linter.__init__` → `self._pattern_checks`.

---

### Project layout

```
pylinter-assist/
├── pylinter_assist/
│   ├── checks/
│   │   ├── base.py          # PatternCheck protocol + CheckResult + Severity
│   │   ├── secrets.py       # HCS001–HCS005 hardcoded secrets/URLs/IPs
│   │   ├── fastapi.py       # FAD001 FastAPI missing docstrings
│   │   └── react.py         # RUE001–RUE002 React useEffect deps
│   ├── linter.py            # Orchestrator: pylint + pattern checks
│   ├── reporter.py          # text / JSON / Markdown rendering
│   ├── config.py            # .linting-rules.yml loader with defaults
│   └── cli.py               # Click CLI (pr / staged / diff / files)
├── scripts/
│   └── lint_pr.py           # convenience entry point (activate venv first)
├── .github/workflows/
│   └── lint-pr.yml          # GitHub Actions using actions/setup-python
├── .python-version          # Python version pin for pyenv / actions/setup-python
├── .linting-rules.yml       # Default configuration
├── .gitignore
└── pyproject.toml           # standard pyproject (pip-installable)
```
