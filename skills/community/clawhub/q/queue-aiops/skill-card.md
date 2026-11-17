## Description:

Provides Redis and RabbitMQ monitoring, troubleshooting, root-cause analysis, and governed configuration and queue operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use the skill to inspect Redis and RabbitMQ health, investigate broker issues, and manage supported configuration or queue changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive broker operations can purge messages or delete queues, and the skill does not itself decide whether a write is permitted.

Mitigation: Start with broker-enforced monitoring-only permissions; require explicit approval outside the model before destructive MCP calls, and review dry-run previews before CLI writes.

Risk: Broker credentials and transport settings can expose access if configured carelessly.

Mitigation: Keep TLS verification enabled and provide the master password through protected runtime secret injection.

Risk: The release security review flags destructive-action safeguards and credential setup for review.

Mitigation: Review and pin the package version before installation, and follow the security guidance for permissions and secret handling.

## Reference(s):

- [Capabilities reference](artifact/references/capabilities.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Setup guide](artifact/references/setup-guide.md)
- [CLI reference](artifact/references/cli-reference.md)
- [ClawHub release page](https://clawhub.ai/zw008/skills/queue-aiops)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON tool results with concise operational analysis and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include measured broker evidence, findings, and operation previews.]

## Skill Version(s):

0.12.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
