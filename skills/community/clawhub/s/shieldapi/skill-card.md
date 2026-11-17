## Description:

ShieldAPI provides x402 security intelligence endpoints for AI agents, including password range checks, email breach lookup, domain and IP reputation, URL safety, full security scans, prompt injection checks, MCP trust checks, and package checks with pay-per-request USDC micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alberthild](https://clawhub.ai/user/alberthild)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add external security checks for passwords, domains, IPs, URLs, prompts, MCP servers, software packages, and agent skills. It is suited for agents that can call ShieldAPI endpoints with curl and, for paid requests, complete x402 payment flow outside the agent prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security-check inputs are sent to an external ShieldAPI service and may include domains, URLs, IP addresses, email addresses, prompts, or package names.

Mitigation: Use demo mode first and avoid internal-only URLs, customer emails, regulated data, confidential prompts, or other sensitive indicators unless ShieldAPI's privacy policy and your compliance requirements allow it.

Risk: Paid endpoint use requires USDC micropayments through the x402 flow.

Mitigation: Install only if pay-per-request behavior is acceptable, and delegate payment signing to a secure wallet or signer rather than exposing raw private keys or mnemonic phrases to the agent.

Risk: The deprecated full password hash endpoint can reveal sensitive password-derived data to the service.

Mitigation: Use the k-anonymity password range endpoint and do not send raw passwords or full password hashes.

## Reference(s):

- [ShieldAPI Skill Page](https://clawhub.ai/alberthild/skills/shieldapi)
- [ShieldAPI Live API Health](https://shield.vainplex.dev/api/health)
- [ShieldAPI Base API](https://shield.vainplex.dev/api)
- [ShieldAPI Privacy Policy](https://shield.vainplex.dev/privacy.html)
- [x402 Protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline shell commands and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; paid requests require out-of-band x402 payment signing and may return JSON API responses.]

## Skill Version(s):

3.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
