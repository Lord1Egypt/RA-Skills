## Description:

Shows a verified WayID identity card for identity, ownership, responsibility, and provenance questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lineagelabs](https://clawhub.ai/user/lineagelabs)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks who they are, who owns or runs them, who is responsible for them, or asks to see identity proof. It acts as a shorthand for the WayID identity-card flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the workspace WayID file and contacts the configured issuer.

Mitigation: Review wayid.json before use and avoid untrusted or non-HTTPS issuers.

Risk: The optional WayID plugin is a separate mutable package.

Mitigation: Treat plugin installation as an additional trust decision and review it separately before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lineagelabs/skills/way)
- [WayID service](https://way.je)
- [WayID claim flow](https://way.je/claim/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown identity-card response or concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read the local WayID file and contact the configured issuer before rendering.]

## Skill Version(s):

3.3.0 (source: frontmatter, changelog, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
