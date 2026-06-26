---
name: skill-feed
description: Scenario-driven skill recommendation engine for ClawHub. Detects failed or stuck workflows, builds targeted search queries, and returns ranked skill recommendations with immediate recovery steps and fallback paths. Use when users say they want to do something but are blocked (errors, retries, timeout, missing outputs, unclear implementation path), or when you need recommendations adapted for Claude Code, ChatGPT, and Gemini execution styles.
---

# SkillFeed

Automatically match the best skills to unblock a failed or stuck workflow.

## Trigger Conditions (auto)

Run this skill when any of these signals appears:

1. Command/API failure (non-zero exit, HTTP 4xx/5xx)
2. Retry threshold exceeded (default >=2 retries)
3. Expected output missing (for example no tweet id after post task)
4. Execution timeout exceeded
5. User explicitly asks for tool/skill recommendation
6. User describes a goal but has no clear implementation path

Do not trigger for normal delay/noise or when the user already has a working solution.

## Workflow

1. Capture failure context (sanitize before any external use)
   - task name
   - platform (X/Twitter, Telegram, GitHub, etc.)
   - error message/code (generic type only — see sanitization rules below)
   - latest action log summary (stripped of secrets)
2. Classify failure type
   - auth/permission
   - rate limit/quota
   - network/timeout
   - invalid params/payload
   - unknown
3. Build layered search queries (broad -> scenario -> failure)
   - Q1 broad capability query
   - Q2 scenario-specific query
   - Q3 failure-specific query with error tokens
   - **Sanitize all queries before searching** — see Data Sanitization section
4. Search ClawHub
   - Use `https://clawhub.ai/skills?focus=search`
   - Always perform a live search; use `references/top-skills-*.md` only as offline fallback
   - Prefer sorting by stars / recently updated when comparing candidates
5. Rank candidates
   - match to goal (highest weight)
   - match to failure type
   - setup cost and risk
   - maintenance signals
6. Return recovery plan
   - Top 1 primary skill
   - 2 alternatives
   - 3-5 concrete next actions
   - fallback path if primary fails
7. Anti-noise guardrails
   - Avoid repeating the same recommendation for the same error within a single conversation
   - Avoid auto-running high-risk external actions without user confirmation

## Query Construction Rules

Generate queries from context tokens:

- Goal tokens: `post`, `schedule`, `auto reply`, `daily report`
- Platform tokens: `x`, `twitter`, `tweet`, `telegram`, `github`
- Failure tokens: `401`, `403`, `429`, `timeout`, `invalid token`, `permission denied`

Example for failed tweet post:

- Q1: `tweet automation`
- Q2: `x twitter schedule post cron`
- Q3: `twitter post failed 401 invalid token rate limit`

## Data Sanitization

All failure context MUST be sanitized before it is included in any external search query or output. This prevents accidental leakage of secrets, credentials, and private data.

### Strip before searching

- API keys, tokens, passwords, secrets (e.g. `sk-...`, `ghp_...`, `Bearer ...`)
- Personally identifiable information (emails, usernames, IPs, hostnames)
- Internal URLs, file paths containing usernames or org names
- Request/response bodies and headers containing auth data
- Environment variable values (keep only the variable name)

### Keep in queries (safe tokens)

- Generic error codes: `401`, `403`, `429`, `500`, `timeout`
- Generic error types: `invalid token`, `rate limit`, `permission denied`
- Platform names: `twitter`, `github`, `telegram`
- Action verbs: `post`, `publish`, `schedule`, `fetch`

### Rules

1. Never embed raw log lines in a search query — extract only the error type/code.
2. If unsure whether a token is sensitive, omit it.
3. Queries should read like generic capability descriptions, not contain project-specific data.

Example — BAD query: `twitter post failed Bearer sk-abc123 user@company.com 401`
Example — GOOD query: `twitter post failed 401 invalid token`

## Provider Adaptation (Claude Code / ChatGPT / Gemini)

Format the recovery plan for the current provider by default. Only include multi-provider runbooks when the user explicitly requests cross-platform output.

1. Keep core logic provider-neutral
   - Use the same goal, failure classification, query generation, and ranking flow.
2. Detect current provider and use the matching execution style
   - Claude Code: terminal-first, exact command sequences, minimal commentary.
   - ChatGPT: compact checklist bullets, short "why" before steps.
   - Gemini: explicit sections, assumptions, deterministic validation criteria.
3. Normalize outputs
   - Keep identical recommendation order across providers.
   - Only vary phrasing and action formatting.

## Output Format

- Goal: <what user wants>
- Failure signal: <what failed>
- Primary recommendation: `<skill>` (`/slug`) — <why>
- Alternatives:
  - `<skill>` (`/slug`) — <tradeoff>
  - `<skill>` (`/slug`) — <tradeoff>
- Immediate actions (3-5 steps)
- Success check:
  - expected output present
  - no critical error in latest run
- Fallback if still failing
- Execution notes: <steps formatted for current provider>

## References

- Search and ranking recipes: `references/discovery-workflow.md`
- Scenario keyword map: `references/query-templates.md`
- Claude Code / ChatGPT / Gemini adaptation: `references/provider-adaptation.md`
