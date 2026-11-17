## Description:

Security-first skill vetting for AI agents before installing skills from ClawHub, GitHub, or other sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fedrov2025](https://clawhub.ai/user/fedrov2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to review agent skills before installation, identify security red flags, assess permission scope, and document a vetting verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may run the example curl commands against unintended repositories or with private credentials in their environment.

Mitigation: Treat the curl examples as optional and target-specific; fetch only public repositories intended for review and do not paste private tokens or credentials into review commands.

Risk: A checklist-only review can miss subtle malicious behavior or incomplete context in a skill package.

Mitigation: Read all skill files, follow the permission-scope checks, and use scan results or human approval for medium- or high-risk findings before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fedrov2025/skills/skill-vetter-1-0-0)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with checklist guidance, report template, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a human-readable vetting report covering source, author, version, metrics, red flags, permissions, risk level, verdict, and notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
