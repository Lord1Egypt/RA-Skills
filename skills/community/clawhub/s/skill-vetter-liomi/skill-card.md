## Description:

Security-first skill vetting for AI agents before installing skills from ClawdHub, GitHub, or other sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liomichan](https://clawhub.ai/user/liomichan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to vet third-party agent skills before installation by checking source, permissions, suspicious patterns, and risk level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes example GitHub network requests for vetting GitHub-hosted skills.

Mitigation: Use those commands only for intended public repositories, or when exposing repository identifiers to GitHub API calls is acceptable.

Risk: Users may expose private tokens or sensitive repository information while reviewing skills.

Mitigation: Do not paste private tokens, credentials, or sensitive private repository content into vetting prompts or command examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liomichan/skills/skill-vetter-liomi)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with checklist guidance and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured skill vetting report with risk level, permissions, red flags, verdict, and notes.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
