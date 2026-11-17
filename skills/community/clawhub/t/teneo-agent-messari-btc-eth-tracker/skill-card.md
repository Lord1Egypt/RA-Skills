## Description:

Messari BTC & ETH Tracker provides Bitcoin and Ethereum market analytics from Messari data through a Teneo Protocol agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev)

### License/Terms of Use:

MIT-0

## Use Case:

External traders, analysts, researchers, and developers use this agent to retrieve BTC and ETH market metrics, ROI data, supply information, and all-time-high analytics for portfolio review or analytics pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a funded wallet for automatic USDC payments without clear local limits or per-transaction approval.

Mitigation: Use an isolated low-balance wallet, avoid unlimited token approvals, and confirm the agent identity, payment amount, recipient, chain, and approval flow before signing any transaction.

Risk: SDK or package substitution could affect wallet or payment behavior.

Mitigation: Verify the SDK source and package versions before installation and review the installed dependency tree before use.

## Reference(s):

- [Skill page on ClawHub](https://clawhub.ai/teneoprotocoldev/skills/teneo-agent-messari-btc-eth-tracker)
- [Teneo Protocol](https://teneo-protocol.ai)
- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [@teneo-protocol/sdk npm package](https://www.npmjs.com/package/@teneo-protocol/sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, a supported wallet, and USDC on Base, Peaq, or Avalanche for paid agent access.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
