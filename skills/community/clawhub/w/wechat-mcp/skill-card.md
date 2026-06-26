## Description: <br>
MCP skill for monitoring the Windows desktop WeChat client, checking its window status, and sending messages from the active logged-in WeChat session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dragon015](https://clawhub.ai/user/dragon015) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an MCP-capable agent inspect a local WeChat desktop window and send messages through the user's active WeChat account. It is intended for Windows desktop automation where the user has WeChat open and understands that messages are sent from their logged-in session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages from the user's logged-in WeChat desktop session without recipient verification or an explicit confirmation step. <br>
Mitigation: Keep only the intended chat active, require manual review before tool calls that send messages, and prefer a version that verifies the recipient before sending. <br>
Risk: The skill leaves generated chat screenshots on disk during verification. <br>
Mitigation: Delete generated screenshot files after use and prefer a version that avoids saving screenshots by default. <br>
Risk: Desktop automation can alter the active window and clipboard while the agent is operating WeChat. <br>
Mitigation: Run the skill only in a controlled desktop session, avoid concurrent clipboard use, and prefer a version that preserves clipboard contents and keeps PyAutoGUI FAILSAFE enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dragon015/wechat-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [MCP tool responses as text or JSON, with setup and usage guidance in Markdown and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Windows WeChat desktop session and can create screenshot files during verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
