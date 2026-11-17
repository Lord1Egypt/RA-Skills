## Description:

Queries database tables through an API, analyzes selected data, and generates a Word analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rm-ra](https://clawhub.ai/user/rm-ra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use sql-doc to look up mapped database tables, run authorized SQL queries through a database API, and produce Word reports summarizing incident-style records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query broad database tables and generate reports containing sensitive incident-style records.

Mitigation: Use only approved database endpoints and tables, restrict queries to authorized scope, and redact or aggregate sensitive fields before report generation.

Risk: The documented database API call uses plaintext HTTP to an internal endpoint.

Mitigation: Revise deployments to use authenticated HTTPS and least-privilege access controls before handling sensitive data.

Risk: Generated reports are written to a fixed workspace path and may expose unredacted content.

Mitigation: Require a user-approved protected output path and apply appropriate file permissions and retention controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated DOCX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database query results and unredacted report content; use only with authorized data and protected output locations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
