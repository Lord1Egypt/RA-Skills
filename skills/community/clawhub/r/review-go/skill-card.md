## Description:

Comprehensive Go backend code review with optional parallel review areas. Use when reviewing changed Go files; detects BubbleTea, Wish SSH, and Prometheus and loads the matching review skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to perform structured reviews of changed Go backend files, detect relevant Go technologies, load matching review guidance, and produce a consolidated review with findings and a verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on separately available companion review skills, so incomplete or untrusted companion skills could affect review quality.

Mitigation: Review and trust the companion skills before relying on the full Go review workflow.

## Reference(s):

- [Review Go on ClawHub](https://clawhub.ai/anderskev/skills/review-go)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown review with severity sections, file-line findings, good patterns, and verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can coordinate sequential or parallel review areas when supported by the agent.]

## Skill Version(s):

1.0.2 (source: server release evidence, created 2026-06-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
