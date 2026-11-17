## Description:

Demonstrates the x402 payment protocol on TRON by fetching a protected image.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[hades-ye](https://clawhub.ai/user/hades-ye)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to exercise an x402 payment flow on TRON and retrieve a protected image resource.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically sign and pay for a protected resource, including on TRON mainnet, without clear user confirmation or payment limits.

Mitigation: Use test networks by default, require deliberate mainnet opt-in, and show the network, token, amount, recipient, fees, and signature scope before any payment or permit is signed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hades-ye/skills/x402-payment-demo)
- [TRON Nile protected demo endpoint](https://x402-tron-demo.aibank.io/protected-nile)
- [TRON Shasta protected demo endpoint](https://x402-tron-demo.aibank.io/protected-shasta)
- [TRON Mainnet protected demo endpoint](https://x402-tron-demo.aibank.io/protected-mainnet)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Files]

**Output Format:** [Markdown guidance with retrieved image display]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Temporary local image files should be deleted after display.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
