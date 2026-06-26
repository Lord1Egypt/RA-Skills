---
name: plan-review
description: Auto-assembles review panel using deterministic rules, dispatches agents against plan file, collects verdicts.
---

Phase gate: PLAN checkpoint. MUST get APPROVE from all reviewers before proceeding to Build.

## Inputs
- Plan file path (default: most recent non-`.done.md` file in `ai-workspace/plans/`)
- `--include <agent>`: Force-add an agent to the panel
- `--exclude <agent>`: Remove an agent (except technical-editor, which cannot be excluded)

## Steps

1. **Find the plan file**:
   ```bash
   ls -t "$(git rev-parse --show-toplevel)/ai-workspace/plans/"*.md | grep -v '.done.md' | head -1
   ```
   If no plan file found → error: "No plan file in ai-workspace/plans/. Write a plan first."
   If plan file is `.done.md` → error: "This plan is already finalized."

2. **Read the plan** and extract:
   - Files to Modify section
   - Full body text
   - Plan scope (count files changed, count body lines)

3. **Assemble the review panel** — invoke `/assemble-panel` with scope = plan file. It returns the panel based on file types and keywords in the plan. Pass `--include`/`--exclude` as overrides. Log which agents were selected and why.

   Codex/Cursor: read `.claude/skills/assemble-panel/SKILL.md` directly and apply the scope/keyword maps inline.

   If `/assemble-panel` is unavailable, fall back to `[technical-editor, code-reviewer]` with gate=P2, cap=3.

4. **Dispatch all selected agents IN PARALLEL** using the Agent tool (single message, multiple Agent tool calls). Each agent receives:
   - The plan file content
   - Their specific review mandate
   - Instructions to return: APPROVE / REVISE / DROP with findings tagged P0/P1/P2

5. **Collect verdicts** and synthesize into a summary table:
   ```
   ## Plan Review Summary
   | Agent | Verdict | P0 | P1 | P2 | Key Finding |
   |-------|---------|----|----|-----|-------------|
   ```

6. **Gate logic and review loop** — invoke `/assemble-panel` for panel governance. It provides the policy algebra (gate=P2, cap=3) and handles RETAIN, EXPAND, CONVERGE, and ESCALATE_RECURRING. Do not duplicate those rules here.

   After each round:
   - All APPROVE with no above-gate findings → "Proceed to Build"
   - Above-gate findings remain → fix, then re-review per assemble-panel's RETAIN + EXPAND rules
   - Cap reached with unresolved findings → escalate to human

   If `/assemble-panel` is unavailable, fall back: keep all reviewers with above-gate findings, exit at round 3 or when all clean.

## Panel Bounds
- Minimum: technical-editor alone (1 agent, trivial plans)
- Typical: technical-editor + code-reviewer + architect-reviewer (3)
- Maximum: all agents (rare, large cross-cutting plans)
