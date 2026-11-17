## Description:

Provides Zcash-backed attestation tools and hooks for OpenClaw agents to record messages, commands, session changes, and proof checkpoints with a remote ZAP1 service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skndrs](https://clawhub.ai/user/skndrs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add proof-oriented Zcash attestation, verification, and lifecycle lookup workflows to OpenClaw agents. It is intended for agents where message, command, session, and policy-related activity should be recorded or checked through a ZAP1 service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill submits agent messages, command activity, session changes, and related hashes to a ZAP1 service and may create durable proof records.

Mitigation: Install only when this telemetry is intended, configure a trusted HTTPS apiUrl, and avoid sending sensitive activity unless durable remote attestation is acceptable.

Risk: The security review says advertised policyRules should not be treated as automatic access control unless enforcement is separately wired and tested.

Mitigation: Validate policy enforcement in the host agent's tool dispatch path before relying on blockedTools or restrictedTools for safety controls.

Risk: The security review flags admin key creation and remote event creation as sensitive operations.

Mitigation: Use tightly scoped API keys, avoid admin keys unless required, rotate keys according to local policy, and review created events before using them as authoritative records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skndrs/skills/zap1-zcash-attestation)
- [Publisher profile](https://clawhub.ai/user/skndrs)
- [ZAP1 protocol repository](https://github.com/Frontier-Compute/zap1)
- [ZAP1 on-chain protocol specification](https://github.com/Frontier-Compute/zap1/blob/main/ONCHAIN_PROTOCOL.md)
- [Zcash ZIP draft PR 1243](https://github.com/zcash/zips/pull/1243)
- [ZAP1 verifier](https://pay.frontiercompute.io/verify.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proof hashes, proof bundles, anchor status, lifecycle records, event summaries, decoded memo data, and checkpoint text injected into an agent session.]

## Skill Version(s):

0.2.1 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
