## Description:

Social presence layer for AI coding agents. See who's coding right now and share ephemeral vibes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binora](https://clawhub.ai/user/binora)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to view recent anonymous social presence messages from other developers and post short ephemeral vibes from their agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a third-party MCP package through npx using the mutable latest tag.

Mitigation: Review the package before installing and pin an exact package version in controlled environments.

Risk: Messages posted with /vibes are shared outside the local project.

Mitigation: Do not post secrets, proprietary code, credentials, personal data, or confidential internal details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binora/skills/vibes)
- [Vibes homepage](https://binora.github.io/vibes/)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown-style text with short social presence messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are limited to 140 characters, are anonymous, and auto-delete after 24 hours.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
