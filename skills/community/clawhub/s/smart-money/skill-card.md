## Description: <br>
Smart Money tracks Ethereum mainnet whale, fund, market-maker, custom-wallet, and liquidity-pool activity and surfaces on-chain trading signals through Antalpha MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to monitor smart-money wallet activity, review whale trading and LP signals, and set up custom wallet alerts. It is intended for on-chain signal tracking and alerting, not custody or transaction execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide agents to create recurring OpenClaw Cron monitoring jobs after custom wallet subscriptions are added. <br>
Mitigation: Require explicit user confirmation before creating any Cron job, review the exact schedule and message, and tell the user how to remove the Cron job and related local state files. <br>
Risk: The skill registers an agent and stores a local API key and monitoring state for later MCP calls. <br>
Mitigation: Store credentials securely, avoid exposing them in prompts or logs, and delete local state files when monitoring is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Smart Money release page](https://clawhub.ai/deanpeng-dotcom/smart-money) <br>
- [Antalpha MCP endpoint](https://mcp-skills.ai.antalpha.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with MCP tool arguments, signal summaries, optional shell commands, and local configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recurring OpenClaw Cron setup guidance and local state-file guidance for custom wallet monitoring.] <br>

## Skill Version(s): <br>
1.2.3 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
