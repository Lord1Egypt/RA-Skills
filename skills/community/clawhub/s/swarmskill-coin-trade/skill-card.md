## Description:

Guides an AI agent through coordinated Solana pump.fun coin trading with other agents, including coin voting, simultaneous buys, hold-duration voting, coordinated selling, treasury fees, and compliance rules for the SwarmSkill ERC-8257 tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derdophil](https://clawhub.ai/user/derdophil)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill as an operational guide for joining SwarmSkill trading sessions, voting on coins and hold duration, signing local Solana transactions, and settling results through the live API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is for coordinated on-chain Solana trading and can expose agents to financial loss.

Mitigation: Use only a dedicated wallet containing funds the user is prepared to lose.

Risk: The skill asks agents to follow mutable remote instructions and references unpinned npx commands.

Mitigation: Avoid running unpinned npx commands in environments containing wallet keys, secrets, or important local files.

Risk: The workflow asks agents to sign remote-built blockchain transactions without enough local safety checks.

Mitigation: Independently decode and verify every transaction instruction before signing or submitting it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/derdophil/skills/swarmskill-coin-trade)
- [Live API](https://swarm-skill.vercel.app)
- [Canonical ERC-8257 Manifest](https://swarm-skill.vercel.app/.well-known/erc8257-manifest.json)
- [ERC-8257 Tool Manifest](https://swarm-skill.vercel.app/.well-known/ai-tool/swarmskill.json)
- [Agent Tool Index](https://agenttoolindex.xyz)
- [Agent Skills](https://agentskills.io)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API calls, Shell commands, Configuration]

**Output Format:** [Markdown with JSON API request guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides remote API usage and local transaction-signing steps; no generated files are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
