## Description: <br>
WhatsApp Business API integration with managed OAuth for sending messages, managing templates, handling media, and interacting with customers through WhatsApp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raidan-ai](https://clawhub.ai/user/raidan-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to guide an agent through WhatsApp Business API operations via Maton, including sending messages, managing OAuth connections, templates, media, phone numbers, and business profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to send real WhatsApp Business messages or modify WhatsApp Business resources. <br>
Mitigation: Confirm recipients, message text, media, phone number IDs, template changes, and delete operations before execution. <br>
Risk: The Maton API key grants access to connected WhatsApp Business operations. <br>
Mitigation: Store MATON_API_KEY securely, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected. <br>
Risk: Customer or regulated data may be sent through WhatsApp Business workflows. <br>
Mitigation: Avoid sending regulated or unauthorized customer data unless the user has confirmed the data handling requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/raidan-ai/whatsapp-business-1-0-3) <br>
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
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples, Python and JavaScript code snippets, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and a valid MATON_API_KEY; generated requests can affect real WhatsApp Business messaging and connection state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence); artifact metadata version 1.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
