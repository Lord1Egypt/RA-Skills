---
name: work-productivity-skill-vetter-workflow-helper
description: Vet third-party or generated skills for usefulness, safety, overlap, and publish quality. Use when the user needs to decide whether to install, keep, rename, merge, improve, or publish a skill based on evidence and review criteria.
---

# Work Productivity Skill Vetter Workflow Helper

Use this skill when a skill folder or marketplace listing needs a practical go/no-go review that balances usefulness, safety, duplication risk, and maintenance burden.

Read `references/requirement-plan.md` for the demand evidence that led to this package.

## Review Inputs

Collect:

- Skill folder, listing URL, or marketplace metadata.
- Intended user job and trigger examples.
- Existing local skills that may overlap.
- User's decision: install, publish, archive, merge, rename, or revise.

## Workflow

1. Read `SKILL.md` frontmatter first and judge whether the trigger description is specific enough.
2. Inspect bundled resources only as needed: scripts for execution risk, references for usefulness, assets for licensing or relevance.
3. Compare the skill against nearby local or marketplace skills to find duplication.
4. Score the skill on job clarity, trigger quality, operational safety, evidence, completeness, and maintenance cost.
5. Recommend keep, revise, merge, reject, or publish, with the smallest set of required changes.
6. If revising, produce concrete frontmatter/body edits and validation commands.

## Guardrails

- Do not install or publish a skill just because it has a high-level promise.
- Treat vague "helper" skills as suspect unless the body contains a real workflow.
- Separate security blockers from quality improvements.
- Preserve the user's existing skill folders unless they explicitly request cleanup.

## Outputs

- Skill vetting report with decision and rationale.
- Overlap or duplicate-skill analysis.
- Required fixes before install or publish.
- Revised trigger description or workflow outline when useful.

## Validation Checklist

- The decision follows from explicit criteria.
- Security risks and usefulness gaps are separated.
- Duplicate or overlapping skills are named.
- Required fixes are concrete enough to implement.

## Triggers

Keywords: skill vetter, vet skill, review skill, install decision, publish readiness, duplicate skill, trigger quality, marketplace skill.

Example requests:

- `Vet this skill before I install it.`
- `Use $work-productivity-skill-vetter-workflow-helper to decide whether these generated skills are publishable.`
- `Compare this skill with my existing ones and recommend keep, merge, or reject.`
