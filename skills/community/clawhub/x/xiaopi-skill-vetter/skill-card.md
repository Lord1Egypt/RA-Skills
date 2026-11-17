## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-din](https://clawhub.ai/user/a-din)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to review agent skills before installation, document red flags, classify risk, and produce a concise vetting report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example GitHub commands may disclose repository names, paths, or URLs to external GitHub endpoints.

Mitigation: Run the commands only for repositories whose details may be shared with GitHub, and avoid private repository names or sensitive URLs unless disclosure is approved.

Risk: The skill produces conservative vetting guidance that can flag issues requiring human judgment.

Mitigation: Treat the generated report as review support and have a human confirm high-risk findings before installation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a-din/skills/xiaopi-skill-vetter)
- [Publisher profile](https://clawhub.ai/user/a-din)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown vetting report with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code, persistence, or hidden data handling was reported by the authoritative security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
