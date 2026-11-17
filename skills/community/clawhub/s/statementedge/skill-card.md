## Description:

Convert PDF bank statements to CSV, Excel, QuickBooks, Xero, Sage, or OFX through StatementEdge with auto-reconciliation, EU hosting, support for 100+ banks across 22 countries, and no model training on uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saipradeep77](https://clawhub.ai/user/saipradeep77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance automation users use this skill to convert uploaded PDF bank statements into reconciled structured data and accounting export formats through the StatementEdge API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads bank statements and any supplied PDF passwords to StatementEdge and its disclosed subprocessors.

Mitigation: Use a dedicated API key, upload only files intended for conversion, and review StatementEdge retention and privacy terms before using it with financial or regulated data.

Risk: A StatementEdge API key is required to convert files and fetch job history for the user's account.

Mitigation: Store the key as an environment variable or managed secret, avoid committing it to files, and revoke or rotate it from the StatementEdge dashboard if exposed.

## Reference(s):

- [StatementEdge ClawHub Skill](https://clawhub.ai/saipradeep77/skills/statementedge)
- [StatementEdge Homepage](https://www.statementedge.com)
- [StatementEdge API Documentation](https://www.statementedge.com/docs/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with curl commands, JSON API responses, and exported statement files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STATEMENTEDGE_API_KEY and sends user-selected bank statement PDFs to StatementEdge for conversion.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
