## Description:

Use when configuring OpenClaw to run TWZRD preflight checks before payment-shaped x402 tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twzrd-sol](https://clawhub.ai/user/twzrd-sol)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and developers use this skill to configure a preflight gate before payment-shaped x402 or AgentCash-style tool calls. It provides installation and configuration guidance for enforcing fail-closed checks before payment requests can reach a signer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable npm package in the payment-call path.

Mitigation: Pin and audit a specific twzrd-preflight npm version, verify its publisher and lifecycle scripts, and review it before deployment.

Risk: The configured runtime contacts a remote preflight service with transaction or request data.

Mitigation: Confirm what data is sent to https://intel.twzrd.xyz and restrict the OpenClaw runtime's file and credential access.

Risk: Incorrect configuration could allow payment-shaped requests to proceed without the intended preflight gate.

Mitigation: Use enforce mode with fail-closed behavior and wash-flag refusal unless a reviewed operational need requires shadow mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twzrd-sol/skills/twzrd-preflight)
- [TWZRD Intel endpoint](https://intel.twzrd.xyz)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with bash, JSON, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw plugin configuration and HTTP-client wrapper guidance.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
