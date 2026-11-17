## Description:

Create Solana-based USDC subscription checkout URLs with encoded parameters using the Tributary Payments SDK's subscription session manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xeroc](https://clawhub.ai/user/xeroc)

### License/Terms of Use:


## Use Case:

Developers use this skill to create Lando checkout URLs for USDC subscription payments on Solana, including encoded session parameters, payment frequency, tracking IDs, and redirect handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring payments may be enabled without enough user awareness, especially when autoRenew is used.

Mitigation: Require explicit customer opt-in for autoRenew and document cancellation and revocation paths before using the generated checkout flow.

Risk: Checkout URLs, tracking IDs, memos, and line items can expose personal data or secrets.

Mitigation: Keep personal data and secrets out of URL parameters, tracking IDs, memos, and line item descriptions.

Risk: Incorrect or unverified payment domains, SDK packages, or gateway public keys could redirect or authorize payments incorrectly.

Mitigation: Independently verify the Tributary/Lando domains, SDK package names, and fixed gateway public key before following the integration guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xeroc/skills/solana-payments)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces checkout URL construction guidance and integration examples; payment domains, SDK packages, gateway keys, and customer consent should be verified before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
