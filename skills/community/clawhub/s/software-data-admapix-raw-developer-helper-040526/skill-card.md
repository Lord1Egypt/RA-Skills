## Description:

Design and harden AdMapix-style raw data workflows for creative, app, ranking, revenue, and analytics datasets before they become dashboards or agent tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, growth analysts, skill authors, and agent builders use this skill to plan AdMapix-style raw data ingestion, normalization, validation, and publication workflows while preserving provenance and auditability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation may route generic analytics, revenue, or ETL prompts to this skill outside the intended AdMapix-style raw data context.

Mitigation: Review implicit invocation settings and scope use to AdMapix, app-market, creative, ranking, revenue, or raw-data workflow requests.

Risk: Workflow guidance applied without source-specific validation could produce misleading cleaned datasets or dashboards.

Mitigation: Keep immutable raw captures separate, require validation for schema drift, duplicates, missing values, metric consistency, and record source, timestamp, row count, and anomalies for each transform.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-admapix-raw-developer-helper-040526)
- [AdMapix Demand Signal](https://clawhub.ai/skills/admapix)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with checklists, validation rules, data model notes, and optional code or command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw-to-clean data models, schema checks, local ingestion plans, audit trail requirements, and reliability checklists.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
