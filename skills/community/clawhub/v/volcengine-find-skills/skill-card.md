## Description:

Find, compare, and install Volcengine marketplace skills that cover a user's task or fill a capability gap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Volcengine users can browse the marketplace catalog, identify the smallest set of skills for a task, and check or install selected capabilities when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status checks and installation can automatically download and run software.

Mitigation: Use a reviewed, pinned CLI and skill source; inspect the command with dry-run and approve exact skills before installation.

Risk: A capability gap can lead to user-wide skill installation.

Mitigation: Prefer project scope and review the exact skills and installation scope before proceeding.

## Reference(s):

- [Skill catalog](references/catalog.json)
- [Volcengine Skills Finder on ClawHub](https://clawhub.ai/volc-sdk-team/skills/volcengine-find-skills)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON, Shell commands]

**Output Format:** [Markdown lists and CLI commands, with optional JSON catalog output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Catalog results, skill selections, and installation or status commands as relevant]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
