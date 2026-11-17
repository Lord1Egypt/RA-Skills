## Description:

Query and manage VictoriaMetrics time-series database instances, including single-node and cluster deployments with multi-tenancy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangjinzhao](https://clawhub.ai/user/yangjinzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query monitoring data, inspect VictoriaMetrics service health, and generate PromQL commands for single-node or clustered VictoriaMetrics deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring credentials may be exposed through configuration files, terminal prompts, or logs.

Mitigation: Use HTTPS endpoints, avoid Basic Auth over HTTP, restrict permissions on the VictoriaMetrics config file, and avoid running the init wizard where passwords can be captured.

## Reference(s):

- [VictoriaMetrics API Reference](references/api_reference.md)
- [Common Monitoring Queries](references/common_queries.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce VictoriaMetrics API query results as JSON when its CLI is run against user-configured instances.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
