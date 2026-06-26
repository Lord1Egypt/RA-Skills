## Description: <br>
SendGrid email integration with API key authentication. Manage marketing campaigns, transactional templates, contacts, suppression lists, sender identities, IP pools, and event webhooks via the SendGrid API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a SendGrid account through ClawLink and manage email marketing, transactional email, contacts, suppressions, sender identities, IP pools, webhooks, and related account operations from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad SendGrid write capabilities, including API keys, SSO, teammates, subusers, IP allow-list changes, account provisioning, webhooks, and deletions. <br>
Mitigation: Use a least-privilege SendGrid API key, review the live tool catalog, and require preview plus explicit user confirmation before write operations. <br>
Risk: A connected SendGrid API key gives ClawLink access to the permissions granted on that key. <br>
Mitigation: Install only when the user trusts ClawLink with the SendGrid API key and is comfortable with the key's scoped permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/sendgrid-email) <br>
- [SendGrid API Documentation](https://docs.sendgrid.com/api-reference) <br>
- [SendGrid Marketing Campaigns API](https://docs.sendgrid.com/api-reference/campaigns-api) <br>
- [SendGrid Transactional Email](https://docs.sendgrid.com/ui/sending-email/how-to-send-email-with-transactional-templates) <br>
- [SendGrid IP Management](https://docs.sendgrid.com/ui/sending-email/ip-access-management) <br>
- [SendGrid Inbound Parse](https://docs.sendgrid.com/for-developers/parsing-email/setting-up-the-inbound-parse-webhook) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing setup steps, connection checks, tool-selection guidance, and SendGrid tool call examples.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
