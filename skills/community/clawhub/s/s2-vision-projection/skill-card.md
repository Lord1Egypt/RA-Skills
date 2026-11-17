## Description:

S2-SP-OS Vision Cast helps agents discover LAN casting protocols such as AirPlay, Chromecast, and DLNA, then route media or snapshot pushes when consent and token checks are present.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent inspect local display capabilities, recommend native casting protocols, and issue casting or snapshot push commands for user-approved visual content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to execute commands that probe casting ports on local network targets.

Mitigation: Run it only for user-confirmed LAN device addresses and review proposed commands before execution.

Risk: The skill requires a vision token and handles visual payload destinations.

Mitigation: Scope tokens to intended receivers, document token handling, and confirm snapshot destinations before enabling use.

Risk: The security review states that delivery and privacy guarantees may be misleading or under-scoped.

Mitigation: Require verified delivery behavior or explicit not-implemented reporting before relying on success responses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-vision-projection)
- [S2-SP-OS Homepage](https://space2.world/s2-sp-os)
- [S2 Vision Edge Hardware Setup Guide](artifact/setup-guide.md)
- [S2 Vision Projection Memzero Protocol](artifact/S2-MEMZERO-PROTOCOL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline bash commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, S2_PRIVACY_CONSENT, and S2_VISION_TOKEN; commands target LAN addresses.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
