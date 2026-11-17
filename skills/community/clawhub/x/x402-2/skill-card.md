## Description:

Search for paid API services, inspect x402 payment requirements, and make paid USDC API requests using the x402 payment protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrag](https://clawhub.ai/user/0xrag)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover paid API services in the x402 bazaar, inspect endpoint price and schemas, and make authenticated USDC-backed API requests when explicitly needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated paid requests can spend real USDC on endpoints the user did not intend to buy.

Mitigation: Use the skill only for explicit x402 tasks, inspect prices and endpoint details first, set --max-amount for every paid request, and avoid funded wallets beyond the amount prepared to spend.

Risk: Mutable third-party command execution can change behavior between runs.

Mitigation: Prefer a pinned and reviewed awal version before running payment-related commands.

Risk: Arbitrary or untrusted URLs can expose the agent to incompatible endpoints or misleading payment requirements.

Mitigation: Avoid arbitrary URLs, use known or bazaar-discovered endpoints, and inspect schemas and requirements before calling paid endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xrag/skills/x402-2)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid requests should inspect requirements first and set a maximum payment amount.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
