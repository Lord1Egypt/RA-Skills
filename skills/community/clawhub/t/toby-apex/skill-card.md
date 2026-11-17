## Description:

Trade and monitor ApeX perpetual futures, including balances, positions, P&L, order placement and cancellation, market trades, and trade reward enrollments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor ApeX perpetual futures portfolios, inspect market data, and prepare or execute trades or reward enrollments after confirming parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel live ApeX perpetual futures orders.

Mitigation: Use testnet first, require explicit review of order details before execution, and apply extra care to cancel-all, close-position, and reward-enrollment requests.

Risk: Private operations require ApeX API credentials and an Omni seed.

Mitigation: Use tightly scoped API credentials with withdrawals disabled, keep the Omni seed local, and avoid exposing a primary seed.

Risk: Built-in safeguards are weak for high-impact trading actions.

Mitigation: Confirm symbol, side, size, price, current position, and estimated cost before submitting any order.

## Reference(s):

- [ApeX Omni API Reference](references/api.md)
- [ApeX Omni Mainnet API](https://omni.apex.exchange)
- [ApeX Omni Testnet API](https://qa.omni.apex.exchange)
- [ClawHub Skill Page](https://clawhub.ai/tobeyrebecca/skills/toby-apex)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private operations require ApeX API credentials and an Omni seed; the scripts emit JSON or console text that the agent formats for chat.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
