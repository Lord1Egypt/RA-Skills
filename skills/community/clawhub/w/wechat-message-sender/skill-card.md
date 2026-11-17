## Description:

Automates sending text messages and image or file attachments to WeChat contacts in the macOS WeChat desktop app by controlling the GUI with AppleScript and JXA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeholdon](https://clawhub.ai/user/yeholdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to send one-off or batch text messages and image/file attachments to trusted WeChat contacts from a logged-in macOS WeChat desktop session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe AppleScript construction may mishandle untrusted recipient names, messages, or file paths.

Mitigation: Use only trusted user-supplied values, and update the scripts to pass values to AppleScript as arguments or otherwise safely quote inputs before execution.

Risk: Messages and files are sent immediately without a confirmation step.

Mitigation: Add a confirm-before-send or draft-only mode, especially for external recipients, batch sends, and file attachments.

Risk: Ambiguous WeChat search results can select the wrong recipient.

Mitigation: Use exact, specific contact names and verify the selected chat before sending.

## Reference(s):

- [WeChat Send ClawHub listing](https://clawhub.ai/yeholdon/skills/wechat-message-sender)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and command status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, WeChat for Mac, a visible logged-in WeChat window, and Accessibility permission for node.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
