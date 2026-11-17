---
name: skills
description: Generate a 1-on-1 brief from GitHub activity. Fully deterministic pipeline — 5 tool calls, zero sub-agent spawns.
license: MIT
---

## Overview

PullStar fetches GitHub activity for one engineer (PRs authored, reviews given), runs a **deterministic local scoring engine** across five dimensions, and prepares an LLM input payload. The **agent** then performs LLM inference and finalizes the brief.


**Quickstart:** 

    run_brief.py --login steipete --pr-insights --days 7
    Read llm_input_steipete.json, do the LLM inference, present the brief



**Data Flow Summary:**

| Step | What runs | External calls |
|------|-----------|----------------|
| Ingest | `run_brief.py` → `ingest.py` | GitHub API |
| Score | `run_brief.py` → `score.py` | None |
| Prepare | `run_brief.py` → `agent_prepare_1on1.py` | None |
| **Agent inference** | **Agent calls LLM** | **LLM provider** |
| Finalize | Agent runs `agent_finalize_1on1.py` | None |

**⚠️ Important:** Steps 1–3 run locally. Only the LLM inference step (step 4) sends data to your AI provider.

---

## Requirements

- Python 3.11+
- Install dependencies: `pip install PyGithub python-dotenv requests`
- A GitHub personal access token (see Security section below)

---

## Security & Privacy

### Token Scope

| Option | Where to create | Best for |
|--------|----------------|----------|
| Classic PAT (`repo` scope) | https://github.com/settings/tokens | Cross-user search, org-wide ingestion |
| Fine-grained PAT | https://github.com/settings/personal-access-tokens | Your own repos only |

> Fine-grained PATs cannot search across arbitrary users. Use a classic PAT for org-wide briefs.

Set `GITHUB_ORG` to narrow search to one organization.

### Token Resolution Order

Secrets are resolved using layered lookup — first match wins:

1. `--github-token` CLI flag (override/debug only — never logged)
2. `GITHUB_TOKEN` environment variable
3. `~/.pullstar/credentials` (key=value format)
4. `.env` in the skill directory

### Data Privacy by Mode

**Default (no `--pr-insights`):**
- Only aggregated statistics and scores sent to LLM
- No raw PR text, comments, or review bodies included

**PR Insights (`--pr-insights`):**
- Bounded raw PR discussion text packaged into the LLM prompt
- Bounded to 5 PRs, 3 reviews/comments each, 600 char limit per item
- Review `llm_input_{login}.json` before inference if you have privacy concerns

---

## Configuration

### `.env`

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Recommended | Classic PAT with `repo` scope. Omit for unauthenticated access (60 req/hr). |
| `GITHUB_ORG` | No | Scope ingestion to one org. |

---

## Usage

### Standard run

```bash
python run_brief.py --login jsmith
```

### With PR insights

```bash
python run_brief.py --login jsmith --pr-insights
```

### Common options

```bash
python run_brief.py --login jsmith --days 14          # wider lookback (default: 5)
python run_brief.py --login jsmith --max-results 10   # faster on high-activity users (default: 20)
python run_brief.py --login jsmith --api-mode rest    # force REST API (default: graphql)
```

### All options

| Flag | Default | Description |
|------|---------|-------------|
| `--login` | required | Engineer GitHub login |
| `--days` | `5` | Lookback window in days |
| `--pr-insights` | off | Include PR review/comment context in LLM prompt |
| `--max-results` | `20` | Max search results to iterate (lower = faster) |
| `--api-mode` | `graphql` | `graphql` or `rest` |
| `--output-dir` | `.pullstar` | Directory for all artifacts |
| `--github-token` | — | Override/debug only. Prefer `.env`. |

---

## Agent Flow (Deterministic — No Sub-Agents)

**The entire pipeline runs in the agent's main session.** Use `exec` for Python scripts and do the LLM inference inline — the agent itself is the LLM. Never spawn sub-agents.

```
1. exec:    python run_brief.py --login <login> [flags]
2. read:    .pullstar/llm_input_<login>.json
3. write:   .pullstar/llm_output_<login>.json  (produce the brief inline as the LLM)
4. exec:    python scripts/agent_finalize_1on1.py --login <login>
5. read:    .pullstar/output_<login>.json       (quality gate: verify meaningful data)
6. (done — present the brief)
```

### Why Inline

- **Zero sub-agent overhead.** No spawn latency, no polling, no completion-event complexity.
- **Deterministic tool count.** Exactly 5 tool calls: exec → read → write → exec → read.
- **Faster end-to-end.** All steps run sequentially in one session with no context-fork tax.
- **The agent IS the LLM.** Creating a sub-agent to call the same model for inference adds nothing.

### Quality Gate

After step 4, read `output_<login>.json` and verify the brief has meaningful data. If `total_score` is 0 or the brief contains phrases like "no activity" / "no contributions" / "no PRs merged" / "insufficient data", respond with a graceful fallback message instead of presenting an empty brief.

---

## Agent JSON Contract

### Input (from `run_brief.py`)

File: `.pullstar/llm_input_{login}.json`

| Field | Type | Description |
|-------|------|-------------|
| `system` | string | System prompt with instructions |
| `user` | string | User message with engineer data and scores |
| `metadata` | object | Version, timestamps, total score, confidence |

### Output (from agent)

File: `.pullstar/llm_output_{login}.json`

```json
{
  "version":        "1.0",
  "engineer_login": "jsmith",
  "brief":          "## Quick Summary\n..."
}
```

**Requirements:**
- Valid JSON
- `brief` must be a non-empty markdown string
- Plain text is also accepted — the full file content will be used as the brief

---

## Brief Output Format

The final brief (`output_{login}.json`) contains a markdown document with six sections:

| Section | Content |
|---------|---------|
| **Quick Summary** | 2–3 sentences, lead with concrete numbers |
| **Highlights** | 2–4 bullets, one data point each |
| **Areas to Explore** | 2–3 open-ended questions for the 1-on-1 |
| **Patterns Worth Noting** | 1–3 factual behavioral observations |
| **Score Summary** | Markdown table — Dimension / Score / Confidence / Signal. Emoji encouraged in Confidence column. |
| **Suggested Focus** | One paragraph on the most useful 1-on-1 theme |

Example Score Summary table:

| Dimension | Score | Confidence | Signal |
|-----------|-------|------------|--------|
| Velocity | 16/20 | ✅ High | 10 PRs merged, 3 active weeks |
| PR Quality | 14/20 | ✅ High | Avg 320 lines, 2 large PRs flagged |
| Review Participation | 8/20 | ⚠️ Medium | 3 reviews given in window |
| Collaboration | 12/20 | ✅ High | 4 repos, 3 reviewers per PR avg |
| Consistency | 10/20 | 🔴 Low | 1 of 3 weeks inactive |

---

## Artifacts

All artifacts are written to `.pullstar/` (gitignored, never committed).

| File | Written by | Sent to AI? |
|------|------------|-------------|
| `ingest_{login}.json` | `ingest.py` | ❌ No |
| `score_{login}.json` | `score.py` | ❌ No |
| `llm_input_{login}.json` | `agent_prepare_1on1.py` | ✅ Yes |
| `llm_output_{login}.json` | Agent | ❌ No |
| `output_{login}.json` | `agent_finalize_1on1.py` | ❌ No |

---

## Troubleshooting

**"GitHub rejected the PR search query (422)"**
Use a classic PAT — fine-grained PATs cannot search across arbitrary users.

**"GitHub rate limit hit"**
Authenticated: 5000 req/hr. Unauthenticated: 60 req/hr. Set `GITHUB_TOKEN`.

**Slow ingestion on high-activity users**
Use `--max-results 10` to cap iteration. Default is 20.

**GraphQL errors**
Use `--api-mode rest` to fall back to the legacy REST API.

---

## For Agent Developers

### Deterministic Pattern (Mandatory)

The brief pipeline is fully deterministic. There is exactly one correct execution path:

```
exec(run_brief.py) → read(llm_input) → write(llm_output) → exec(agent_finalize) → read(output/quality gate)
```

**❌ Never spawn sub-agents for this pipeline.** The agent itself performs the LLM inference step — delegating to a sub-agent is redundant, adds latency, and creates thrash. The pipeline completes in 5 tool calls. If you're tempted to spawn a sub-agent, ask yourself: "Am I running a Python script or doing LLM inference?" If the answer is "Python script," use `exec`. If the answer is "LLM inference," do it inline.

**Recovery:** If `run_brief.py` exits non-zero, the GitHub user likely doesn't exist or the token is invalid. Respond with the graceful fallback message; do not retry or spawn alternative paths.

---

## License

MIT — See source repository for full license text.
