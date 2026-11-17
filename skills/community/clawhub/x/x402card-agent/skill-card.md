## Description:

This skill helps an agent discover, issue, top up, and manage wallet-owned x402card virtual cards through public Base-USDC x402 entrypoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elvismusli](https://clawhub.ai/user/elvismusli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide wallet-owned virtual card issuance, top-ups, balance/status checks, and secure credential reveal without exposing a private key to the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented curl-to-shell installer is powerful for a financial and wallet-connected workflow without pinning or integrity checks.

Mitigation: Review before installing and prefer an auditable pinned, checksum- or signature-verified release from a trusted publisher path.

Risk: Card issue and top-up actions move Base USDC, and ambiguous submission handling can create payment risk if the body or idempotency key changes.

Mitigation: Require explicit approval, validate the x402 challenge and economics before signing, reuse the same body and idempotency key for recovery, and treat unknown settlement state as pending.

Risk: Credential reveal can expose sensitive card details if shown to the model, logs, files, stdout, chat, or MCP surfaces.

Mitigation: Require fresh owner authentication and reveal credentials only to the controlling TTY or explicit clipboard while keeping them out of model context and persistent outputs.

## Reference(s):

- [x402card ClawHub skill page](https://clawhub.ai/elvismusli/skills/x402card-agent)
- [x402card card discovery API](https://api.x402card.org/api/card/discovery)
- [x402card agent API](https://api.x402card.org/api/agent)
- [x402card card purchase API](https://api.x402card.org/api/card/purchase)
- [x402card top-up discovery API](https://api.x402card.org/api/card/topup/discovery)
- [x402card top-up API](https://api.x402card.org/api/card/topup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment-validation, idempotency, owner-authentication, and credential-handling guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
