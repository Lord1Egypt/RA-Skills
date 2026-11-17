## Description:

An unofficial Supremacy 1914 self-play war cabinet that briefs the player through an interactive president-and-ministers experience using their own Ultimate client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pixel-agents](https://clawhub.ai/user/pixel-agents)

### License/Terms of Use:

MIT-0

## Use Case:

Players use the skill with a self-hosted Supremacy 1914 MCP server to get briefings and plans for their own game. The agent proposes game changes for the player to approve.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separately downloaded MCP server whose behavior has not been verified.

Mitigation: Review and pin the external server code before running it.

Risk: Game credentials or the MCP token could be exposed if access to the server is not protected.

Mitigation: Protect credentials and the MCP token, keep access local or use HTTPS remotely, and leave writes disabled until ready to approve game actions.

Risk: Enabling writes may allow game changes before the player is ready to approve them.

Mitigation: Keep writes disabled until ready to approve game actions, and require confirmation for mutating tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pixel-agents/skills/supremacy1914-cabinet)
- [MCP project repository linked by the skill](https://github.com/Pixel-Agents/supremacy1914-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, API Calls]

**Output Format:** [Conversational briefings and proposed MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutating actions require player approval.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
