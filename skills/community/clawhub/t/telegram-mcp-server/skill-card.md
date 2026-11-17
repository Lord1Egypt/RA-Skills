## Description:

Guides agents through operating and diagnosing the telegram-mcp MCP server for real Telegram user accounts, including chat/message tool calls, auth failures, lifecycle checks, and multi-account use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aihlp](https://clawhub.ai/user/aihlp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to help agents call and troubleshoot a Telegram MCP server that can read chats and send messages through a real user account. It is intended for setup diagnosis, auth/session handling guidance, and account-specific tool-call routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Telegram MCP tools can read message history and send messages as the selected real Telegram user account.

Mitigation: Install and enable the skill only for agents that intentionally need this access, and review requested chat/message actions before use.

Risk: Telegram session strings, API IDs, and API hashes are sensitive credentials.

Mitigation: Keep TELEGRAM_SESSION_STRING, TELEGRAM_API_ID, and TELEGRAM_API_HASH private, avoid printing them in logs or responses, and require human-attended QR login for new or expired sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aihlp/skills/telegram-mcp-server)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
