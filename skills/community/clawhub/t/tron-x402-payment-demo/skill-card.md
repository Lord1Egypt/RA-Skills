## Description:

Demo of x402 payment protocol by fetching a protected image.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[wzc1206](https://clawhub.ai/user/wzc1206)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to demonstrate an x402 payment flow on the TRON network by requesting a protected image, handling payment, and presenting the retrieved image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically sign TRON payment operations using a private key.

Mitigation: Use only a dedicated low-balance demo wallet and require manual review before any signature or payment is submitted.

Risk: The protected resource is requested over plaintext HTTP.

Mitigation: Verify the endpoint, network, recipient, asset, amount, fees, and permit scope before executing the payment flow.

Risk: The payment flow does not clearly state per-transaction approval or spending limits.

Mitigation: Run the skill only in a controlled demo context with explicit payment limits and human confirmation for each transaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzc1206/skills/tron-x402-payment-demo)
- [Protected x402 TRON demo endpoint](http://x402-tron-demo.sunagent.ai/protected)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with trigger phrases and operational steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require TRON_PRIVATE_KEY and produces a displayed image after payment flow completion.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
