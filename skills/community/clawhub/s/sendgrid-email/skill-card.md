## Description:

SendGrid email integration with API key authentication. Manage marketing campaigns, transactional templates, contacts, suppression lists, sender identities, IP pools, and event webhooks via the SendGrid API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to connect an agent to Twilio SendGrid through ClawLink, then manage contacts, campaigns, templates, sender identities, suppressions, IP pools, webhooks, and related account resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes SendGrid API access through a hosted proxy that is not included for review.

Mitigation: Use a dedicated SendGrid API key with the minimum scopes needed, and revoke or rotate the key when the integration is no longer needed.

Risk: The skill asks users to allowlist an unpinned external plugin.

Mitigation: Review the plugin before installation and allowlist only the trusted ClawHub release required for this integration.

Risk: The skill exposes write-capable SendGrid operations, including destructive account, suppression, webhook, sender, IP, and access-management changes.

Mitigation: Preview and explicitly confirm create, update, and delete operations, and avoid granting admin, API-key, SSO, or teammate permissions unless required.

## Reference(s):

- [ClawHub SendGrid Skill Page](https://clawhub.ai/hith3sh/skills/sendgrid-email)
- [SendGrid API Documentation](https://docs.sendgrid.com/api-reference)
- [SendGrid Marketing Campaigns API](https://docs.sendgrid.com/api-reference/campaigns-api)
- [SendGrid Transactional Email](https://docs.sendgrid.com/ui/sending-email/how-to-send-email-with-transactional-templates)
- [SendGrid IP Management](https://docs.sendgrid.com/ui/sending-email/ip-access-management)
- [SendGrid Inbound Parse](https://docs.sendgrid.com/for-developers/parsing-email/setting-up-the-inbound-parse-webhook)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ClawLink tool names and JSON parameters; write operations should be previewed and confirmed before execution.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
