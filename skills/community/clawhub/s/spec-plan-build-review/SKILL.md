---
name: spec-plan-build-review
description: "Run a proportional delivery lifecycle for software or skill work: clarify scope, create a concise plan, implement, verify, review, and ship. Use when the user asks to spec, plan, build, test, review, ship, release, prepare a PR, prepare ClawHub or GitHub publication, or coordinate a multi-step coding task that should not skip verification."
---

# Spec Plan Build Review

Use this skill to turn non-trivial work into a controlled delivery loop. Keep it proportional: tiny edits can skip straight to implementation and verification.

## Lifecycle

1. **Spec**
   - Identify the user-visible outcome, affected repo or package, and non-goals.
   - Read local context before deciding the implementation shape.
   - If requirements conflict, resolve from source evidence or ask one focused question.

2. **Plan**
   - Make a short checklist only when it helps.
   - Keep one item in progress at a time.
   - Assign verification before shipping, not after.

3. **Build**
   - Reuse existing patterns and helpers.
   - Keep changes tightly scoped to the stated outcome.
   - Avoid unrelated refactors, formatting churn, and broad dependency changes.

4. **Verify**
   - Run the narrowest reliable local checks first.
   - Add or update tests when behavior changed.
   - Record any checks that could not run and why.

5. **Review**
   - Inspect the diff as if reviewing a PR.
   - Lead with defects, missed tests, user-visible regressions, and release risks.
   - For risky work, use a fresh-context or high-risk review skill before shipping.

6. **Ship**
   - Confirm a clean worktree except intended changes.
   - Commit with a specific message.
   - Push and verify remote CI.
   - Create release artifacts only after CI is green.

## Proportionality Guide

- `tiny`: one file or docs-only edit; implement and run a direct check.
- `normal`: small feature or bug fix; plan, implement, test, review.
- `release`: public package, ClawHub skill, security-sensitive change, or migration; run full lifecycle and remote CI.
- `high-risk`: destructive operations, credentials, permissions, money, production, public policy; add fresh-context skeptical review.

## Review Personas

Use these lenses during the review step:

- `code reviewer`: correctness, maintainability, local conventions.
- `test engineer`: missing coverage, flaky assumptions, reproducibility.
- `security reviewer`: permissions, secrets, data exposure, supply chain, release surface.

If the runtime supports real subagents and the task is large enough, fan out independent review passes. Otherwise, apply the lenses sequentially in the main context and keep findings concrete.

## Ship Checklist

- Local tests or validators pass.
- Public metadata is current.
- No generated temp files are staged.
- GitHub Actions are green for the pushed commit or tag.
- ClawHub publish uses the same version as the repo release.
- Final status names the shipped version, checks, and any residual risk.
