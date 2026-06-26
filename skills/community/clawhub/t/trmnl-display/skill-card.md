## Description: <br>
Send concise text, notifications, or updates with optional Markdown and images to a TRMNL e-ink terminal display via webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peetzweg](https://clawhub.ai/user/peetzweg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to send short messages, status updates, reminders, Markdown-formatted text, and public image URLs to a TRMNL e-ink display. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends content to a hard-coded TRMNL webhook whose ownership is not shown. <br>
Mitigation: Install only if the webhook is recognized as yours or you are comfortable sending display content to that endpoint. <br>
Risk: Private reminders, credentials, internal status, or sensitive image links could be sent to an unintended display or account. <br>
Mitigation: Avoid sending sensitive content until the destination is user-configurable and clearly confirmed before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peetzweg/trmnl-display) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise TRMNL display content with title, text, and optional public image URL fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
