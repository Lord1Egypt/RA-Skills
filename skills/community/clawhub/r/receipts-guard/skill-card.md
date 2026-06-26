## Description: <br>
ERC-8004 identity, x402 payments, and arbitration protocol for autonomous agent commerce. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lazaruseth](https://clawhub.ai/user/lazaruseth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Receipts Guard to capture agreements, manage DID-based agent identity, handle x402 payment-backed arbitration, and run local or cloud HTTP workflows for agent commerce. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet private keys, API keys, local identity keys, and receipt storage. <br>
Mitigation: Use a dedicated low-balance wallet for RECEIPTS_WALLET_PRIVATE_KEY, protect and back up ~/.openclaw/receipts, and keep API keys and chain credentials in deployment secrets. <br>
Risk: The HTTP server exposes protected proposal, agreement, and acceptance workflows. <br>
Mitigation: Configure RECEIPTS_API_KEY, prefer DID request signing for counterparty-sensitive actions, set strict CORS origins, and avoid wildcard CORS in production. <br>
Risk: The included security audit covers v0.6.0 while this release is v0.7.1. <br>
Mitigation: Treat the v0.6.0 audit as historical assurance and review the v0.7.1 HTTP, payment, and cloud-deployment changes before production deployment. <br>


## Reference(s): <br>
- [Receipts Guard ClawHub listing](https://clawhub.ai/lazaruseth/receipts-guard) <br>
- [Security Audit Report](SECURITY_AUDIT.md) <br>
- [W3C DID Core context](https://www.w3.org/ns/did/v1) <br>
- [Moltbook Receipts Guard profile](https://moltbook.com/u/receipts-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; workflows may write identity, agreement, arbitration, and receipt files under the local Receipts data directory.] <br>

## Skill Version(s): <br>
0.7.1 (source: metadata.openclaw.version, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
