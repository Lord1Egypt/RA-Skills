## Description:

Get a disposable temp phone number and receive OTP codes to sign up on websites without using your real number. Handles x402 crypto payment automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xshadoweth](https://clawhub.ai/user/0xshadoweth)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to obtain single-use temporary phone numbers, trigger SMS verification on supported websites, and retrieve OTP codes without using a personal phone number.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent authority to make paid x402 crypto purchases for temporary phone numbers.

Mitigation: Use a dedicated, minimally funded wallet and require explicit approval before each paid number purchase.

Risk: Disposable phone verification can violate third-party service terms or support deceptive account creation.

Mitigation: Use only where disposable verification is permitted, and do not use it for financial or identity-linked access.

Risk: OTP handling may complete account access or registration on a third-party site.

Mitigation: Require explicit approval before entering any OTP into a third-party website.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xshadoweth/skills/shadow-phone)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTTP request examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SHADOW_WALLET_KEY and may spend approximately $0.10 USDC on Base per number purchase.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
