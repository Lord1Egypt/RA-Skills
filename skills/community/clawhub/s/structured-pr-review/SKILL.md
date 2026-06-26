---
name: structured-pr-review
description: >
  Structured PR code review with layered analysis and severity tiers. Two modes:
  (1) Giving reviews — walk through security, correctness, conventions, IaC, and
  testing layers, then produce a verdict with MUST FIX / SHOULD FIX / SUGGESTION.
  (2) Addressing reviews — respond to reviewer comments, fix code, reply to every
  thread, resolve conversations. Uses only `gh` CLI — no external dependencies.
  Use when: reviewing a PR, giving feedback, checking code quality, addressing
  review comments, fixing reviewer feedback, resolving PR threads.
argument-hint: "<PR-URL or number>"
---

# Structured PR Review

Two modes: giving reviews and addressing review comments. No external dependencies — uses `gh` CLI only.

## Giving Reviews

When asked to review or check a PR:

1. Fetch the PR details and full diff
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

## References

- [references/review-layers.md](references/review-layers.md) — review framework, severity tiers, verdict format
- [references/addressing-workflow.md](references/addressing-workflow.md) — comment handling, thread resolution
- [references/conventions.md](references/conventions.md) — your team's conventions (customizable)
- [references/iac-checklist.md](references/iac-checklist.md) — IaC review checklist (customizable)

## Works Well With

- **terraform-skill** (antonbabenko) — Terraform authoring best practices, module patterns, testing strategies
- **conventional-commits** — commit message format conventions (useful when addressing reviews)
- **github** (built-in) — general `gh` CLI operations for PRs, issues, and CI runs
- **gh-issues** (built-in) — automated PR monitoring and review spawning
