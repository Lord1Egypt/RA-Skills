## Description:

RCS Message, the upgraded 5G intelligent SMS, supports mass sending and forwarding of text and template messages directly via phone numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longbiao515](https://clawhub.ai/user/longbiao515)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send SMS, RCS, AIM, MMS, and fallback SMS messages from natural-language requests or command-line calls. It supports template messages, recipient validation, dry-run validation, and rate-limited group sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mass-send real external SMS/RCS messages through the configured provider.

Mitigation: Review recipient lists and message content before execution, use dry-run validation when possible, and avoid bulk sends unless they are intentional.

Risk: API credentials may be stored locally for reuse.

Mitigation: Use non-shared credentials, prefer environment-based secret management, and remove or harden local plaintext credential storage before sensitive use.

## Reference(s):

- [ClawHub rcs-message Skill Page](https://clawhub.ai/longbiao515/skills/rcs-message)
- [5G Messaging API Server](https://5g.fontdo.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send real external SMS/RCS messages when configured with valid provider credentials; dry-run mode validates inputs without sending.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
