## Description:

Builds n8n automation workflows that connect business apps, automate repetitive tasks, and create custom business logic flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, consultants, and business automation developers use this skill to design n8n workflows for CRM sync, email sequences, notifications, form routing, ecommerce automation, data pipelines, and AI-assisted workflow orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows may act on production CRM, email, social, payment, or ecommerce systems with broad permissions.

Mitigation: Review credentials, scopes, permissions, rollback steps, and sanitized test results before connecting workflows to production systems.

Risk: The release declares an unexplained unpinned Node package install.

Mitigation: Review the package purpose and pin an approved version before installation.

Risk: Broad activation phrases may trigger business automation guidance unexpectedly.

Mitigation: Invoke the skill deliberately and review proposed workflows before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/sales-automation-workflows)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with workflow JSON, setup steps, and optional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include n8n workflow JSON, setup guidance, and maintenance notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
