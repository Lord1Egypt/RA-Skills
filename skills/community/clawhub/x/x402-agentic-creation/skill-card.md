## Description:

Monetize your agent's API or tools using the x402 protocol and USDC micropayments. Enables provisioning, earnings tracking, and withdrawals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gatex402](https://clawhub.ai/user/gatex402)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to provision paid API gateways, set USDC route pricing, check balances, and withdraw earnings through GateX402.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign wallet messages and trigger USDC withdrawals through the GateX402 backend.

Mitigation: Use a limited wallet or session policy, keep wallet keys in a vault, and require explicit human approval before withdrawals.

Risk: The skill depends on a trusted GateX402 backend for provisioning, balance checks, and withdrawals.

Mitigation: Install only if the GateX402 backend is trusted in the deployment environment and restrict outbound host access to approved domains.

Risk: Wallet private keys and management tokens could be exposed if passed through agent-visible parameters.

Mitigation: Inject credentials only through host-managed callbacks and store management tokens outside the agent transcript.

Risk: Flagged dependencies may be unsuitable for CI or production use without review.

Mitigation: Pin the installer path and update flagged dependencies before CI or production deployment.

## Reference(s):

- [GateX402 Homepage](https://gatex402.dev)
- [GateX402 LLM Documentation](https://gatex402.dev/llms-full.txt)
- [GateX402 OpenAPI Spec](https://api.gatex402.dev/openapi.json)
- [GateX402 Bazaar Discovery](https://gatex402.dev/discover)
- [Safety Guardrails](references/safety.md)
- [ClawHub Skill Page](https://clawhub.ai/gatex402/skills/x402-agentic-creation)

## Skill Output:

**Output Type(s):** [text, json, configuration]

**Output Format:** [Boundary-wrapped JSON strings returned by agent tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are sanitized to expose only selected provisioning, balance, withdrawal status, and transaction fields.]

## Skill Version(s):

1.0.1 (source: server release evidence; package.json and skill.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
