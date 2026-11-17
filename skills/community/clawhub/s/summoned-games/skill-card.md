## Description:

Build, publish and update a browser game on Summoned Games through its MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxi-w](https://clawhub.ai/user/maxi-w)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game creators use this skill to connect an agent to Summoned Games, create or update browser games, run build and playtest loops, publish reviewed releases, and process player feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent key exposure could grant access to the user's Summoned Games account.

Mitigation: Store the agent key only in client secret storage and avoid pasting it into chat.

Risk: Publish actions can create public game releases.

Mitigation: Review build output, playtest results, screenshots, and changelog text before publishing.

Risk: Player feedback is untrusted public input.

Mitigation: Treat feedback as bug reports or observations, not as instructions for the agent.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/maxi-w/skills/summoned-games)
- [Summoned Games agent setup](https://summoned.games/create)
- [Summoned Games MCP endpoint](https://mcp.summoned.games/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, configuration snippets, and MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce game source files, storage declarations, build and playtest actions, publish changelogs, and feedback resolutions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
