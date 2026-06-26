---
name: reddit-to-pr
description: Scan Reddit for pain points in a product’s niche, identify a real user complaint worth fixing, and prepare an approved patch or PR workflow for a target repository. Default to analysis-only; only modify code, commit, push, or open a PR after explicit user approval. Use when asked to check Reddit for issues, find user complaints, do reddit-to-pr, or run a recurring product-feedback-to-code workflow.
---

# Reddit to PR

Scan Reddit for pain points, choose the most actionable issue, and prepare a fix proposal. Default to analysis-only. Only modify code, commit, push, or open a PR after explicit user approval.

## Mode Detection

Use `{baseDir}` as the skill directory. Check whether `{baseDir}/config.json` exists.

- If it does **not** exist, run **Setup Mode**.
- If it exists, run **Execution Mode**.
- If the user says **setup** or **reconfigure**, run **Setup Mode** even if config already exists.

## Setup Mode

Ask setup questions **one at a time**, waiting for the answer before asking the next one.

### Question 1: Target subreddits
Ask:

> What subreddits should I monitor for user feedback? These should be communities where your users or potential users hang out.

Examples: `webdev, reactjs, programming`

Store as `subreddits` — array of strings **without** the `r/` prefix.

### Question 2: Product context
Ask:

> Describe your product in 1–2 sentences. What does it do and who is it for? This helps me identify which complaints are relevant.

Store as `productDescription`.

### Question 3: Repository
Ask:

> What’s the path to your code repository? This is where I’ll create branches and PRs.

Examples: `/Users/you/projects/my-app`

Store as `repoPath`.

### Question 4: Search keywords
Ask:

> What keywords should I look for in Reddit posts? These help filter for relevant complaints.

Examples: `slow, crash, bug, broken, error, annoying, doesn’t work`

Store as `keywords` — array of strings.

### Question 5: Execution mode
Ask:

> Which mode should this use by default? Options: analyze, patch, pr. `analyze` only researches and proposes a fix. `patch` may edit locally after approval. `pr` may edit, commit, push, and open a PR after approval.

Store as `mode`.

### Question 6: Schedule
Ask:

> How often should I run this? Options: nightly, twice-daily, weekly, manual.

Store as `schedule`.

If `schedule` is not `manual` and `mode` is not `analyze`, tell the user scheduled runs should default to `analyze` until they explicitly approve a write-enabled workflow.

### Question 7: Results destination
Ask:

> Where should I post results when I find something? Options: proposal, slack, both.

Store as `resultsDestination`.

If the answer includes Slack, ask one follow-up:

> What Slack destination should I use?

Use an OpenClaw channel id or canonical channel choice. Store it as `slackTarget`.

### Save config

After all answers are collected, save `{baseDir}/config.json` with this shape:

```json
{
  "subreddits": ["webdev", "reactjs"],
  "productDescription": "...",
  "repoPath": "/path/to/repo",
  "keywords": ["slow", "crash", "bug"],
  "mode": "analyze",
  "schedule": "nightly",
  "resultsDestination": "proposal",
  "slackTarget": null,
  "setupComplete": true,
  "setupDate": "2026-03-24"
}
```

Then tell the user: `Setup complete!`

### Scheduling

If `schedule` is not `manual`, help the user set up scheduling.

Scheduled runs must default to `analyze` mode unless the user explicitly reconfigures the skill for a write-enabled workflow and confirms they want that behavior.

For OpenClaw, recommend a cron entry like:

```bash
openclaw cron add \
  --name "reddit-to-pr" \
  --cron "<CRON_EXPR>" \
  --tz "<USER_TIMEZONE>" \
  --session isolated \
  --message "Run the reddit-to-pr skill."
```

Cron expressions:

- `nightly` → `0 2 * * *`
- `twice-daily` → `0 8,20 * * *`
- `weekly` → `0 2 * * 1`

## Execution Mode

Load config from `{baseDir}/config.json`.

Execution mode must honor these safety defaults:
- `mode=analyze`: do not modify repository files
- `mode=patch`: local edits are allowed only after explicit user approval for the selected fix
- `mode=pr`: local edits, commits, pushes, and PR creation are allowed only after explicit user approval for the selected fix

Credential expectations:
- repository access is limited to the configured `repoPath`
- local edits require filesystem access to that repo
- commits require git to be available in that repo
- pushes and PR creation require existing remote/auth tooling already configured in the environment
- this skill must not request, create, or install credentials on its own

### Phase 1: Scan Reddit

For each subreddit in config:

1. Search the web for recent posts in the last 7 days using patterns like:
   - `site:reddit.com/r/{subreddit} {keywords} {productDescription keywords}`
   - `site:reddit.com/r/{subreddit} "wish it could" OR "anyone know how to" OR "frustrated with" OR "why can't" OR "feature request"`
2. Collect posts and comments that describe real pain points.
3. Filter for relevance to the configured product.
4. Prefer current, specific complaints over vague discussion.

### Phase 2: Analyze and prioritize

From all findings:

1. Score each issue by:
   - `frequency` — how often the problem appears
   - `severity` — how frustrated users are
   - `fixability` — whether a concrete code fix is realistic
2. Pick the single best issue: the most fixable issue with meaningful user pain behind it.
3. Document:
   - **The complaint** — direct quotes from Reddit users
   - **The root cause** — what is actually wrong or missing
   - **The fix** — the code change that would address it
   - **Impact** — how many users or threads indicate the pain

### Phase 3: Self-evaluation and local run report

Before implementing the fix, always evaluate the run.

Rate the run from 0–10 based on:

- Did the search find relevant complaints?
- How confident is the proposed fix?
- How efficient was the search?

Only report instruction problems as instruction problems. External blockers are still valid reasons for a low rating, but they are not flaws in the skill itself.

Write a local run report to `{baseDir}/state/last-run.json` with this shape:

```json
{
  "skill": "reddit-to-pr",
  "version": "0.1.2",
  "rating": 7,
  "success": true,
  "whatWorked": "Found 3 relevant complaint threads in r/webdev.",
  "whatFailed": "One subreddit produced low-signal results.",
  "improvementIdea": "Narrow keyword matching before deep analysis.",
  "adaptations": "Prioritized complaint-style phrasing over broad product terms.",
  "errorSummary": null
}
```

If the environment does not permit file writes, include the same report content in your final output under a `Local run report` heading instead of sending it to any external service.

Do not send telemetry to external services from this skill.

### Approval checkpoint

Before making any repository changes, present:
- the selected Reddit complaint
- the proposed root cause
- the intended fix
- the files likely to change
- the tests you plan to run
- whether the current config permits patch-only work or full PR work

Do not modify files, create branches, commit, push, or open a PR until the user explicitly approves the selected fix.

If approval is not given, stop after analysis and save the proposal + local run report.

### Phase 4: Implement fix

Only run this phase after explicit user approval.

1. Navigate to `repoPath`.
2. Operate only inside that repository. Do not modify files outside `repoPath`.
3. Create a branch named `fix/reddit-<short-description>-<date>` if the approved mode requires edits.
4. Investigate the relevant code paths.
5. Implement the smallest real fix that addresses the complaint.
6. Add or update tests.
7. Run relevant tests.
8. Commit with:

```text
fix: <description> (sourced from r/<subreddit> user feedback)
```

### Phase 5: Open PR

Only run this phase if `mode=pr` and the user explicitly approved PR creation for this fix.

Open a PR using this format.

**Title**

```text
fix: <short description of fix>
```

**Body**

```markdown
## User Pain Point

> "{direct quote from Reddit user}"
> — u/{username} in r/{subreddit} ({upvotes} upvotes, {comments} comments)

[Additional quotes if available]

## Root Cause
{What is actually causing the issue}

## Fix
{What this PR changes and why}

## Evidence
- Found in: r/{subreddit}
- Frequency: {how many posts/comments mention this}
- Severity: {High/Medium/Low}

## Test Plan
- [ ] {test steps}

---
*Generated by OpenClaw Network Skills — reddit-to-pr*
```

### Phase 6: Notify

If `resultsDestination` is `proposal` or `both`, include a concise local proposal summary in the final output even when no code was changed.

If `resultsDestination` includes Slack:

- If `slackTarget` exists, use OpenClaw messaging to send a short summary and PR link.
- Do not send notifications to arbitrary webhooks from this skill.

Include:

- the pain point
- the chosen fix
- the subreddit source
- the PR link
- any notable risk or follow-up

## Guardrails

- Do not claim Reddit evidence is strong if the signal is weak.
- Do not implement speculative product changes when the complaint is ambiguous.
- Prefer minimal, testable fixes over broad roadmap detours.
- Default to analysis-only unless the user explicitly approved a write-enabled run.
- Do not modify files, create branches, commit, push, or open a PR without an explicit approval step for the selected fix.
- Limit all repository access to the configured `repoPath`; do not modify files outside that repo.
- Do not change secrets, auth, billing, deployment, or infrastructure code unless the user explicitly approves that scope.
- If the repo path is missing, invalid, or inaccessible, stop after analysis and report that blocker.
- If no credible complaint is found, say so plainly instead of forcing a patch or PR.
- If opening a PR or sending a notification requires credentials or permissions that are missing, stop and report the exact blocker.
