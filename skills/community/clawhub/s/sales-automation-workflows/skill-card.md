## Description: <br>
Builds n8n automation workflows that connect business apps, automate repetitive tasks, and create custom business logic flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business teams, operators, and automation consultants use this skill to design n8n workflows for CRM sync, email automation, notifications, e-commerce operations, data pipelines, and AI-assisted routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflows may perform business actions through connected accounts before they have been reviewed. <br>
Mitigation: Review generated n8n workflows before enabling real accounts, and require manual approval for customer emails, invoices, payment-related actions, social posts, and bulk data sync. <br>
Risk: Workflow setup can expose customer data or account credentials if tested directly against production systems. <br>
Mitigation: Test with sandbox or sanitized data first, store secrets in n8n credential storage, and use least-privilege API keys. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with workflow JSON, setup instructions, and inline code or configuration examples when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic questions, n8n workflow designs, workflow JSON backups, setup guidance, and maintenance notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
