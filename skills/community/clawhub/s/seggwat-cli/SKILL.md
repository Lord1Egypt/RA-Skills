---
name: seggwat-cli
description: Use the SeggWat CLI to manage feedback, projects, and ratings from the terminal. Trigger this skill whenever the user wants to collect, triage, query, or automate user feedback using the `seggwat` command-line tool. Also trigger when the user mentions SeggWat, feedback widgets, NPS scores, star ratings, helpful ratings, or wants to integrate feedback collection into CI/CD pipelines or developer workflows. This includes installation, authentication, CRUD operations on feedback and ratings, querying statistics, and scripting with JSON output.
---

# SeggWat CLI

The SeggWat CLI (`seggwat`) lets you manage feedback, projects, and ratings for the [SeggWat](https://seggwat.com) feedback platform directly from the terminal.

## Installation

```bash
cargo install seggwat-cli
```

A shell-based installer is also available at `https://seggwat.com/static/install.sh` (supports pinning a version via `VERSION=v0.17.2`).

Verify: `seggwat --version`

## Authentication

Two methods are available. Use API key for scripts/CI, OAuth for interactive use.

### API Key (non-interactive, recommended for automation)

```bash
# Environment variable
export SEGGWAT_API_KEY=oat_<your-token>

# Or inline flag
seggwat --api-key oat_<your-token> project list
```

API keys use the `oat_` prefix (Organization Access Token) and are created in the SeggWat Dashboard under Settings > API Tokens.

### OAuth Login (interactive)

```bash
seggwat login          # Opens browser, caches tokens at ~/.config/seggwat/tokens.json
seggwat whoami         # Show current user
seggwat logout         # Clear cached tokens
```

For self-hosted instances, pass `--api-url`, `--zitadel-domain`, and `--client-id` to point at your own deployment.

## Global Options

| Flag | Env Variable | Description |
|------|-------------|-------------|
| `--api-url <url>` | `SEGGWAT_API_URL` | API base URL (default: `https://seggwat.com`) |
| `--api-key <key>` | `SEGGWAT_API_KEY` | API key for authentication |
| `--json` | — | Output as JSON instead of tables |
| `-v, --verbose` | — | Enable debug logging |

## Commands Reference

### Projects

```bash
seggwat project list                    # List all projects (alias: p ls)
seggwat project get <id>                # Get project details
seggwat project summary <id>            # Project overview with feedback & rating stats
```

### Feedback

**CRUD operations:**

```bash
# List (with optional filters and pagination)
seggwat feedback list <project-id> [--status <status>] [--type <type>] [--search <text>] [--page N] [--limit N]

# Get single item
seggwat feedback get <project-id> <feedback-id>

# Create
seggwat feedback create <project-id> --message "text" [--type bug|feature|praise|question|improvement|other] [--path /page] [--version 1.0.0]

# Update
seggwat feedback update <project-id> <feedback-id> [--message "text"] [--type <type>] [--status <status>] [--resolution-note "text"]

# Delete (archive)
seggwat feedback delete <project-id> <feedback-id>

# Statistics
seggwat feedback stats <project-id>
```

**Feedback statuses:** `new`, `active`, `assigned`, `hold`, `closed`, `resolved`

**Feedback types:** `bug`, `feature`, `praise`, `question`, `improvement`, `other`

**Aliases:** `feedback` → `fb`, `list` → `ls`, `delete` → `rm`

### Ratings

```bash
# List (with optional filters)
seggwat rating list <project-id> [--type helpful|star|nps] [--path /page] [--page N] [--limit N]

# Get single rating
seggwat rating get <project-id> <rating-id>

# Delete (archive)
seggwat rating delete <project-id> <rating-id>

# Statistics (type defaults to helpful)
seggwat rating stats <project-id> --type helpful   # Thumbs up/down percentage
seggwat rating stats <project-id> --type star      # Star distribution & average
seggwat rating stats <project-id> --type nps       # NPS score, promoters/passives/detractors
```

**Rating types:**
- `helpful` — binary thumbs up/down (value: true/false)
- `star` — 1-5 star rating (value + max_stars)
- `nps` — Net Promoter Score 0-10 (promoters 9-10, passives 7-8, detractors 0-6)

**Aliases:** `rating` → `r`, `list` → `ls`, `delete` → `rm`

### Shell Completions

```bash
seggwat completions bash > ~/.local/share/bash-completion/completions/seggwat
seggwat completions zsh > ~/.zfunc/_seggwat
seggwat completions fish > ~/.config/fish/completions/seggwat.fish
```

## JSON Output & Scripting

Add `--json` to any command for machine-readable output, useful for piping to `jq` or other tools:

```bash
# List project IDs
seggwat project list --json | jq -r '.projects[].id'

# Count open bugs
seggwat feedback list PROJECT_ID --type bug --status new --json | jq '.feedback | length'

# Export all feedback
seggwat feedback list PROJECT_ID --limit 100 --json > feedback.json

# Get NPS score
seggwat rating stats PROJECT_ID --type nps --json | jq '.score'

# Find feedback containing a keyword
seggwat feedback list PROJECT_ID --search "login" --json | jq '.feedback[].message'
```

## Common Workflows

### Triage new feedback

```bash
# See what's new
seggwat feedback list PROJECT_ID --status new

# Review and update status
seggwat feedback update PROJECT_ID FEEDBACK_ID --status active
seggwat feedback update PROJECT_ID FEEDBACK_ID --status resolved --resolution-note "Fixed in v2.1"
```

### Monitor rating health

```bash
# Quick health check
seggwat rating stats PROJECT_ID --type helpful
seggwat rating stats PROJECT_ID --type nps

# Check specific page performance
seggwat rating list PROJECT_ID --type star --path "/pricing"
```

### CI/CD integration

```bash
# In your pipeline, create feedback from test results
export SEGGWAT_API_KEY=oat_<your-token>
seggwat feedback create PROJECT_ID \
  --message "E2E test failure: checkout flow" \
  --type bug \
  --version "$(git describe --tags)"
```
