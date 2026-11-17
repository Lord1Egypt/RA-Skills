## Description:

A routing skill suite for Volcano Engine Serverless Flink that helps agents use the `volc_flink` CLI for tool setup, project and configuration management, Flink job development, operations, monitoring, diagnostics, and performance tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvheyang](https://clawhub.ai/user/lvheyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to route concrete Volcano Engine Flink requests to focused subskills for setup, authentication, resource inspection, SQL/JAR/CDC/batch job work, operations, savepoints, monitoring, diagnostics, and tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide state-changing cloud operations such as create, delete, publish, start, stop, restart, rescale, endpoint, resource-pool, and default-configuration changes.

Mitigation: Require explicit user confirmation with the target object, target ID, planned change, and expected operational impact before executing any state-changing workflow.

Risk: The skill is credential-adjacent because it works with local `volc_flink` profiles and optional Volcano Engine access-key environment variables.

Mitigation: Use interactive login or enterprise secret management, avoid command-line password or AK/SK examples, redact sensitive values, and do not print full credential-bearing files.

Risk: Connector and dependency setup can affect data exposure, transport security, or package supply-chain trust.

Mitigation: Prefer TLS-backed Kafka settings and secure secret entry, and pin or verify the `volc-flink-cli` package source where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvheyang/skills/volc-flink-skill)
- [Artifact README](artifact/README.md)
- [Common security conventions](artifact/COMMON_SECURITY.md)
- [Common mutation conventions](artifact/COMMON_MUTATION.md)
- [Flink CDC overview reference](artifact/skills/flink-cdc/references/overview.md)
- [Flink CDC command reference](artifact/skills/flink-cdc/references/volc_flink_commands.md)
- [Flink SQL connector reference](artifact/skills/flink-sql/references/connectors.md)
- [Flink SQL command reference](artifact/skills/flink-sql/references/volc_flink_commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, code blocks, configuration snippets, and occasional JSON or YAML examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk confirmations, redacted status summaries, and generated SQL or CDC configuration templates.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
