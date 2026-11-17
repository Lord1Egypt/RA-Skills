## Description:

Tork Guardian is an AI governance and safety layer for OpenClaw agents that redacts sensitive data, governs tool and network activity, and generates compliance audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torkjacobs](https://clawhub.ai/user/torkjacobs)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add policy checks, PII redaction, network governance, tool-call review, scanner reports, and compliance receipts to OpenClaw agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, content, and security telemetry may be sent to Tork.

Mitigation: Use only with approved data and credentials, and avoid sending sensitive or regulated content unless the deployment is authorized for that data.

Risk: Security evidence says the SDK protection controls can fail open or be bypassed.

Mitigation: Do not treat it as the sole enforcement boundary; add host, runtime, and policy controls and verify fail-closed behavior before production use.

Risk: Security guidance warns against scanning untrusted source maps through scanFromSource.

Mitigation: Scan only trusted source maps or run scans in an isolated disposable environment with path validation.

Risk: Security guidance requires dependency updates before production use.

Mitigation: Update and audit dependencies during release intake before deploying in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/torkjacobs/skills/tork-guardian)
- [Quick Start](docs/QUICK-START.md)
- [Network Security](docs/NETWORK-SECURITY.md)
- [Security Scanner](docs/SCANNER.md)
- [Tork website](https://tork.network)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with TypeScript examples, shell commands, JSON scanner reports, and structured governance decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit redacted text, allow/deny decisions, compliance receipt metadata, network activity logs, risk scores, verdicts, and badge markdown.]

## Skill Version(s):

1.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
