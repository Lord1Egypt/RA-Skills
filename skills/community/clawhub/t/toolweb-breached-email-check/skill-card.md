## Description:

Checks whether an email address appears in known data breaches and returns breach history, exposed data types, severity, paste exposure, and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and enterprise security practitioners use this skill to check onboarding, employee audit, and threat exposure workflows for email addresses that may have appeared in breaches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checked email addresses are sent to ToolWeb.in's breach-check service.

Mitigation: Use the skill only for addresses covered by an approved security workflow with consent and data-handling review.

Risk: Breach results and remediation guidance can affect user security decisions.

Mitigation: Review results before taking account actions, especially for employee, customer, or third-party addresses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-breached-email-check)
- [ToolWeb Breached Email Check API](https://portal.toolweb.in/apis/security/breached-email-check)
- [ToolWeb](https://toolweb.in)
- [ToolWeb Portal](https://portal.toolweb.in)
- [ToolWeb MCP Server](https://hub.toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API Calls]

**Output Format:** [Markdown with JSON examples and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends checked email addresses to ToolWeb.in and may require an API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
