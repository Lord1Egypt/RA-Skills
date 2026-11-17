## Description:

Access Telegram data via MCP using the telebiz-tt browser client. Lists chats, reads messages, searches, manages folders, and sends messages through an authenticated Telegram session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acastellana](https://clawhub.ai/user/acastellana)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect an MCP-capable agent to an authenticated Telegram session for reading chats and messages, searching Telegram content, organizing folders, and sending or managing messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A logged-in Telegram account may be exposed through unauthenticated local HTTP or WebSocket services.

Mitigation: Bind services to loopback, add strong authentication, remove wildcard CORS, and avoid running the skill on shared or untrusted machines or networks.

Risk: The skill can send, forward, delete, and organize Telegram content through the active browser session.

Mitigation: Require explicit review or confirmation before destructive or high-volume operations, and prefer reversible actions where possible.

Risk: Telegram flood protection or unintended bulk actions may be triggered by excessive tool calls.

Mitigation: Follow the documented limits of 20 calls per request, 30 calls per minute, at least 500 ms between calls, and 1 second for heavy operations.

Risk: Documented upstream behavior for batch folder updates and entity linking is unreliable.

Mitigation: Use sequential add-to-folder calls and avoid relying on linkEntityToChat until the upstream contract is stable.

Risk: Dependency issues may remain until packages are reviewed and updated.

Mitigation: Update vulnerable dependencies before deployment and re-run security review after dependency changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acastellana/skills/telebiz-mcp-skill)
- [Telebiz web app](https://telebiz.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool responses as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Telegram browser session and local MCP or HTTP relay configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
