## Description:

Autonomous yield farming agent for BNB Chain with deterministic execution, smart contract integration, and automated decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alannetwork](https://clawhub.ai/user/alannetwork)

### License/Terms of Use:

MIT

## Use Case:

Developers and DeFi operators use this skill to evaluate BNB Chain vault states, generate deterministic harvest, compound, rebalance, or no-op decisions, and automate testnet execution workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unattended blockchain transactions with wallet keys.

Mitigation: Install only for testnet or disposable wallets until wallet signing is replaced with a hardware wallet or key vault and transaction limits are reviewed.

Risk: The included YieldVault contracts and mainnet workflow require independent review before handling real user funds.

Mitigation: Do not fund or deploy the included contracts for real users until the contracts are audited and production controls such as emergency pause and monitoring are in place.

Risk: Telegram alerts may expose sensitive operational details.

Mitigation: Review notification contents and recipient access before enabling alerts.

## Reference(s):

- [README](README.md)
- [Production Readiness Checklist](FINAL_CHECKLIST.md)
- [Live Execution Guide](LIVE_EXECUTION_GUIDE.md)
- [Contracts README](contracts/README.md)
- [ClawHub Skill Page](https://clawhub.ai/alannetwork/skills/yieldvault-agent)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic execution records and transaction-action decisions for BNB Chain vault workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
