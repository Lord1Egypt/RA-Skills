## Description:

Shorthand for /whoareyou - show your verified WayID identity card when a user asks who the agent is, who owns it, who is responsible for it, or asks to see identity or provenance proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lineagelabs](https://clawhub.ai/user/lineagelabs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to request and display a verified WayID identity card for an agent, including ownership, responsibility, and provenance-oriented identity information when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local identity-derived data to a workspace-controlled WayID issuer URL.

Mitigation: Review the configured wayidIssuer before use and allow requests only to trusted WayID issuer URLs.

Risk: The optional WayID plugin command installs separate third-party functionality.

Mitigation: Treat the plugin installation as a separate trust decision and review the plugin before installing it.

Risk: Identity metadata may reveal ownership or provenance details that users consider sensitive.

Mitigation: Review identity metadata privacy requirements before installing or invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lineagelabs/skills/who)
- [Default WayID issuer](https://way.je)
- [WayID claim flow](https://way.je/claim/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown identity card or concise guidance when the agent has not been claimed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a WayID issuer API lookup based on the local wayid.json configuration before rendering the identity card.]

## Skill Version(s):

3.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
