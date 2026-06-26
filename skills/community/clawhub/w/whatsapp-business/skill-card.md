## Description: <br>
WhatsApp Business API integration with managed OAuth for sending messages, managing templates, handling media, and managing customer conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to connect a WhatsApp Business account through Maton, send customer messages, manage templates and media, and inspect or update account resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Maton as an intermediary for WhatsApp Business account access and message data. <br>
Mitigation: Install only when Maton is trusted for the connected account, and revoke unused OAuth connections. <br>
Risk: The integration can send messages and create, update, or delete WhatsApp Business resources. <br>
Mitigation: Confirm recipients, connection IDs, message contents, target resources, and intended effects before any write or destructive request. <br>
Risk: MATON_API_KEY is a sensitive credential for the integration. <br>
Mitigation: Keep the key private, pass it through the environment only, and rotate or remove it when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/whatsapp-business) <br>
- [WhatsApp Business API Overview](https://developers.facebook.com/docs/whatsapp/cloud-api/overview) <br>
- [Send Messages](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages) <br>
- [Message Templates](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates) <br>
- [Media](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media) <br>
- [Phone Numbers](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/phone-numbers) <br>
- [Business Profiles](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/business-profiles) <br>
- [Webhooks](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks) <br>
- [Error Codes](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with REST endpoint descriptions and inline Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user approval before write or destructive API calls.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
