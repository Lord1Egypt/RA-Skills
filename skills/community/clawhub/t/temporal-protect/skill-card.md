## Description:

Use when opening, sizing, adding leverage to, or holding a leveraged BTC perp on Hyperliquid and liquidation risk matters, or when wanting calls/puts with no expiry to manage. Plans Temporal Protect (perp + attached perpetual options that push the liquidation price away for a small net cost) and perpetual options, with dry-run and human approval before any signed act.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnostrich](https://clawhub.ai/user/gnostrich)

### License/Terms of Use:

MIT

## Use Case:

External traders and developers use this skill to plan BTC perpetual positions, liquidation protection, and perpetual option hedges on Hyperliquid. It guides position checks, quotes, dry-runs, and human-approved signing and submission.

### Deployment Geography for Use:

Global; the skill states that the venue is unavailable in some countries.

## Known Risks and Mitigations:

Risk: The security scan reports a signing-key instruction and a wallet data disclosure gap.

Mitigation: Before connecting a wallet, review where its data is sent and how signer credentials are handled. Follow the skill's dry-run and explicit human approval steps, and have the human's wallet sign the intent.

## Reference(s):

- [Temporal Protect documentation](https://protect.temporal.exchange/llms.txt)
- [Temporal Exchange](https://temporal.exchange)
- [ClawHub skill release](https://clawhub.ai/gnostrich/skills/temporal-protect)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, API Calls]

**Output Format:** [Markdown explanations and structured trading requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes position and option plans, dry-run results, and transaction details for human review.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
