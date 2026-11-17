## Description:

Use when an agent needs a public bounded deterministic W04 trace-integrity verification from supplied redacted JSON evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slowsleeper1](https://clawhub.ai/user/slowsleeper1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to submit redacted expected-versus-observed W04 trace evidence to a public deterministic verifier and interpret the machine-readable integrity result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive data could be exposed if users submit real customer data, production traces, secrets, credentials, or tokens to the public verifier endpoint.

Mitigation: Submit only deliberately redacted, non-sensitive trace evidence and reject secret-bearing or oversized payloads before calling the endpoint.

Risk: The verifier compares only supplied expected and observed evidence, so missing supplied evidence is not proof of runtime failure.

Mitigation: Interpret incomplete results as trace-evidence findings and corroborate them with independent runtime or operational evidence before making production decisions.

## Reference(s):

- [Public W04 Trace Integrity Verifier API](https://soja-w04-public-evaluate.slowsleeper1.workers.dev/v1/trace-integrity-verifier/evaluate)
- [ClawHub skill page](https://clawhub.ai/slowsleeper1/skills/soja-trace-evidence-checks)

## Skill Output:

**Output Type(s):** [Guidance, API calls, JSON]

**Output Format:** [Markdown guidance with HTTP and JSON examples; machine-readable JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded redacted JSON payloads up to 64 KiB; no API key currently required.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
