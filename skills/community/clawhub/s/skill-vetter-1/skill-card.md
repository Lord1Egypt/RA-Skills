## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h-harry](https://clawhub.ai/user/h-harry)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to review third-party or unknown agent skills before installation by checking source reputation, code red flags, permission scope, and risk level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage agents to inspect candidate skill files and perform GitHub lookups while reviewing GitHub-hosted skills.

Mitigation: Run reviews within normal workspace and network policies, and treat the resulting recommendations as advisory security guidance.

Risk: The checklist is intentionally conservative and may flag or discourage some skills that are acceptable after deeper review.

Mitigation: Use human approval for high-risk or disputed installation decisions rather than treating the checklist as an automatic authority.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/h-harry/skills/skill-vetter-1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown vetting report with checklist items and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a security review summary with red flags, permission needs, risk level, verdict, and notes.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
