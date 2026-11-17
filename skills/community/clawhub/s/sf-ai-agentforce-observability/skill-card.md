## Description:

Extract and analyze Agentforce session tracing data from Salesforce Data Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsouza-anush](https://clawhub.ai/user/dsouza-anush)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations engineers use this skill to extract Session Tracing Data Model telemetry, analyze Agentforce sessions, reconstruct timelines, and debug routing, action, latency, and quality issues from Data 360 data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Agentforce conversation telemetry, action payloads, generation data, and exported Parquet files.

Mitigation: Install only for authorized users, use approved secure storage for extracts, and handle message and generation content as sensitive data.

Risk: Broad Data Cloud access and wide date ranges can expose more telemetry than needed and increase query cost.

Mitigation: Use a dedicated least-privilege Salesforce External Client App and prefer focused date, agent, and session filters.

Risk: Server security guidance flags token forwarding and SQL interpolation issues.

Mitigation: Fix those code paths before shared, automated, or production-support use, and review generated SQL before execution.

## Reference(s):

- [README](README.md)
- [Authentication Setup](references/auth-setup.md)
- [Data Model Reference](references/data-model-reference.md)
- [Data Cloud Query Patterns](references/query-patterns.md)
- [Analysis Cookbook](references/analysis-cookbook.md)
- [Debugging Sessions](references/debugging-sessions.md)
- [CLI Reference](references/cli-reference.md)
- [Billing Considerations & Troubleshooting](references/billing-and-troubleshooting.md)
- [Salesforce Data Cloud Query API](https://developer.salesforce.com/docs/atlas.en-us.c360a_api.meta/c360a_api/c360a_api_query.htm)
- [Agentforce Session Tracing](https://help.salesforce.com/s/articleView?id=sf.copilot_session_tracing.htm)
- [Salesforce JWT Bearer Flow](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with shell commands, Python snippets, SQL examples, file paths, and analysis summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference Parquet telemetry extracts and metadata files; treat exported telemetry as sensitive.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
