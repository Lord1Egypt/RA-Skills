## Description: <br>
Sendivent provides agent guidance for using a multi-channel notification API across email, SMS, Slack, push, Telegram, WhatsApp, and Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oakleaf](https://clawhub.ai/user/oakleaf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to integrate Sendivent notifications, manage contacts, inspect delivery data, configure webhooks, and produce API or SDK implementation examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill can draft or execute workflows that send real notifications and change Sendivent contact data. <br>
Mitigation: Start with sandbox or test keys, confirm production recipients and contact deletions before execution, and use idempotency keys for send operations. <br>
Risk: Webhook signing secrets and API keys can be mishandled if copied into logs, examples, or shared prompts. <br>
Mitigation: Store secrets in environment or secret-management systems, avoid logging webhook signing secrets, and review generated code before using production credentials. <br>


## Reference(s): <br>
- [Sendivent API Guide](references/api-guide.md) <br>
- [Sendivent Node.js SDK Guide](references/sdk-guide.md) <br>
- [Sendivent Documentation](https://sendivent.com/docs) <br>
- [Sendivent Node.js SDK](https://github.com/appitudeio/sendivent-node) <br>
- [Sendivent PHP SDK](https://github.com/appitudeio/sendivent-php) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON, TypeScript, REST, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include examples that use Sendivent API keys, sandbox or production base URLs, event names, channel settings, contact identifiers, and webhook configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
