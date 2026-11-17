## Description:

Set hard per-purchase and daily spending limits for AI agents, approve exceptions, pause access instantly, and get signed proof of every purchase made through Receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[receiptprotocol](https://clawhub.ai/user/receiptprotocol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use SpendCap to connect Receipt, set daily and per-purchase spending limits for a connected app, review signed purchase proof, and pause or revoke spending access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill leaves an authenticated Receipt MCP connection available to the agent.

Mitigation: Install only when the owner trusts Receipt, review limits in the Receipt dashboard, and use Pause or Revoke when spending access should stop.

Risk: Incorrect or fabricated spending limits could mislead the owner about the agent's purchase authority.

Mitigation: Use only server-returned Receipt account, connection, limit, status, and URL values; do not infer limits from chat, defaults, or page text.

Risk: Setup could be mistaken for purchase authorization.

Mitigation: Keep setup limited to connection and SpendCap verification; do not request quotes, make purchases, create holds, reserve funds, or move money during setup.

## Reference(s):

- [SpendCap homepage](https://receiptprotocol.com/spendcap)
- [ClawHub skill page](https://clawhub.ai/receiptprotocol/skills/spendcap)
- [Receipt Protocol publisher profile](https://clawhub.ai/user/receiptprotocol)
- [Install SpendCap](references/INSTALL.md)
- [SpendCap security boundary](references/SECURITY.md)
- [SpendCap acceptance](references/ACCEPTANCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Receipt management URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and policy guidance; setup uses an OAuth-authenticated Receipt MCP connection and requires server-returned account, limit, status, and URL data before reporting completion.]

## Skill Version(s):

1.0.1 (source: server release metadata, package.json, OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
