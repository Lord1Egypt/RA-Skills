## Description:

Audits SQL syntax and safety, executes candidate SQL against a StarRocks or Doris-compatible database, and returns query results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovenervermore](https://clawhub.ai/user/lovenervermore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill as the final audit and execution step in a SQL generation workflow. It checks candidate SQL, runs accepted queries, returns rows and row counts, and can provide retry candidates when no rows are returned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute raw database queries.

Mitigation: Run it only with a dedicated read-only database account, restrict accessible schemas and tables, and validate that SELECT-only and WHERE/table/schema limits are enforced before production use.

Risk: Query context can be sent to an external LLM fallback endpoint.

Mitigation: Use the fallback only with an explicit HTTPS allowlist and opt-in configuration, and avoid sending production or sensitive data until that path is reviewed.

Risk: Environment loading and default token behavior may expose or reuse unintended credentials.

Mitigation: Remove hardcoded token defaults, limit .env discovery scope, and provide credentials through managed secret storage.

## Reference(s):

- [Sql Audit ClawHub Skill Page](https://clawhub.ai/lovenervermore/skills/sql-audit)
- [lovenervermore ClawHub Publisher Profile](https://clawhub.ai/user/lovenervermore)

## Skill Output:

**Output Type(s):** [JSON, Data, Guidance]

**Output Format:** [JSON object with execution status, SQL, result rows, row count, error message, retry flag, retry count, and optional simplified metric candidates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 50 result rows and may suggest retry candidates when a query returns no rows.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
