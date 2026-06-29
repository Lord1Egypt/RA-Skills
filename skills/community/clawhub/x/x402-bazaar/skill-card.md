## Description: <br>
x402 Bazaar protocol guide for AgentPMT that helps agents implement the HTTP 402 two-step handshake, sign EIP-3009 TransferWithAuthorization, route through the AgentPMT facilitator, and settle USDC payments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent builders use this skill to implement and debug AgentPMT x402 payment flows for wallet-funded credit purchases and agent-to-agent marketplace transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet signatures and USDC credit purchases are real financial actions. <br>
Mitigation: Before signing or retrying payment, verify the endpoint, amount, chain, token, payee, nonce, and validity window against the server challenge. <br>
Risk: Reusing or changing signed payment or session data can cause replay, mismatch, or failed authorization. <br>
Mitigation: Use fresh request IDs and nonces, sign the exact path and payload hash, and rebuild signatures from the expected message when authorization errors occur. <br>
Risk: Endpoints, schemas, setup steps, and examples may become stale. <br>
Mitigation: Refresh the skill when its documented last-updated date is more than seven days old, and verify live AgentPMT requirements before production use. <br>


## Reference(s): <br>
- [AgentPMT External Agent API](https://www.agentpmt.com/external-agent-api) <br>
- [AgentPMT Marketplace](https://www.agentpmt.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API calls] <br>
**Output Format:** [Markdown with inline code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet-signature, x402 payment flow, and error-handling guidance; agents must verify live endpoint requirements before payment.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
