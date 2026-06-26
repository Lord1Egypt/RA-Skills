---
name: reporead
version: 1.1.0
description: Analyze GitHub repositories using RepoRead AI. Use when the user asks to "analyze a repo", "generate docs", "security audit a repo", "create a README", or wants AI-powered repository analysis. Supports MCP server integration and REST API.
metadata:
  clawdis:
    primaryEnv: REPOREAD_API_KEY
    homepage: https://www.reporead.com
    requires:
      env:
        - REPOREAD_API_KEY
      anyBins:
        - curl
    config:
      requiredEnv:
        - REPOREAD_API_KEY
---

# RepoRead — AI Repository Analysis

RepoRead is an AI-powered platform that analyzes GitHub repositories and generates documentation, technical architecture breakdowns, security audits, visual diagrams, and LLM-optimized summaries. Connect via the MCP server (preferred) or REST API to analyze any public GitHub repository.

## Quick Start

### 1. Get an API Key

Sign up at [reporead.com](https://www.reporead.com) and create an API key at [reporead.com/settings](https://www.reporead.com/settings). Keys use the `rrk_` prefix.

### 2. Set the Environment Variable

```bash
export REPOREAD_API_KEY="rrk_your_api_key_here"
```

Add to your shell profile (`~/.zshrc`, `~/.bashrc`) to persist across sessions.

### 3. Verify Connection

```bash
bash {baseDir}/scripts/check-connection.sh
```

This confirms your API key is valid and shows your current token balance.

### 4. Connect the MCP Server (Recommended)

Add to your MCP configuration (e.g. `claude_desktop_config.json`, `.mcp.json`):

```json
{
  "mcpServers": {
    "reporead": {
      "type": "streamable-http",
      "url": "https://api.reporead.com/mcp",
      "headers": {
        "Authorization": "Bearer rrk_your_api_key_here"
      }
    }
  }
}
```

Replace `rrk_your_api_key_here` with your actual API key.

## MCP Tools

When the MCP server is connected, these tools are available:

| Tool | Description |
|------|-------------|
| `import_repository(github_url)` | Import a GitHub repo by URL |
| `list_repositories(page?, per_page?)` | List imported repos |
| `get_repository(repository_id)` | Get repo details by ID |
| `start_analysis(repository_id, analysis_type, branch?)` | Queue an analysis job |
| `list_analyses(page?, per_page?, repository_id?, status?, analysis_type?)` | List jobs with filters |
| `get_analysis(analysis_id)` | Get full analysis results |
| `get_analysis_status(analysis_id)` | Lightweight status poll |
| `get_token_balance()` | Check available tokens and tier |

## REST API Fallback

If the MCP server is not configured, use the REST API helper script:

```bash
# Check token balance
bash {baseDir}/scripts/reporead-api.sh balance

# Import a repository
bash {baseDir}/scripts/reporead-api.sh import https://github.com/owner/repo

# Start an analysis
bash {baseDir}/scripts/reporead-api.sh analyze <repository_id> technical

# Check analysis status
bash {baseDir}/scripts/reporead-api.sh status <analysis_id>

# Get full analysis results
bash {baseDir}/scripts/reporead-api.sh results <analysis_id>

# List repositories
bash {baseDir}/scripts/reporead-api.sh repos
```

Or call the REST API directly:

**Base URL:** `https://api.reporead.com/public/v1`
**Auth:** `Authorization: Bearer $REPOREAD_API_KEY`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/repositories` | `POST` | Import repo `{"github_url": "..."}` |
| `/repositories` | `GET` | List repos `?page=1&per_page=20` |
| `/repositories/{id}` | `GET` | Get repo details |
| `/analyses` | `POST` | Start analysis `{"repository_id": "...", "analysis_type": "..."}` |
| `/analyses` | `GET` | List analyses `?repository_id=...&status=...` |
| `/analyses/{id}` | `GET` | Get full results |
| `/analyses/{id}/status` | `GET` | Lightweight status check |
| `/tokens/balance` | `GET` | Check token balance |

---

## Choosing an Analysis Type

| Context | Type | What You Get |
|---------|------|--------------|
| New to a codebase, need orientation | `technical` | Architecture, patterns, key components |
| Need to create or update documentation | `readme` | Full README documentation |
| Pre-deploy, PR review, or security audit | `security` | Vulnerability analysis, risk assessment |
| Need visual architecture diagrams | `mermaid` | Workflow and system diagrams |
| Building AI tools that consume repo context | `llmstxt` | LLM-optimized summary |

**Default:** Use `technical` if unsure.
**Full docs:** Combine `readme` + `mermaid`.
**Free tier:** `readme` and `llmstxt` only. Paid tiers unlock all types.

---

## Workflow

1. **Check balance** — `get_token_balance()` to verify sufficient tokens
2. **Check if already imported** — `list_repositories()` to avoid duplicates
3. **Import the repo** — `import_repository(github_url)` — save the returned `id`
4. **Start analysis** — `start_analysis(repository_id, analysis_type)` — save the returned `id`
5. **Poll for completion** — `get_analysis_status(analysis_id)` every 10 seconds until `status` is `completed` or `failed`
6. **Fetch results** — `get_analysis(analysis_id)` — the `results` field contains the full output
7. **Use the results** as context for the user's task

---

## Common Patterns

### Understand a Codebase Before Working on It

When the user says "explain this repo" or you need context before coding:

1. Import the repo
2. Run `start_analysis(repo_id, "technical")`
3. Poll until completed
4. Use the architecture breakdown, key patterns, and component descriptions as working context

### Generate Documentation

When the user wants a README, docs, or visual diagrams:

1. Import the repo
2. Run both in parallel:
   - `start_analysis(repo_id, "readme")`
   - `start_analysis(repo_id, "mermaid")`
3. Poll both until completed
4. Combine the README content with the visual diagrams

### Security Check Before Deploy

When reviewing a repo for vulnerabilities or doing a PR audit:

1. Import the repo
2. Run `start_analysis(repo_id, "security")`
3. Poll until completed
4. Review findings and flag critical issues to the user

---

## Token Awareness

- **Always** call `get_token_balance()` before starting an analysis
- If `available_tokens` is low, tell the user — they can purchase more at [reporead.com/settings](https://www.reporead.com/settings)
- Monthly allowances: Free 100K, Starter 500K, Growth 1M
- Larger repos consume more tokens
- `reserved_tokens` shows tokens held for in-progress analyses

---

## Tips

- **Poll `get_analysis_status`**, not `get_analysis` — much lighter payload
- **Poll every 10 seconds.** Analysis takes 1-5 minutes depending on repo size
- **Status values:** `queued` → `processing` → `completed` or `failed`
- If status is `failed`, show the `error` field to the user — do not retry automatically
- Use `list_repositories` before `import_repository` to avoid "already imported" errors
- The `branch` parameter is optional — defaults to the repo's default branch
- Rate limit: 60 requests/minute burst
- `analysis_type` must be one of: `readme`, `technical`, `security`, `mermaid`, `llmstxt`
