## Description:

Generates Salesforce report blueprints from live org metadata by guiding users through Salesforce CLI metadata discovery, object mapping, and report design constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breynol01](https://clawhub.ai/user/breynol01)

### License/Terms of Use:

MIT-0

## Use Case:

Salesforce administrators, analysts, and developers use this skill to turn reporting questions into Salesforce Report Builder blueprints grounded in real org metadata. It helps identify relevant objects, fields, relationships, filters, groupings, and gaps before a report is built.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Salesforce metadata, query results, and local exports may contain sensitive business or personal data.

Mitigation: Use a sandbox or least-privilege Salesforce user for exploration, avoid unnecessary local exports, and handle any saved schema or query output according to the organization's data policy.

Risk: Generated SOQL or report assumptions may not match the target org's schema, permissions, or report type availability.

Mitigation: Review commands and SOQL before execution, run live metadata describes before making field claims, and validate reportable fields and permissions before building the report.

## Reference(s):

- [SFDC CLI Reference](artifact/references/cli-reference.md)
- [Object Mapping Guide](artifact/references/object-mapping.md)
- [ClawHub Skill Page](https://clawhub.ai/breynol01/skills/salesforce-reporting-copilot)
- [Project Homepage](https://github.com/breynol01/salesforce-reporting-copilot)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report blueprint with tables, lists, and optional inline Salesforce CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relies on live Salesforce metadata; users should review generated SOQL and avoid storing sensitive schema or query outputs unnecessarily.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
