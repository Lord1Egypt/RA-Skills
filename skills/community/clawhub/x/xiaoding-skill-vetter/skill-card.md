## Description:

Security-first skill vetting for AI agents before installing skills from ClawHub, GitHub, or other sources, checking for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use this skill to review unfamiliar agent skills before installation, checking source, permissions, red flags, and risk level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The vetting report could contain incorrect or misleading security conclusions.

Mitigation: Review the skill files and scanner evidence before acting on the verdict.

Risk: Example GitHub curl commands could be pointed at an unintended repository or used with sensitive credentials.

Mitigation: Confirm repository URLs before running commands and avoid pasting private tokens or credentials into the review process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/xiaoding-skill-vetter)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown checklist and vetting report with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable risk classification, verdict, permissions summary, and notes.]

## Skill Version(s):

1.0.3 (source: server release evidence; SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
