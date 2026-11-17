## Description:

Helps an agent pay Coinbase payment links and Bitrefill invoices with supported cryptocurrency, and make x402 payments from a prepaid Rozo balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnmuggle](https://clawhub.ai/user/shawnmuggle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and manage cryptocurrency payments for supported Coinbase or Bitrefill invoices, or to pay supported x402 endpoints from a prepaid Rozo balance. It provides payment options, command examples, and payment status guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan reports that several bundled scripts were only partly analyzed, so it cannot establish that the artifact is safe.

Mitigation: Treat the release as unverified and obtain a version-pinned, integrity-checked package source before considering installation.

Risk: The scan reports shielded Zcash payment support that is not declared in the skill metadata.

Mitigation: Seek clarification or removal of the undeclared Zcash route before using the skill.

Risk: The scan reports default credential-derived tracking and repeated examples that use an unpinned package.

Mitigation: Seek clear opt-in handling for attribution and use a version-pinned, integrity-checked package source.

## Reference(s):

- [OpenRouter credits page](https://openrouter.ai/settings/credits)
- [Rozo ZEC checkout information](https://checkout.rozo.ai/zec)
- [ClawHub release page](https://clawhub.ai/shawnmuggle/skills/rozo-checkout)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [CLI text and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment amounts, expiry times, deposit instructions, and status details.]

## Skill Version(s):

0.1.26 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
