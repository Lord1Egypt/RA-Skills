## Description:

Record, inspect, mock, replay, and generate API traffic using the proxymock CLI for HTTP, gRPC, database, load, regression, and CI testing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mleray24](https://clawhub.ai/user/mleray24)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to guide agents through proxymock traffic capture, RRPair inspection and editing, mock generation, replay and load testing, and CI validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recorded RRPair files, logs, and snapshots can contain sensitive API or database traffic.

Mitigation: Use authorized traffic only, prefer non-production or sanitized data, and treat recordings as sensitive before sharing or uploading them.

Risk: Cloud push commands can upload captured snapshots outside the local environment.

Mitigation: Confirm the destination, authorization, and data handling approval before using cloud push.

Risk: TLS bypass examples can weaken security if copied into real workflows.

Mitigation: Use TLS bypass only for isolated local testing and restore normal certificate validation for production-like traffic.

## Reference(s):

- [proxymock CLI Reference](references/cli-reference.md)
- [Language-Specific Proxy Configuration](references/language-reference.md)
- [Speedscale proxymock Language Reference](https://docs.speedscale.com/proxymock/getting-started/language-reference/)
- [ClawHub skill page](https://clawhub.ai/mleray24/skills/proxymock)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the proxymock binary; may guide agents to create or inspect RRPair markdown or JSON files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
