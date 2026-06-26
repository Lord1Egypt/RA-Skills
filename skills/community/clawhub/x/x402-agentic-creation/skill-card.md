## Description: <br>
Monetize your agent's API or tools using the x402 protocol and USDC micropayments. Enables provisioning, earnings tracking, and withdrawals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gatex402](https://clawhub.ai/user/gatex402) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent provision monetized API routes, check USDC earnings, and trigger withdrawals through GateX402 on supported Base and Solana networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes live USDC withdrawal authority. <br>
Mitigation: Use host-enforced approvals for withdrawals, wallet or session limits, destination and network verification, and audit logging for payout actions. <br>
Risk: Wallet private keys and management tokens are sensitive credentials. <br>
Mitigation: Store credentials outside agent-visible parameters and inject them only through the host runtime or secure vault interfaces. <br>
Risk: Provisioning and payout calls depend on the GateX402 backend. <br>
Mitigation: Restrict network access to approved GateX402 domains and log provisioning, balance, and withdrawal requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gatex402/x402-agentic-creation) <br>
- [GateX402 homepage](https://gatex402.dev) <br>
- [GateX402 LLM documentation](https://gatex402.dev/llms-full.txt) <br>
- [GateX402 OpenAPI specification](https://api.gatex402.dev/openapi.json) <br>
- [Safety guardrails](references/safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Boundary-wrapped text responses, JSON-like payloads, TypeScript tool calls, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tools require host-injected wallet credentials and management token access; withdrawal actions should use host-enforced approvals, session limits, destination and network verification, secure secret storage, and audit logging.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
