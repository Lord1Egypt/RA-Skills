## Description: <br>
Monitor WeChat window status, capture screenshots, search contacts, and send messages on Windows through desktop automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow builders use this skill to let an agent check WeChat desktop status, capture the WeChat window, search contacts, and send messages from a live Windows session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can send messages from the user's live WeChat desktop session without built-in recipient or content confirmation. <br>
Mitigation: Require manual approval before each message send, and verify the active chat and exact message content before execution. <br>
Risk: Screenshots of the WeChat window can expose private conversations, contacts, or other sensitive desktop content. <br>
Mitigation: Use screenshot tools only in sessions without sensitive conversations visible, and avoid running the skill around private contacts or confidential chats. <br>


## Reference(s): <br>
- [Windows WeChat MCP skill definition](artifact/SKILL.md) <br>
- [Windows WeChat MCP server script](artifact/scripts/server.py) <br>
- [ClawHub release page](https://clawhub.ai/openlark/windows-wechat-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with Python examples; MCP tool calls return JSON-like status objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open Windows WeChat desktop window and local Python automation dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
