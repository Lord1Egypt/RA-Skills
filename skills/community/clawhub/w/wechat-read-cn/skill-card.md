## Description:

Reads WeChat contact or group chat history on macOS by driving the desktop client, capturing screenshots, and using agent OCR to extract messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuntong007](https://clawhub.ai/user/chuntong007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve recent or historical WeChat conversation content from a selected contact or group on a logged-in macOS WeChat desktop client. It is intended for reading messages, not sending them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private WeChat messages and can leave screenshots and contact text in temporary files.

Mitigation: Use it only for chats the user is authorized to read, on an account where Accessibility and Screen Recording permissions are acceptable, and remove temporary WeChat read files after use.

Risk: Search results or OCR ambiguity may select or report the wrong conversation.

Mitigation: Confirm the target conversation before relying on extracted content, especially after fallback flows or ambiguous search results.

Risk: The authoritative security verdict marks the release as suspicious and says it needs review before installation.

Mitigation: Review the skill and its permissions before deployment, and limit use to environments where the privacy exposure is acceptable.

## Reference(s):

- [WeChat Read CN ClawHub page](https://clawhub.ai/chuntong007/skills/wechat-read-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown conversation record with inline shell commands and OCR-derived message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes sender direction, timestamps, de-duplicated screenshot content, and may depend on temporary screenshot files created during execution.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
