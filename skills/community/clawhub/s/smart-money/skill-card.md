## Description:

Smart Money helps agents track Ethereum smart-money wallets, including whale, fund, market-maker, custom wallet, and liquidity-pool activity, through Antalpha MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query on-chain wallet signals, inspect watched Ethereum addresses, manage a small custom watchlist, and set up recurring checks for new high-priority activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an agent API key locally for later MCP calls.

Mitigation: Store the credential in a restricted local path, avoid exposing it in logs or prompts, and remove it when the skill is no longer used.

Risk: Monitored wallet addresses are sent to Antalpha's MCP service.

Mitigation: Only add addresses the user is comfortable sharing with the service, and remove watched addresses when monitoring is no longer needed.

Risk: The skill directs agents to create recurring Cron checks about every 15 minutes after adding a custom address.

Mitigation: Create recurring checks only when the user explicitly wants ongoing monitoring, and verify how to inspect, disable, and remove the Cron job before enabling it.

## Reference(s):

- [Smart Money ClawHub listing](https://clawhub.ai/deanpeng-dotcom/skills/smart-money)
- [Antalpha MCP endpoint](https://mcp-skills.ai.antalpha.com/mcp)
- [Publisher profile](https://clawhub.ai/user/deanpeng-dotcom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text summaries with MCP tool-call arguments, JSON configuration examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet signal levels, token or pool activity summaries, transaction references, local agent credential storage guidance, and recurring Cron monitoring commands.]

## Skill Version(s):

1.2.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
