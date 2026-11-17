## Description:

x402 payment client for AI agents - how to automatically respond to HTTP 402 challenges, pay via CDP/Permit2, retry with PAYMENT-SIGNATURE, and settle the full x402 flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marketingkioldenburg](https://clawhub.ai/user/marketingkioldenburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to help agents consume x402-enabled pay-per-request APIs by handling HTTP 402 payment challenges, making Base USDC payments, and retrying requests with a payment signature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents to make cryptocurrency payments automatically from remote x402 payment challenges.

Mitigation: Use an isolated low-balance wallet, strict per-request and daily spend limits, approved recipient addresses, Base USDC validation, and manual approval for any new provider, changed recipient, or unexpected amount.

Risk: Blind retries can cause duplicate payments or settlement confusion.

Mitigation: Inspect payment state before retrying, reuse operation identifiers where available, and re-fetch results after settlement instead of submitting a fresh payment.

## Reference(s):

- [x402 Homepage](https://www.x402.org)
- [Hermes Commerce x402 Manifest](https://agent.kihustle.tech/.well-known/x402)
- [VerdictSwarm x402 Manifest](https://api.vswarm.io/.well-known/x402)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and an agent-controlled wallet for payment execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
