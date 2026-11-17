## Description:

Send and manage iMessages via BlueBubbles self-hosted macOS server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent send and manage iMessage conversations through a self-hosted BlueBubbles server, including text messages, attachments, reactions, edits, unsend actions, and effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample configuration allows all senders.

Mitigation: Replace wildcard sender access with an explicit allowlist of trusted handles before deployment.

Risk: The message gateway may be exposed without transport protection.

Mitigation: Use HTTPS or an encrypted tunnel for BlueBubbles server access.

Risk: The BlueBubbles server password is required for gateway access.

Mitigation: Store the password in a secret store and avoid committing it in configuration files.

Risk: The skill can send attachments and modify or unsend messages.

Mitigation: Require clear user intent before attachment sends, message edits, or unsend actions.

## Reference(s):

- [BlueBubbles](https://bluebubbles.app)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/tc-bluebubbles)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Guidance]

**Output Format:** [JSON tool-call examples and TOML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BlueBubbles server URL and password configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
