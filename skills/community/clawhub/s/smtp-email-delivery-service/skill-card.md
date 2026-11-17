## Description:

SMTP Email Delivery Service helps agents send SMTP or SMTPS email with plain text or HTML bodies, CC/BCC recipients, attachments, and priority settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to configure AgentPMT-hosted remote calls that send transactional, notification, newsletter, or report emails through a chosen SMTP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP credentials and email contents are sent through a remote intermediary.

Mitigation: Use a dedicated, least-privilege app password or service SMTP account, and avoid confidential content unless AgentPMT is trusted for that data.

Risk: Automated email delivery can send messages to unintended recipients or include unintended attachments.

Mitigation: Verify every recipient, CC/BCC list, subject, body, and attachment before invoking the send action.

Risk: Setup commands can install or run external skill packages.

Mitigation: Review referenced setup skills and unpinned npx commands before using them in a production integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/smtp-email-delivery-service)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/smtp-email-delivery-service)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [guidance, configuration, code, shell commands]

**Output Format:** [Markdown with JSON request examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines one send action for SMTP email delivery through AgentPMT-hosted MCP or REST calls.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
