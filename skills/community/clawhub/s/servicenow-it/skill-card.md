## Description:

ServiceNow IT Service Management integration with API key authentication. Manage incidents, problems, change requests, tasks, CMDB records, service catalog items, and IT operations via the ServiceNow REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

IT operations teams and service desk agents use this skill to inspect and manage ServiceNow ITSM, CMDB, service catalog, task, attachment, and change workflows through ClawLink-backed ServiceNow tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables a broad external plugin in OpenClaw.

Mitigation: Install only after reviewing and trusting the ClawLink plugin source and connection flow.

Risk: The artifact includes unrelated SendGrid Quick Start write examples.

Mitigation: Do not run SendGrid examples for a ServiceNow workflow; verify every tool name against the live ServiceNow catalog before execution.

Risk: ServiceNow write, delete, catalog checkout, CMDB, and attachment actions can modify operational records or create irreversible changes.

Mitigation: Use preview plus explicit user confirmation before executing these operations.

## Reference(s):

- [ClawHub ServiceNow Skill](https://clawhub.ai/hith3sh/skills/servicenow-it)
- [ServiceNow REST API Documentation](https://docs.servicenow.com/category/nav_to_landing_page)
- [ServiceNow Table API](https://docs.servicenow.com/en-US/docs/services/rest-table)
- [ServiceNow Change Management](https://docs.servicenow.com/category/change-management)
- [ServiceNow CMDB](https://docs.servicenow.com/category/configuration-management)
- [ServiceNow Service Catalog](https://docs.servicenow.com/category/service-catalog)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the live ServiceNow tool catalog exposed through ClawLink.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
