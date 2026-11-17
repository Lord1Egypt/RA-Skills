## Description:

Enterprise semantic search skill for table, field, and file search plus Text-to-SQL data generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sevenal](https://clawhub.ai/user/sevenal)

### License/Terms of Use:

MIT

## Use Case:

Developers and data teams use this skill to retrieve relevant database tables, fields, files, and generated SQL-backed data answers from natural-language queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-generated SQL may execute against connected databases and return unintended or excessive data.

Mitigation: Use read-only least-privilege database credentials, parser-based SQL validation, row limits, audit logs, and access controls before enabling Text-to-SQL on production data.

Risk: Published configuration includes internal-looking endpoints and credential-like values that require review.

Mitigation: Review PROJECT_CONFIG.md before installation, remove environment-specific values from deployments, and rotate any credentials that match published examples.

Risk: Schema details, sample rows, and user questions may be sent to model or embedding endpoints.

Mitigation: Approve model endpoints for the data involved and avoid sending sensitive schema or sample rows to external providers unless policy allows it.

Risk: Unpinned dependencies can change behavior or introduce vulnerable transitive packages.

Mitigation: Pin dependencies and scan the locked runtime environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sevenal/skills/semantic-search)
- [README](artifact/README.md)
- [Configuration guide](artifact/CONFIG_GUIDE.md)
- [Usage examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [JSON response objects with Markdown guidance, Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include retrieved resources, field names, generated SQL, query results, status codes, and error messages.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
