## Description:

Complete Salesforce CRM integration for real-time data access, lead management, opportunity tracking, duplicate detection, and bulk operations with one-click OAuth connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sawera557](https://clawhub.ai/user/sawera557)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and RevOps users, Salesforce administrators, and developers use this skill to connect agents to Salesforce, query CRM records, manage leads and opportunities, detect duplicates, and perform controlled bulk changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large or persistent Salesforce changes can affect production CRM data.

Mitigation: Test in a Salesforce sandbox, preview affected records, confirm record counts, prepare a rollback plan, and require administrator approval before production use.

Risk: Overprivileged or long-lived Salesforce credentials can increase impact if exposed or misused.

Mitigation: Use a dedicated least-privilege Salesforce integration user and avoid storing passwords, admin tokens, or long-lived secrets in .env.

Risk: A misconfigured Salesforce instance host can send operations to the wrong org.

Mitigation: Validate SALESFORCE_INSTANCE_URL before connecting and explicitly distinguish sandbox from production environments.

Risk: Bulk updates, deletes, GTM standardization, and automation deployment can change many records or future workflows.

Mitigation: Require explicit confirmation, use dry runs or previews where available, keep backups for destructive operations, and activate deployed automation manually only after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sawera557/skills/salesforce-easy)
- [Salesforce guide](salesforce-guide.html)
- [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with tables, JSON from helper scripts, and inline shell or Python commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured Salesforce credentials; write operations should be previewed and confirmed before execution.]

## Skill Version(s):

1.0.17 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
