---
name: release-notes
description: "User-facing change logs: categories, clarity, links. Use when maintaining CHANGELOG or release notes."
---

# Release Notes

Structured guidance for **CHANGELOG** files and **release notes**: confirm triggers, propose the stages below, and adapt if the user wants a lighter pass.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions **release notes**, **CHANGELOG**, **what shipped**, or closely related work
- They want a structured workflow rather than ad-hoc tips
- They are preparing a review, rollout, or stakeholder communication

**Initial offer:**
Explain the four stages briefly and ask whether to follow this workflow or work freeform. If they decline, continue in their preferred style.

## Workflow Stages

### Stage 1: Clarify context & goals

Anchor on **audience** (users vs developers) and **cadence** (per release vs continuous). Ask what success looks like and what must not break.

### Stage 2: Structure & categories

Group changes (features, fixes, breaking, security). Prefer links to issues/PRs and migration notes when breaking.

### Stage 3: Draft & refine

Iterate for clarity: imperative mood, scannable bullets, version headers aligned with semver or product versioning.

### Stage 4: Verify & ship

Close the loop with **tone: concise and verifiable**: monitoring, documentation, stakeholder updates, and lessons learned for the next cycle.

## Checklist Before Completion

- Goals and constraints are explicit for **release notes** work
- Risks and trade-offs are stated, not hand-waved
- Verification steps match the change’s impact (tests, canary, peer review)
- Operational follow-through is covered (monitoring, docs, owners)

## Tips for Effective Guidance

- Be procedural: stage-by-stage, with clear exit criteria
- Ask for missing context (environment, scale, deadlines) before prescribing
- Prefer checklists and concrete examples over generic platitudes
- If the user declines the workflow, switch to freeform help without lecturing

## Handling Deviations

- If the user wants to skip a stage: confirm and continue with what they need.
- If context is missing: ask targeted questions before strong recommendations.
- Prefer concrete examples, trade-offs, and verification steps over generic advice.

## Quality Bar

- Each recommendation should be **actionable** (what to do next).
- Call out **failure modes** relevant to release communication (security, scale, UX, or ops).
- Keep tone direct and respectful of the user’s time.
