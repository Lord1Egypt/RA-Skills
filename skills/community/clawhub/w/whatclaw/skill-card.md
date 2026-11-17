## Description:

Manages WhatsApp whitelists to send messages only to approved numbers, track delivery status, and verify OpenClaw connectivity via word-trigger commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[santanu-kumar-prusty](https://clawhub.ai/user/santanu-kumar-prusty)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage approved WhatsApp recipient sets, send text or media messages through OpenClaw only to those sets, and check delivery status for sent messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real WhatsApp messages to whitelisted recipients with limited confirmation before delivery.

Mitigation: Use only with trusted operators and carefully controlled recipient sets; add a preview or confirmation step before sends in higher-risk deployments.

Risk: The skill can send local media files externally when a file path is supplied.

Mitigation: Use non-sensitive media paths and restrict local media access to an approved directory.

Risk: Word-trigger commands may be unsafe in automated contexts where untrusted text can invoke actions.

Mitigation: Avoid wiring untrusted input directly to this skill and require an operator review before message-sending commands run.

Risk: Whitelist and message log data are stored locally in JSON files.

Mitigation: Document retention expectations and set appropriate filesystem permissions for the local data directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/santanu-kumar-prusty/skills/whatclaw)
- [Artifact usage guide](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw CLI, a connected WhatsApp channel, and local JSON storage for whitelist and message status data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
