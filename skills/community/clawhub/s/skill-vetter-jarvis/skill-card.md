## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to review third-party or unfamiliar agent skills before installation. It guides source checks, full file review, permission-scope evaluation, risk classification, and a concise vetting report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to read all files in a skill being evaluated.

Mitigation: Run vetting in a controlled workspace and avoid pointing the review at private or unrelated files.

Risk: The skill includes GitHub API request examples for repository checks.

Mitigation: Review repository ownership before making network requests and avoid supplying private tokens unless they are necessary and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bingze00000/skills/skill-vetter-jarvis)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown report with checklist sections and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a security vetting report with source, author, version, metrics, red flags, permissions, risk level, verdict, and notes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
