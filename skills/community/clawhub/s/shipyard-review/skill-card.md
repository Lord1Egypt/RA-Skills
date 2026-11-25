## Description:

Coordinates a full web app review, verifies findings, organizes fixes, reruns checks, and prepares changes for release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipposk](https://clawhub.ai/user/philipposk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review an established web app before release or after substantial changes. It coordinates reviewers, checks findings, guides fixes and verification, and summarizes remaining issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's bare npx tsc command may download and run an unexpected package.

Mitigation: Use a trusted local TypeScript compiler and understand the environment and network access available to the skill before installing or running it.

Risk: The security scan was incomplete, so review results may miss issues or pass despite reported problems.

Mitigation: Review findings independently; the scan covered only part of the skill and its tool-misuse analysis was degraded.

## Reference(s):

- [Shipyard review on ClawHub](https://clawhub.ai/philipposk/skills/shipyard-review)
- [Shipyard installation instructions](https://github.com/philipposk/shipyard/blob/main/INSTALL.md)
- [Review workflows](references/workflows.md)
- [Choosing review areas](references/areas.md)
- [Local production checks and shipping](references/ship.md)
- [Speed checks](references/speed.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Markdown]

**Output Format:** [Markdown findings and guidance, with code changes and release notes as applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect and modify an app, run local checks, and prepare pull requests.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
