## Description:

Operates TraeCN through TRAECNclaw's focused stdio MCP tools for sending or stopping work, selecting workspace/model/mode/conversation context, managing settings and conversations, and resolving exceptional questions or command approvals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckycat133](https://clawhub.ai/user/luckycat133)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MCP-capable agents use this skill to operate TraeCN through TRAECNclaw, delegate coding work, manage TraeCN context and settings, and handle exceptional approvals or questions through a focused tool surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher can load server code from environment-influenced locations.

Mitigation: Use a fixed, verified absolute server path or a trusted package installation, and control the MCP client's working directory, NODE_PATH, and PATH before installation.

Risk: Gateway access could expose TraeCN control if bound beyond loopback or if its token is mishandled.

Mitigation: Keep TRAECN_GATEWAY_HOST on 127.0.0.1 unless remote access is secured, and never print, log, or persist TRAECN_GATEWAY_TOKEN.

Risk: Command approvals, settings changes, stop-generation requests, and conversation deletion can have high impact.

Mitigation: Require explicit user intent, re-read exact commands or conversation identifiers, acknowledge documented risks, and preserve audit reasons for high-impact decisions.

## Reference(s):

- [TRAECNclaw MCP Skill Page](https://clawhub.ai/luckycat133/skills/traecnclaw-mcp)
- [MCP surface](references/mcp-surface.md)
- [MCP tool contracts](references/mcp-tool-contracts.json)
- [MCP call examples](references/mcp-call-examples.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and a matching TRAECNclaw server; exposes a focused 20-tool stdio MCP surface.]

## Skill Version(s):

0.6.0 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
