# X Bookmarks Digest — Architecture & Implementation Plan

## 1. Purpose

Automatically review X/Twitter bookmarks for useful insights, tools, projects,
repos, products, and ideas. Produce a clean, actionable digest with proposed
next actions — including auto-installing promising skills via clawhub or
scaffolding new ones.

## 2. System Context

```
User trigger ("digest x bookmarks" / "check my bookmarks" / cron)
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  Claude Agent (OpenClaw)                            │
│                                                     │
│  1. Trigger match → load SKILL.md                   │
│  2. Run fetch_bookmarks.py → raw bookmark JSON      │
│  3. Agent analyses bookmarks (LLM-native analysis)  │
│  4. Output digest + proposed actions                │
│  5. Update state (last-checked bookmark ID + ts)    │
└──────────────┬──────────────────────────────────────┘
               │ xurl CLI (authenticated X API)
               ▼
┌─────────────────────────────────────────────────────┐
│  X/Twitter API v2 (via xurl)                        │
│                                                     │
│  GET /2/users/:id/bookmarks                         │
│  Fields: text, author, urls, created_at, metrics    │
└─────────────────────────────────────────────────────┘
```

## 3. Components

### 3.1 SKILL.md (Agent instruction manual)

The primary artifact. Contains:
- Frontmatter (name, description, triggers, metadata)
- Step-by-step workflow the agent follows
- Analysis criteria for categorising bookmarks
- Output format specification
- Error handling table

### 3.2 scripts/fetch_bookmarks.py

Fetches bookmarks via the `xurl` CLI and manages state.

**Responsibilities:**
- Call `xurl bookmarks -n <count>` to get latest bookmarks
- Load last-checked state from `state.json`
- Filter out already-processed bookmarks (by ID comparison)
- Output new bookmarks as JSON to stdout
- Update `state.json` with newest bookmark ID + timestamp
- Enforce rate limit (1 run per hour minimum)

**State file** (`state.json`):
```json
{
  "last_bookmark_id": "1234567890",
  "last_run_ts": "2026-03-19T12:00:00Z",
  "processed_count": 150
}
```

### 3.3 scripts/analyse_bookmarks.py

Lightweight categorisation and scoring of bookmark content.

**Responsibilities:**
- Read bookmark JSON from stdin or file
- Categorise each bookmark:
  - `tool` — CLI tools, libraries, frameworks, SDKs
  - `project` — GitHub repos, open-source projects
  - `product` — SaaS, apps, services, startups
  - `insight` — Tips, techniques, architectural patterns
  - `resource` — Articles, papers, tutorials, threads
  - `other` — Doesn't fit above categories
- Score relevance (1-5) based on keyword matching + heuristics
- Extract URLs, GitHub links, product names
- Output structured JSON with categories and scores

**Note:** The heavy analysis (deciding what's actionable, writing summaries,
proposing next steps) is done by the agent itself after reading the structured
output. This script just pre-processes and categorises.

### 3.4 scripts/digest_runner.sh

Orchestrator script that chains fetch → analyse → output.

```bash
#!/bin/bash
# Usage: digest_runner.sh [--count N] [--force]
# --count: number of bookmarks to fetch (default 50)
# --force: skip rate limit check
```

### 3.5 references/analysis_criteria.md

Reference document for the agent describing:
- What makes a bookmark "actionable"
- Category definitions with examples
- How to decide: install via clawhub vs build new skill vs just note it
- Output format template

## 4. Authentication

```
xurl handles all X API authentication internally.
No tokens are stored or handled by this skill.

Setup check:
1. Run: xurl whoami
2. If 401 → guide user through: xurl auth apps add
3. If success → proceed with bookmarks fetch
```

## 5. Rate Limiting Strategy

X API Free Tier constraints:
- Bookmarks endpoint: limited reads per month
- Safe cadence: max 1 run per hour, recommended 1-2x daily

Implementation:
- `state.json` stores `last_run_ts`
- `fetch_bookmarks.py` checks elapsed time before API call
- `--force` flag bypasses for manual runs
- SKILL.md instructs agent to check before running

## 6. Analysis Workflow

```
Raw bookmarks (JSON from xurl)
    │
    ▼
analyse_bookmarks.py (categorise + score)
    │
    ▼
Structured JSON with categories
    │
    ▼
Agent (Claude) reads structured data and:
  1. Writes human-readable summaries for high-value items
  2. Identifies GitHub repos → proposes cloning or starring
  3. Identifies tools/skills → proposes clawhub install or new skill creation
  4. Identifies insights → proposes saving to memory or Obsidian
  5. Formats final digest output
```

## 7. Output Format

```markdown
# X Bookmarks Digest — 2026-03-19

## Summary
- 47 bookmarks checked, 12 new since last run
- 4 high-value items, 5 medium, 3 low

## High Value

### [Tool] uv — Fast Python package manager
@astaborist: "uv is replacing pip for me..."
- URL: https://github.com/astral-sh/uv
- Action: Install via `pip install uv` or `brew install uv`

### [Project] localllm — Run LLMs locally with 4-bit quantisation
@dev_username: "Just shipped v2.0..."
- URL: https://github.com/user/localllm
- Action: Clone and evaluate for OpenClaw integration

## Medium Value
...

## Proposed Actions
1. [ ] Install uv (`brew install uv`)
2. [ ] Clone localllm for evaluation
3. [ ] Save "React Server Components" thread to Obsidian
4. [ ] Check clawhub for "pdf-ocr" skill mentioned in bookmark #5
```

## 8. File Layout

```
skills/x-bookmarks-digest/
├── SKILL.md                    # Agent instruction manual
├── ARCHITECTURE.md             # This document
├── _meta.json                  # ClawHub package metadata
├── scripts/
│   ├── fetch_bookmarks.py      # Fetch + dedupe + state management
│   ├── analyse_bookmarks.py    # Categorise + score bookmarks
│   └── digest_runner.sh        # Orchestrator script
├── references/
│   └── analysis_criteria.md    # Category definitions + scoring guide
├── state.json                  # Runtime state (last ID, timestamp)
└── .clawhub/
    └── package.json            # ClawHub registry metadata
```

## 9. Dependencies

| Dependency | Purpose | Install |
|-----------|---------|---------|
| xurl | Authenticated X API access | `brew install xurl` (already installed) |
| Python 3.10+ | Script runtime | Pre-installed |
| jq (optional) | JSON processing in shell | `brew install jq` |

## 10. Security

- No X API tokens stored or handled by this skill — xurl manages auth
- No bookmark content persisted beyond state.json (just IDs)
- Rate limiting prevents accidental API quota exhaustion
- Digest output stays local (not posted anywhere)
