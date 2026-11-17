## Description:

WeChat MCP lets an agent check a Windows desktop WeChat window and send messages through MCP or direct Python desktop automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragon015](https://clawhub.ai/user/dragon015)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to expose Windows desktop WeChat status checks and current-chat message sending to an agent through MCP or direct Python calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send messages from the active desktop WeChat session without reliable recipient verification or a final confirmation step.

Mitigation: Add recipient verification and require explicit user confirmation before sending each message.

Risk: The skill can activate WeChat, overwrite the clipboard, paste text, and press Enter in the local desktop session.

Mitigation: Run it only in a least-privileged desktop environment dedicated to the intended WeChat account and workflow.

Risk: Diagnostic screenshots of chat windows can be written to disk.

Mitigation: Make screenshot capture opt-in and clean up screenshot files after diagnostics are complete.

Risk: Dependencies are specified with lower bounds instead of pinned versions.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dragon015/skills/wechat-mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [MCP text content with JSON status payloads or plain text send-result messages; diagnostic screenshots may be saved as PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active Windows desktop WeChat session and local GUI automation access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
