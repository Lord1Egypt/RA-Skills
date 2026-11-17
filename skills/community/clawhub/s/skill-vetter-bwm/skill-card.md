## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to review unknown or third-party skills before installation by checking source trust, code red flags, permission scope, and risk level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to read files while inspecting a candidate skill package.

Mitigation: Constrain file reads to the candidate skill package and supplied release evidence unless a human approves broader review scope.

Risk: The skill may lead an agent to query GitHub repository metadata or raw content while vetting a source.

Mitigation: Review proposed network calls before execution and allow only expected repository metadata or content endpoints for the skill being vetted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blueworldmarketing/skills/skill-vetter-bwm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with checklist items and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source review notes, permission scope, red flags, risk classification, and an install verdict.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
