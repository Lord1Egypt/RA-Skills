## Description:

ERC-8004 identity, x402 payments, and arbitration protocol for autonomous agent commerce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lazaruseth](https://clawhub.ai/user/lazaruseth)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent operators use Receipts Guard to manage agent identity, payment-backed arbitration proposals, evidence, rulings, timelines, and deployment guidance for autonomous agent commerce.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles identities, agreement records, and blockchain actions with unsafe security gaps identified by the authoritative ClawHub security scan.

Mitigation: Install only after source review and use the workflow only when identity, arbitration, and payment functions are required.

Risk: A publicly exposed HTTP server can create risk around protected agreement and proposal endpoints.

Mitigation: Use strict API keys or DID request signing, keep CORS origins restricted, and preserve rate limiting before exposing the server.

Risk: On-chain wallet use can cause irreversible transactions or loss if a funded mainnet key is misconfigured or compromised.

Mitigation: Prefer testnets and avoid funded mainnet wallet keys unless irreversible transaction risk is acceptable.

Risk: Legacy signatures and controller recovery may not provide sufficient assurance until verification issues are fixed.

Mitigation: Avoid relying on legacy signatures or controller recovery for high-value agreements.

## Reference(s):

- [ClawHub Receipts Guard release page](https://clawhub.ai/lazaruseth/skills/receipts-guard)
- [ClawHub publisher profile](https://clawhub.ai/user/lazaruseth)
- [Security audit artifact](artifact/SECURITY_AUDIT.md)
- [W3C DID Core context](https://www.w3.org/ns/did/v1)
- [Moltbook Receipts Guard profile](https://moltbook.com/u/receipts-guard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; blockchain actions may require RPC endpoints and wallet private key configuration.]

## Skill Version(s):

0.7.1 (source: server release metadata, package.json, and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
