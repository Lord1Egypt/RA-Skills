## Description:

Automates sending text messages in the macOS WeChat desktop app by controlling the visible WeChat GUI with AppleScript and JXA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clk1st](https://clawhub.ai/user/clk1st)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent to send text-only WeChat messages to specific contacts through the logged-in macOS WeChat desktop app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends real WeChat messages through the user's logged-in macOS WeChat account.

Mitigation: Use it only for non-sensitive messages, with specific contact names, and review message content before routine use.

Risk: Broad macOS UI automation and unsafe scripting could be abused with crafted inputs.

Mitigation: Harden AppleScript argument passing before routine deployment and limit execution to trusted inputs.

Risk: GUI targeting can select the wrong contact or input area when WeChat search results or window placement are ambiguous.

Mitigation: Use exact contact names, keep WeChat visible, and add confirmation before sending.

Risk: The skill can expose message content through local logs or process output.

Mitigation: Reduce logging and avoid using the skill with sensitive message content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clk1st/skills/wechat-send)
- [Publisher profile](https://clawhub.ai/user/clk1st)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only WeChat messages; requires a logged-in, visible WeChat for Mac session and macOS Accessibility permission for node.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
