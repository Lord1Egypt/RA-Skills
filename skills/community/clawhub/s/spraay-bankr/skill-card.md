## Description:

Spraay × Bankr guides agents through Bankr-funded Spraay batch payouts for airdrops, fee splits, payroll, and ERC-20 distributions with validation, estimates, and explicit confirmation before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with Bankr agent wallets use this skill to prepare Spraay batch payouts for token airdrops, creator or trading fee splits, USDC payroll, and other ERC-20 distributions. The skill helps plan, validate, estimate, and summarize payouts before funds move.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect token, chain, recipient address, amount, fee, or transaction detail could cause a real crypto payout to be wrong.

Mitigation: Verify token, chain, recipient addresses, amounts, fees, and transaction details before confirming execution.

Risk: Funds could move before the user has reviewed the payout.

Mitigation: Always validate and estimate the batch first, show the user the full payout details, and require explicit confirmation before execution.

Risk: The Bankr API key controls real funds.

Mitigation: Keep the key limited to Bankr use and do not echo, log, or send it outside Bankr.

Risk: Fabricated or unverified recipient data could direct payouts to the wrong addresses.

Mitigation: Use recipient lists supplied by the user or another verifiable source, never invent addresses or amounts, and fix validation rejects before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plagtech/skills/spraay-bankr)
- [Spraay gateway](https://gateway.spraay.app)
- [Spraay documentation](https://docs.spraay.app)
- [Spraay live dashboard](https://live.spraay.app)
- [Bankr documentation](https://docs.bankr.bot)
- [Bankr skills repository](https://github.com/BankrBot/skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with endpoint paths, API call plans, validation steps, estimates, confirmation prompts, and transaction summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports real-money payout planning; output should include token, chain, recipient count, totals, estimated fees, and confirmation status before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
