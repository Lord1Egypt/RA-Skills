---
name: skill-merge-and-republish
description: Merge overlapping local skills into one canonical skill and republish the canonical skill to ClawHub. Use when two local skills have overlapping responsibilities, when a temporary helper skill should be folded back into a stronger existing skill, or when the user asks to merge duplicated skills and update ClawHub after the merge.
---

# Skill Merge and Republish

Use this skill when multiple local skills overlap enough that keeping both would create confusion, drift, or duplicated maintenance.

## Goal

Turn:
- duplicated or overlapping skills

into:
- one canonical skill with merged guidance
- one local source of truth
- one updated ClawHub release

## When to use

Use when:
- two skills solve substantially the same workflow
- one newer helper skill should be absorbed into an older canonical skill
- a temporary skill exists only to extend a stronger publish/install/review flow
- the user explicitly says “merge these skills” or “merge this into that and update ClawHub”

## Workflow

1. Read both skills fully.
2. Identify:
   - canonical skill to keep
   - absorbed skill to retire
   - unique instructions that must be preserved
3. Merge the absorbed logic into the canonical `SKILL.md`.
4. Remove the redundant local skill folder.
5. Commit locally.
6. Inspect the canonical remote skill on ClawHub.
7. Bump patch version.
8. Publish the updated canonical skill via `clawhub-publish-flow`.
9. Verify remote status.
10. Update local registry sheet if it references both skills.

## Canonical choice rules

Prefer keeping the skill that already has:
- clearer name
- better installed history
- existing ClawHub presence
- broader but still coherent scope

## Safety rules

- Do not merge unrelated skills just because they look adjacent.
- Do not preserve duplicated wording if it reduces clarity.
- Do not keep both skills unless their trigger boundaries are truly distinct.
- Always update the registry after merge if the registry exists.

## Output

Report:
- kept skill
- retired skill
- what logic was merged
- local commit
- remote version bump
- ClawHub publish result
