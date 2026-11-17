## Description:

Buy live stablecoin, RWA, DeFi, and AI-agent-economy market data for AI agents. Pay-per-call in USDC on Solana via x402 — no accounts, no API keys. Use when you need crypto market metrics, stablecoin peg checks, price snapshots, claim verification, market briefs, or on-demand custom research briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daveabear](https://clawhub.ai/user/daveabear)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use this skill to retrieve paid, current crypto-market data, stablecoin peg checks, price snapshots, and claim verification. They can also request structured or custom research briefs and poll for completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests transfer USDC on Solana, and a custom research brief costs more than ordinary data calls.

Mitigation: Set a spending limit and verify the amount, recipient, network, and USDC mint before signing each payment.

Risk: Claims or research topics submitted to the service may contain confidential information.

Mitigation: Keep private keys out of API requests and omit confidential information from submitted claims and research topics.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/daveabear/skills/rwa-data-api)
- [RWA Data API](https://rwa-data-api.dave-a-bear.workers.dev)
- [RWA Data MCP endpoint](https://rwa-data-mcp.dave-a-bear.workers.dev/mcp)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON market-data responses and text/Markdown briefs; shell-command examples for API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid per-call service; responses include as-of dates, dated sources, FACT/INFERENCE labels, and disclosed fallback status.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
