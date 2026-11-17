---
name: structured-pr-review
description: "Layered PR code review with severity tiers (MUST FIX/SHOULD FIX/SUGGESTION) and addressing-mode. Default: gh CLI only; optional Lobster pipeline."
---

# Structured PR Review

Two modes: giving reviews and addressing review comments. The default/fallback path uses `gh` CLI only — no extra dependencies. An optional Lobster pipeline parallelises data gathering when Lobster (Node/npx) is available; see [references/lobster-integration.md](references/lobster-integration.md).

## Data gathering (optional Lobster pipeline)

`run-pr-review.sh` gathers PR metadata, diff, CI status, and existing review
comments in one step and emits a `pr-context-v0` JSON blob. Use this context
for analysis instead of making multiple sequential `gh` calls.

```bash
# Auto-detect Lobster; falls back transparently to direct pipe-through
scripts/run-pr-review.sh https://github.com/owner/repo/pull/123

# Force direct path (no Lobster required)
scripts/run-pr-review.sh 42 --repo owner/repo --no-lobster
```

See [references/lobster-integration.md](references/lobster-integration.md) for
the full workflow, Lobster args, explicit commands, and install instructions.

## Giving Reviews

When asked to review or check a PR:

1. Fetch the PR details and full diff (use `run-pr-review.sh` or `gh` directly)
2. Walk through each review layer in order (see [references/review-layers.md](references/review-layers.md)):
   - **Security** — secrets, injection, auth, exposure
   - **Correctness** — logic errors, edge cases, error handling
   - **Conventions** — team standards (customize via [references/conventions.md](references/conventions.md))
   - **IaC** — Terraform/CloudFormation checks (customize via [references/iac-checklist.md](references/iac-checklist.md))
   - **Testing** — coverage, new code has tests
3. Produce a structured verdict with severity tiers

**Key principles:**
- Be direct — "this approach has problems" beats "interesting choice"
- Every issue includes what to fix, not just what's wrong
- Acknowledge what the PR does well
- When in doubt on severity, go one level lower

See [references/review-layers.md](references/review-layers.md) for the full framework and verdict format.

## Addressing Review Comments

When asked to address, fix, or respond to PR feedback:

1. Fetch all review comments (inline + review-level)
2. Fix each issue or document why not
3. Reply to every comment — none left unacknowledged
4. Resolve threads, update PR description, push

See [references/addressing-workflow.md](references/addressing-workflow.md) for the step-by-step workflow.

**Key rules:**
- Never leave comments unacknowledged — reply to every one
- Always update the PR description after making changes
- Verify the PR is actually merged before closing linked issues

## Customization

This skill ships with generic review layers. Customize for your team:

- **[references/conventions.md](references/conventions.md)** — coding conventions, commit format, naming rules. Ships with common defaults — customize for your team.
- **[references/iac-checklist.md](references/iac-checklist.md)** — add your IaC-specific checks (required tags, allowed regions, provider pins). Ships with common Terraform patterns — extend for your org.

## Scripts

- `scripts/run-pr-review.sh` — Orchestrator: Lobster if available, direct fallback otherwise
- `scripts/pr-review-workflow.lobster` — Lobster workflow (4 steps: fetch-pr, fetch-ci, fetch-reviews, merge)
- `scripts/lobster-safe-run.sh` — Exit-code wrapper so soft exit-1 steps don't abort Lobster
- `scripts/fetch-pr.sh` — PR metadata + diff → JSON
- `scripts/fetch-ci.sh` — CI / check-run status → JSON
- `scripts/fetch-reviews.sh` — Review comments + inline threads → JSON
- `scripts/merge-pr-context.py` — Merge source blobs → pr-context-v0 envelope

## References

- [references/lobster-integration.md](references/lobster-integration.md) — Lobster path usage, workflow steps, args, install
- [references/review-layers.md](references/review-layers.md) — review framework, severity tiers, verdict format
- [references/addressing-workflow.md](references/addressing-workflow.md) — comment handling, thread resolution
- [references/conventions.md](references/conventions.md) — your team's conventions (customizable)
- [references/iac-checklist.md](references/iac-checklist.md) — IaC review checklist (customizable)

## Works Well With

- **terraform-engineer** — Terraform authoring best practices, module patterns, testing strategies
- **github** (built-in) — general `gh` CLI operations for PRs, issues, and CI runs
- Follow your team's commit message conventions when addressing reviews (conventional commits style works well)
- **gh-issues** (built-in) — automated PR monitoring and review spawning
