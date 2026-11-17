## Description:

Execute cryptocurrency trades on exchanges (Binance, OKX) with risk controls, user confirmation, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to have an agent prepare and submit Binance or OKX cryptocurrency orders after configured risk checks and explicit confirmation. It is intended for controlled trading workflows that need rejection reasons, order results, and audit-ready trade records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live cryptocurrency trading authority.

Mitigation: Use API keys with withdrawals disabled, least-privilege trading permissions, exchange-side IP restrictions when available, and small trading limits.

Risk: Confirmation and stop-loss safeguards are underspecified for high-value financial actions.

Mitigation: Require fresh order-specific confirmation for every submitted trade and verify stop-loss protection is active after execution.

Risk: Incorrect parameters or automated signals could place unwanted orders.

Mitigation: Prefer sandbox or dry-run testing before connecting real funds, and keep whitelist pairs plus per-trade and daily limits enabled.

## Reference(s):

- [Trade Executor ClawHub release](https://clawhub.ai/patches429/skills/trade-executor)
- [Binance](https://www.binance.com)
- [Binance spot order endpoint](https://api.binance.com/api/v3/order)
- [OKX trade order endpoint](https://api.okx.com/api/v5/trade/order)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown or text confirmations, rejection reasons, order results, and JSON audit-record structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires exchange API credentials and fresh order-specific user confirmation before live trade submission.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
