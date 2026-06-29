---
name: skill-ops-suite
description: "Runtime-neutral skill operations suite. Input a skill directory, slug, marketplace goal, or release plan; output quality checks, safety boundaries, naming/summary improvements, install-conversion diagnosis, duplicate/merge/redirect recommendations, and a release checklist. Review-only unless the user explicitly approves publishing or destructive changes."
---

# Skill Ops Suite

Use this flagship skill when the user is creating, auditing, publishing, growing, or maintaining agent skills across different agent runtimes and skill marketplaces.

## User Promise

Input a skill directory, skill slug, market goal, or release plan. Output quality and installability checks, safer name/display name/summary/keywords, security boundary review, duplicate/merge/redirect recommendations, and release checklist.

## Safety Boundaries

- Do not publish, delete, rename, archive, or run destructive commands without explicit user approval.
- Do not upload secrets, credentials, private customer data, or sensitive raw logs.
- High-risk domains such as legal, medical, payments, identity, or browser automation require clear disclaimers and stop rules.

## Example Prompts

1. `Review this skill and tell me why users might not install it.`
2. `Rewrite this skill summary using input/output/safety-boundary format.`
3. `Find duplicate skills in this set and recommend merge or redirect actions.`
4. `Prepare a release checklist for publishing this agent skill.`
5. `Audit this shopping skill for login, checkout, payment, and privacy boundaries.`
