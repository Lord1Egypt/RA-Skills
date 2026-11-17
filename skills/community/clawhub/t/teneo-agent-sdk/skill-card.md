## Description:

Teneo Protocol CLI helps agents discover, inspect, and query Teneo network agents, manage rooms, and handle x402 USDC payments with wallet support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to discover Teneo network agents, inspect command interfaces and pricing, run agent queries for real-time data, and manage rooms and payment-capable wallets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-capable wallet operations can spend USDC through automatic agent command flows.

Mitigation: Use a dedicated low-balance wallet and prefer quote-and-confirm flows before paid execution.

Risk: Private keys or wallet credentials may be exposed through environment files, command output, or logs.

Mitigation: Avoid putting real private keys in `.env` or `TENEO_PRIVATE_KEY`, and do not run the skill where remote responses or command output may be logged with secrets.

Risk: Remote agent responses and payment flows have more authority than a normal install should grant by default.

Mitigation: Install only after reviewing the suspicious security verdict and confirming that payment-capable remote agent execution is acceptable for the environment.

## Reference(s):

- [Teneo Protocol](https://teneo-protocol.ai)
- [Teneo SDK on npm](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [x402 Protocol](https://x402.org)
- [Teneo Agent SDK/CLI on ClawHub](https://clawhub.ai/teneoprotocoldev/skills/teneo-agent-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, TypeScript code, configuration notes, and JSON command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can produce JSON responses from remote agents and may initiate x402 USDC payment flows.]

## Skill Version(s):

1.0.21 (source: ClawHub release evidence, released 2026-03-25; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
