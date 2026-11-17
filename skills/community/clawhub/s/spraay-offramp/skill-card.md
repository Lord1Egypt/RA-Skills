## Description:

Guides batch funding of Paycrest off-ramp payouts through a single Spraay transaction using USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and payout operators use this skill to prepare, check, and execute batch USDC off-ramp payments to mobile money or bank recipients in Kenya, Nigeria, Uganda, and Tanzania.

### Deployment Geography for Use:

Global; supported payout destinations are Kenya, Nigeria, Uganda, and Tanzania.

## Known Risks and Mitigations:

Risk: A payout batch can transfer real funds to incorrect recipients or for incorrect amounts.

Mitigation: Start with dry-run mode, then verify each recipient and amount before using --execute; dry runs still create Paycrest orders.

Risk: Exposure of the Paycrest API secret or wallet private key could compromise production financial credentials.

Mitigation: Protect these credentials as production secrets and never commit them to source control.

Risk: Running an external adapter can expose funded payout batches to software supply-chain risk.

Mitigation: Review or pin the adapter source before funding large batches.

## Reference(s):

- [Spraay Off-Ramp on ClawHub](https://clawhub.ai/plagtech/skills/spraay-offramp)
- [Paycrest documentation](https://docs.paycrest.io)
- [Spraay documentation](https://docs.spraay.app)
- [Spraay off-ramp adapter on npm](https://www.npmjs.com/package/spraay-offramp-adapter)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run, execution, and payout-status guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
