## Description:

x402janus helps agents scan EVM wallets, inspect approvals, identify drainer risk, prepare revoke transactions, and start monitoring, with paid calls using x402 USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill as a pre-transaction wallet security gate for EVM activity. It returns approval analysis, risk signals, recommendations, revoke transaction data, and monitoring subscription details for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid commands can sign asset-transfer payment authorizations from insufficiently validated server data.

Mitigation: Use a low-balance payment wallet, keep JANUS_API_URL on the official HTTPS endpoint, and avoid paid commands with valuable wallets until x402 asset, recipient, network, and maximum amount are locally validated.

Risk: Monitoring webhooks can expose alerts or trust a reused secret.

Mitigation: Use a unique WEBHOOK_SECRET for this integration and rotate it if reused elsewhere.

Risk: The revoke command can submit a real on-chain transaction when run with --execute.

Mitigation: Use the default dry-run output first, inspect calldata and target addresses, and require explicit operator approval before executing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclaw-consensus-bot/skills/x402janus)
- [Publisher profile](https://clawhub.ai/user/openclaw-consensus-bot)
- [Product homepage](https://x402janus.com)
- [ACP marketplace listing](https://app.virtuals.io/acp/agent-details/14804)
- [Repository metadata link](https://github.com/consensus-hq/agent-pulse)
- [Machine-readable skill documentation endpoint](https://x402janus.com/api/skill-md)
- [x402janus on X](https://x.com/x402janus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON, CSV, table, and transaction-calldata outputs from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan commands use exit codes for automation; paid tiers require a wallet key and USDC on Base.]

## Skill Version(s):

3.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
