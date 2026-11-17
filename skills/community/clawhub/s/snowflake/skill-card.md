## Description:

Executes governed, read-only Snowflake SELECT queries with forbidden keyword blocking, row limits, statement timeouts, and structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiagohubnerdataplatform](https://clawhub.ai/user/tiagohubnerdataplatform)

### License/Terms of Use:


## Use Case:

Data engineers and analytics agents use this skill to run bounded Snowflake read queries and receive query metadata plus tabular results as JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact Snowflake database access can expose sensitive data if deployed without strong authorization boundaries.

Mitigation: Deploy behind authentication with a dedicated least-privilege Snowflake role, audited access, and private network binding.

Risk: Query filtering and row limits are incomplete safeguards for arbitrary SQL submitted by callers.

Mitigation: Use robust SQL parsing or approved query templates with non-bypassable row and response-size limits before production use.

Risk: Raw error details can disclose database or environment information.

Mitigation: Sanitize endpoint errors and expose only operationally necessary diagnostics to callers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tiagohubnerdataplatform/skills/snowflake)

## Skill Output:

**Output Type(s):** [API calls, JSON, data]

**Output Format:** [Structured JSON containing query_id, row_count, and result rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Executes SELECT-only Snowflake queries through an HTTP POST endpoint and appends a default row limit when no LIMIT is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
