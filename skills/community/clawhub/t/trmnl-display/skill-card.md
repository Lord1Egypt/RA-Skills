## Description:

Send concise text, notifications, or updates with optional Markdown and images to a TRMNL e-ink terminal display via webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peetzweg](https://clawhub.ai/user/peetzweg)

### License/Terms of Use:


## Use Case:

ClawHub users and developers use this skill to send short messages, status updates, reminders, and image-backed notes to a TRMNL e-ink display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a writable TRMNL webhook endpoint.

Mitigation: Replace it with the user's own webhook stored as a secret, and rotate or revoke the exposed webhook before use.

Risk: User-provided content is sent to an external TRMNL endpoint.

Mitigation: Do not send passwords, tokens, private reminders, personal data, or internal business information unless that external transmission is acceptable.

## Reference(s):

- [ClawHub TRMNL skill page](https://clawhub.ai/peetzweg/skills/trmnl-display)
- [peetzweg publisher profile](https://clawhub.ai/user/peetzweg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown text and JSON webhook payloads sent with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a title, Markdown-capable text, and an optional fully qualified public image URL.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
