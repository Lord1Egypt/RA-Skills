## Description:

Buy a novelty digital rock from treat.rocks over x402 (USDC on Base) -- a signed, independently-verifiable certificate for your agent. Fixed price, no token, not an investment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smelly-lemon](https://clawhub.ai/user/smelly-lemon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents with an x402-capable wallet use this skill to buy and verify a fixed-price novelty digital rock from treat.rocks. The skill guides payment discovery, user-controlled signing, and post-purchase certificate verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead to an irreversible on-chain USDC payment.

Mitigation: Review the live x402 payment prompt before signing, confirm the price, network, recipient, and endpoint, and proceed only if the purchase is intentional.

Risk: Base network gas is separate from the listed novelty item price.

Mitigation: Check the wallet or client gas estimate before approving the transaction.

Risk: The treat.rocks service is closed-source, so the server implementation cannot be independently inspected from this artifact.

Mitigation: Use the returned rock id to run the published verification flow and confirm the certificate before reporting the purchase complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smelly-lemon/skills/treat-rocks)
- [Publisher Profile](https://clawhub.ai/user/smelly-lemon)
- [treat.rocks Homepage](https://treat.rocks)
- [x402 Protocol](https://www.x402.org/)
- [treat.rocks Store Manifest](https://treat.rocks/store.json)
- [x402 Discovery Manifest](https://treat.rocks/.well-known/x402.json)
- [Certificate Public Key](https://treat.rocks/.well-known/treatrocks-pubkey.json)
- [Live Agent Instructions](https://treat.rocks/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with HTTP endpoint examples and payment verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live x402 payment requirements and directs the agent to verify the resulting certificate before reporting completion.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
