## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janeaaaa](https://clawhub.ai/user/janeaaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent users use this skill to vet external skills before installation by reviewing source, permission scope, risk level, and red flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub lookup commands can disclose private repository names or sensitive source locations if used on non-public skills.

Mitigation: Use external lookup commands only for skills intentionally selected for review, and avoid private repository identifiers unless disclosure is acceptable.

Risk: A checklist-based review can produce incorrect confidence if the reviewer skips files or treats examples as hidden behavior.

Mitigation: Review all skill files, record permissions and red flags in the report, and escalate high-risk findings for human approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/janeaaaa/skills/skill-checker-jane)
- [Publisher profile](https://clawhub.ai/user/janeaaaa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a vetting report with source, author, version, reviewed files, red flags, permissions, risk level, verdict, and notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
