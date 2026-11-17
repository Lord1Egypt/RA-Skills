## Description:

Implement UCP AP2 Mandates extension for cryptographic payment mandates in autonomous agent commerce using SD-JWT credentials, merchant authorization signatures, and the Agent Payments Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ichiorca](https://clawhub.ai/user/ichiorca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and payment engineers use this skill to design UCP AP2 mandate flows for autonomous checkout, including mandate artifacts, merchant authorization, verification, downgrade protection, and AP2-specific error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous payment mandate implementations can authorize financial transactions without real-time human approval.

Mitigation: Require explicit user opt-in, narrow spending and validity limits, audit logs, revocation handling, and human review for high-risk transactions.

Risk: Incorrect mandate or merchant authorization handling can weaken payment authorization and verification.

Mitigation: Fetch the current UCP and AP2 specifications before implementation and validate against the referenced conformance tests.

## Reference(s):

- [UCP and AP2 documentation](https://ucp.dev/2026-01-23/documentation/ucp-and-ap2/)
- [Agent Payments Protocol](https://ap2-protocol.org)
- [Universal Commerce Protocol conformance tests](https://github.com/Universal-Commerce-Protocol/conformance)
- [ClawHub skill page](https://clawhub.ai/ichiorca/skills/ucp-ap2-mandates)

## Skill Output:

**Output Type(s):** [guidance, code, configuration, shell commands]

**Output Format:** [Markdown guidance with implementation notes, command suggestions, and code-oriented requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code or hidden execution behavior is reported in the security evidence.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
