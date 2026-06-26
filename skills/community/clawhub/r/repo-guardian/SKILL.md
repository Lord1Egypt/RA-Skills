---
name: repo-guardian
description: >
  Automated GitHub PR review governance and repository maintenance automation.
  Use when reviewing pull requests with dual-model consensus, enforcing merge
  gates, auto-merging approved PRs, and triaging repo state on a cron schedule.
  Not for implementing issue fixes end-to-end (use gh-issues) or general GitHub
  CLI operations (use the github skill). Works on any GitHub repository.
version: 1.4.1
homepage: https://clawhub.ai/corbin-breton/repo-guardian
metadata:
  openclaw:
    requires:
      env:
        - GH_TOKEN
        - GUARDIAN_AGENT
        - GUARDIAN_REVIEWER_B_AGENT
        - GUARDIAN_REPO
        - GUARDIAN_AUTO_MERGE
        - GUARDIAN_AUTO_FIX
        - GUARDIAN_MAX_PRS
        - GUARDIAN_MAX_ISSUES
      bins:
        - openclaw
        - python3
        - curl
    primaryEnv: GH_TOKEN
---

# Repo Guardian — Dual-Model PR Review & Issue Triage

Automated repository maintenance with cross-model review consensus.

## Scope & Boundaries

Repo Guardian handles **PR review governance and repo maintenance automation**:
reviewing PRs, enforcing quality via dual-model consensus, auto-merging when
approved, and triaging repository state.

It is **not** the issue-to-fix implementation pipeline. If the job is to fetch
issues, spawn coding agents, implement fixes, open PRs, and monitor review
feedback, use **gh-issues** instead.

It is also **not** a general-purpose GitHub CLI toolkit. For direct `gh` CLI
operations such as listing PRs, commenting, checking CI, or making ad hoc API
queries, use the **github** skill.

## NOT For

- **Implementing issue fixes end-to-end** — fetching issues, spawning coding agents, writing code, and opening PRs belongs to the **gh-issues** skill
- **General GitHub CLI operations** — listing PRs, commenting, checking CI, or ad-hoc `gh` queries belong to the **github** skill
- **Code authoring or refactoring** — Repo Guardian reviews and gates merges; it does not write new code

## What It Does

Every 6 hours (configurable), Repo Guardian:

1. **Checks for open PRs** on the target repo
2. **Reviews each PR** with two independent models (Opus + GPT-5.4)
3. **Merges** if both models approve
4. **Requests changes** if either model finds issues
5. **Optionally prepares follow-up remediation** for review-discovered issues
6. **Checks for open issues** and triages them for the appropriate next step

## Cron Setup

```bash
# Run the guardian script via OpenClaw cron
# Add to ~/.openclaw/cron/jobs.json:
{
  "repo-guardian": {
    "schedule": "0 */6 * * *",
    "agent": "<your-agent-name>",
    "message": "Run repo-guardian for your-org/your-repo",
    "skill": "repo-guardian"
  }
}
```

Or run manually:
```bash
bash <skill_dir>/scripts/guardian.sh your-org/your-repo
```

## Review Process

### PR Review (Dual-Model Consensus)

```
Open PR detected
  │
  ├─→ Opus reviews (security, architecture, correctness)
  ├─→ Sonnet reviews (code quality, edge cases, tests)
  │   (fallback: Haiku if Sonnet unavailable)
  │
  ├─ Both APPROVE → auto-merge (squash)
  ├─ One APPROVE, one REQUEST_CHANGES → post review comments, do not merge
  ├─ Both REQUEST_CHANGES → post review comments, do not merge
  └─ Either finds CRITICAL issue → post comments + label "needs-fix"
```

### Issue Triage

```
Open issue detected
  │
  ├─ Assess complexity and routing (ready for automation vs needs human)
  ├─ Ready for implementation: hand off to the issue-fix pipeline (gh-issues)
  └─ Complex or unclear: add label "needs-human", post analysis comment
```

## Review Criteria

Each model evaluates independently against:

1. **Correctness** — Does the code do what the PR claims?
2. **Security** — Any vulnerabilities, secret exposure, injection risks?
3. **Tests** — Are changes tested? Do existing tests still pass?
4. **Scope** — Does the PR stay within its stated purpose?
5. **Quality** — Code style, error handling, edge cases, naming

Each model returns a structured verdict:
```json
{
  "verdict": "APPROVE|REQUEST_CHANGES|CRITICAL",
  "summary": "One-line summary",
  "findings": [
    {"severity": "critical|major|minor", "file": "...", "line": 0, "issue": "...", "fix": "..."}
  ],
  "confidence": "high|medium|low"
}
```

## Configuration

Environment variables (set in shell or `.env`):
- `GH_TOKEN` — GitHub token with repo access (required)
- `GUARDIAN_AGENT` — OpenClaw agent name for Reviewer A (default: `$OPENCLAW_AGENT` or `default`)
- `GUARDIAN_REVIEWER_B_AGENT` — OpenClaw agent name for Reviewer B (default: same as `GUARDIAN_AGENT`; set to a different agent for true cross-model review)
- `GUARDIAN_REPO` — Default repo (e.g., `your-org/your-repo`)
- `GUARDIAN_AUTO_MERGE` — Enable auto-merge on consensus (`true`/`false`, default: `true`)
- `GUARDIAN_AUTO_FIX` — Enable auto-fix for issues (`true`/`false`, default: `false`)
- `GUARDIAN_MAX_PRS` — Max PRs to review per run (default: `5`)
- `GUARDIAN_MAX_ISSUES` — Max issues to process per run (default: `3`)

## Data Flow & Privacy

Repo Guardian sends PR diffs and file listings to the configured OpenClaw agent models for review. This means:

- **Repository code from open PRs is transmitted to your configured AI model providers** (e.g., Anthropic, OpenAI) via the OpenClaw agent interface
- No data is sent to any third-party endpoint beyond your configured model providers
- Large diffs are truncated to 500 lines before transmission to limit exposure
- The `GH_TOKEN` is used only for GitHub API calls and is never passed to AI model prompts
- All JSON payloads to the GitHub API are constructed via Python `json.dumps()` to prevent injection

**Recommended `GH_TOKEN` scopes:** `repo` (read) for review-only mode; add `repo` (write) only if auto-merge is enabled. Use a fine-grained token scoped to the specific repository when possible.

## Safety

- **Never force-pushes** or modifies protected branches
- **Squash merges only** — clean history
- **Labels PRs** with review status for audit trail
- **Posts review comments** with model attribution (which model said what)
- **Requires dual consensus** — single model cannot merge alone
- **Skips PRs by org members** marked with `skip-guardian` label
- **Dry-run mode** available (`--dry-run` flag)
- Credentials (GH_TOKEN) are user-configured via environment variables; Repo Guardian never stores, bundles, or transmits tokens
- Auto-merge requires explicit opt-in (GUARDIAN_AUTO_MERGE=true); disabled by default
- All review actions are logged with model attribution for full audit trail
- The skill operates only on the repository specified by the user; it does not discover or access other repos

## Run Trace Logging

Each Repo Guardian run emits a structured trace for audit and performance tracking. After completing all PR reviews and issue triages, write a trace entry:

```markdown
### [YYYY-MM-DD HH:MM] repo-guardian run
- **Repo:** [owner/repo]
- **PRs reviewed:** [count] (merged: N, changes requested: N, critical: N)
- **Issues triaged:** [count] (routed to gh-issues: N, labeled needs-human: N)
- **Model agreement rate:** [% of PRs where both models reached same verdict]
- **Duration:** [approx time]
- **Anomalies:** [any unexpected behavior, timeouts, model disagreements worth noting]
```

Write traces to `memory/performance/skill-runs.md` (following the standard skill execution logging protocol). The model agreement rate is a key health metric — if it drops below 70% over 5+ runs, the review criteria may need recalibration.

## Models Used

| Role | Primary | Fallback |
|------|---------|----------|
| Reviewer A | anthropic/claude-opus-4-6 | anthropic/claude-sonnet-4-6 |
| Reviewer B | anthropic/claude-sonnet-4-6 | anthropic/claude-haiku-4-5 |
| Issue triage | anthropic/claude-sonnet-4-6 | anthropic/claude-haiku-4-5 |

> **Note:** GPT-5.4 (`openai-codex/gpt-5.4`) can be used as Reviewer B if the OpenAI Codex agent is configured and available in your deployment. When using GPT, set Reviewer B primary to `openai-codex/gpt-5.4` with fallback `anthropic/claude-sonnet-4-6`.

## Requirements

**Required environment variables:**
- `GH_TOKEN` — A GitHub Personal Access Token. **Must be set explicitly** (the script will not fall back to `gh auth token` to avoid inadvertent scope leakage). Use a fine-grained PAT scoped to the specific target repository with read/write permissions for pull requests and issues.

**Required binaries (must be on PATH):**
- `openclaw` — OpenClaw CLI (dispatches review prompts to configured model agents)
- `python3` — JSON construction and data parsing
- `curl` — GitHub API calls

**Required OpenClaw configuration:**
- At least one agent configured with access to Opus-tier and Sonnet/GPT-tier models for dual-model review
