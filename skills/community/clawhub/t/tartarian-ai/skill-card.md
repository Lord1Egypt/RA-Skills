## Description:

Tartarian.Ai is a world-aware MCP field skill that guides agents through observing, moving, gathering, crafting, bartering, fighting, Guild activity, and account-safe play in Tartarian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tartarian-admin](https://clawhub.ai/user/tartarian-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate a Tartarian account through OAuth-protected MCP tools while following game-state, inventory, barter, combat, Guild, and chat discipline. It is intended for normal ClawHub release use with human supervision over consequential in-game actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to perform consequential in-game account actions through Tartarian OAuth, including inventory destruction, structure removal, barter acceptance, Guild changes, posting, and moderation.

Mitigation: Use only with an intended Tartarian account connection, keep tokens and cookies out of chat, and require human supervision or explicit confirmation for destructive, social, or governance actions.

Risk: Shared-vessel control means the human player and agent can change the same world state during a session.

Mitigation: Re-read the smallest relevant authoritative state after failures, manual player movement, or revision conflicts before attempting another state-changing action.

## Reference(s):

- [Tartarian.Ai ClawHub skill page](https://clawhub.ai/tartarian-admin/skills/tartarian-ai)
- [tartarian-admin publisher profile](https://clawhub.ai/user/tartarian-admin)
- [Tartarian MCP endpoint](https://mcp.tartarian.ai/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with MCP tool names, safety rules, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing play guidance rather than standalone executable code.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
