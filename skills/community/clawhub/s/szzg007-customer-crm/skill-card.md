## Description: <br>
Unified customer CRM management for cross-border ecommerce workflows, including customer profiles, status tracking, cloud/local sync, segmentation, reporting, and data maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szzg007](https://clawhub.ai/user/szzg007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users and ecommerce operators use this skill to maintain customer records, classify customer priority, track funnel status, synchronize CRM data, and generate customer reports. It is aimed at cross-border ecommerce customer management workflows rather than general-purpose CRM administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive customer records and contact details across local and cloud storage. <br>
Mitigation: Use explicit user approval, narrow service-account permissions, protected credential storage, and access controls before reading, syncing, or modifying CRM data. <br>
Risk: Automated sync, cleanup, conflict resolution, and message-derived status updates can alter or remove commercially important CRM data. <br>
Mitigation: Use backups, dry-run previews, audit logs, and confirmation steps for cleanup, conflict resolution, and customer-field updates. <br>
Risk: Cloud sync to Feishu Bitable or Google Sheets can expose personal, regulated, or commercially sensitive data if configured too broadly. <br>
Mitigation: Limit which sources, tables, fields, and customer records the agent may access or change, and review configurations before enabling scheduled sync. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szzg007/szzg007-customer-crm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, examples, configuration snippets, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include customer profile cards, CRM status updates, sync instructions, cleanup guidance, and report templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
