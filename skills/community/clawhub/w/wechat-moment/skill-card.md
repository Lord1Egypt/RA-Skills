## Description:

微信操作手册 helps an agent operate WeChat Moments through coordinate-based desktop actions for opening Moments, browsing posts, scrolling content, and supervised social interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[islandlxl](https://clawhub.ai/user/islandlxl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to guide supervised desktop automation of WeChat Moments, including opening the Moments view, browsing friend updates, scrolling, and interacting with visible content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordinate-based desktop automation can click the wrong UI target when the WeChat window, resolution, or focus differs from the documented setup.

Mitigation: Use only in a supervised session, verify the active WeChat window and coordinates before execution, and adapt coordinates for the current desktop.

Risk: The skill includes message-sending, comment, like, and voice-call actions that may affect other people if triggered without confirmation.

Mitigation: Require immediate human confirmation of the exact recipient, content, and action before sending messages, posting comments, liking content, or placing calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/islandlxl/skills/wechat-moment)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes fixed screen coordinates that may require adaptation for each desktop environment.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
