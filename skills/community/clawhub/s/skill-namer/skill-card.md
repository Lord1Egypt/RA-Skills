## Description:

Suggests short, sayable names for products, domains, ENS names, skill slugs, and related naming tasks, with harm-aware candidates and search links but no guarantees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otherpowers](https://clawhub.ai/user/otherpowers)

### License/Terms of Use:

MIT-0

## Use Case:

People naming or renaming a business, product, account, domain, ENS name, skill slug, or reusable coordination primitive use this skill to generate harm-aware candidates and organize language, brand, availability, and trademark checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's broad activation condition may make it relevant to a wider range of naming requests.

Mitigation: Use it when the request involves naming, renaming, or letting a name go, and check that this scope fits the task.

Risk: Security analysis was partial: 7 of 11 components were scanned, and tool-misuse analysis was incomplete for four scripts.

Mitigation: Review the four scripts and their behavior before relying on them in a new environment.

## Reference(s):

- [ClawHub skill-namer listing](https://clawhub.ai/otherpowers/skills/skill-namer)
- [Full naming workflow](references/workflow.md)
- [Availability guidance](references/availability.md)
- [Name building blocks and checks ledger](references/blocks.md)
- [Renaming and letting a name go](references/renaming.md)
- [Missing primitive finder](references/primitives.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Candidate names, concise rationale, search links, and a checks ledger; bundled scripts can emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggestions only; availability and trademark status are not guaranteed or cleared.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
