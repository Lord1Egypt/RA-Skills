## Description: <br>
SMTP Email Delivery Service sends email through SMTP or SMTPS with plain text or HTML bodies, CC/BCC recipients, attachments, and priority settings for AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to send transactional, notification, report, and formatted email through an AgentPMT-hosted SMTP delivery tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles SMTP credentials and outbound email content. <br>
Mitigation: Use a scoped SMTP account or app password, keep credentials out of prompts and logs, and send only the minimum required email content. <br>
Risk: Outbound email can reach unintended recipients or expose private attachment data. <br>
Mitigation: Verify recipients, CC/BCC fields, message bodies, and attachments before delivery. <br>
Risk: Broad activation wording could be misread as permission for automatic email delivery. <br>
Mitigation: Require explicit user confirmation before sending email through the tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/smtp-email-delivery-service) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/smtp-email-delivery-service) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [AgentPMT MCP server](https://api.agentpmt.com/mcp/) <br>
- [AgentPMT REST invoke endpoint](https://api.agentpmt.com/products/purchase) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown instructions with JSON request examples and schema details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls return JSON responses from the AgentPMT email delivery service; attachments are base64 encoded and limited to 25MB total.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
