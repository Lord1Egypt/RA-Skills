## Description:

Provides Sendivent API guidance for sending multi-channel notifications via email, SMS, Slack, push, Telegram, WhatsApp, or Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oakleaf](https://clawhub.ai/user/oakleaf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this skill to write Sendivent integrations for notification sending, contact management, events, templates, webhooks, and Node.js SDK workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide real production notification sends, which may contact end users or trigger provider costs.

Mitigation: Prefer sandbox keys for testing and require explicit confirmation before sending real notifications.

Risk: The skill covers destructive operations such as deleting contacts, removing push tokens, and deleting webhooks.

Mitigation: Require a lookup or read-back step plus explicit user confirmation before performing destructive actions.

Risk: The skill documents API keys and webhook signing secrets, which can expose production messaging infrastructure if logged or shared.

Mitigation: Avoid printing or storing secrets in logs, keep credentials in environment variables, and protect webhook signing secrets.

Risk: The server security summary flags insufficient safeguards around production messaging, deletion, and webhook-secret workflows.

Mitigation: Review the skill before installing it for production credential use and pin install or package versions where applicable.

## Reference(s):

- [Sendivent API Reference](references/api-guide.md)
- [Sendivent Node.js SDK Guide](references/sdk-guide.md)
- [Sendivent Documentation](https://sendivent.com/docs)
- [Sendivent Node.js SDK](https://github.com/appitudeio/sendivent-node)
- [Sendivent PHP SDK](https://github.com/appitudeio/sendivent-php)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code examples, shell commands, JSON payloads, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, SDK usage patterns, and configuration steps for Sendivent credentials, channels, events, and webhooks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
