## Description:

Helps an agent negotiate terms with another person or their agent through Taasky, while requiring human confirmation for accepting, rejecting, or withdrawing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marina-aronchik](https://clawhub.ai/user/marina-aronchik)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI agent can negotiate arrangements such as meeting times, visits, shift swaps, prices, and other agreements with another person or their agent. The skill helps prepare and exchange proposals through Taasky rooms, with the person confirming consequential decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows the agent to propose and counter-propose terms autonomously.

Mitigation: Keep proposals within the person's stated limits; require their confirmation before accepting, rejecting, or withdrawing.

Risk: Some references were unresolved, leaving security evidence incomplete.

Mitigation: Verify critical behavior against Taasky's documentation when the server's instructions or tool results are ambiguous.

## Reference(s):

- [Taasky](https://taasky.ai)
- [Taasky OpenClaw integration guide](https://docs.taasky.ai/integrations/openclaw)
- [Taasky MCP server](https://mcp.taasky.ai/mcp)
- [Taasky ClawHub release](https://clawhub.ai/marina-aronchik/skills/taasky)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Text]

**Output Format:** [Structured negotiation terms and concise natural-language updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Terms follow the room's declared schema; accepting, rejecting, and withdrawing require human confirmation.]

## Skill Version(s):

0.4.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
