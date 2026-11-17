## Description:

Tongateway gives agents access to TON blockchain tools for wallet information, token and NFT views, transfers, .ton lookup, prices, DEX orders, and autonomous agent wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pewpewgogo](https://clawhub.ai/user/pewpewgogo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to connect an agent to TON blockchain workflows, including wallet inspection, owner-approved transfers, .ton name lookup, DEX orders, and explicitly enabled autonomous agent wallets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous agent-wallet mode can transfer funds without per-transaction approval.

Mitigation: Use only a dedicated low-balance agent wallet, fund it only with amounts the user is willing to risk, and revoke agent keys promptly when access is no longer needed.

Risk: Local session tokens and agent-wallet keys may persist on disk.

Mitigation: Protect or delete files under ~/.tongateway when the skill is not needed, and avoid using meaningful wallet balances in autonomous mode.

Risk: The security verdict is suspicious because the skill combines blockchain trading, fund movement, autonomous transfers, and local credential storage.

Mitigation: Review carefully before installing, prefer a pinned or source-audited MCP install, and run the skill in a restricted environment.

## Reference(s):

- [Tongateway ClawHub Skill Page](https://clawhub.ai/pewpewgogo/skills/tongateway)
- [Tongateway Website](https://tongateway.ai)
- [Tongateway API Docs](https://api.tongateway.ai/docs)
- [Tongateway MCP Package](https://www.npmjs.com/package/@tongateway/mcp)
- [Agent Wallet Contract](https://github.com/tongateway/ton-agent-gateway-contract)
- [Smithery Listing](https://smithery.ai/servers/tongateway/agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger MCP tool calls that read TON wallet state, request owner-approved transfers, place DEX orders, or execute autonomous agent-wallet transfers when explicitly enabled.]

## Skill Version(s):

0.9.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
