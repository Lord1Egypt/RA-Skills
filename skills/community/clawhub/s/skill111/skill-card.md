## Description: <br>
WhatsApp Business API integration with managed OAuth for sending messages, managing templates, and handling conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenhee350-a11y](https://clawhub.ai/user/kenhee350-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to connect an agent to WhatsApp Business through Maton-managed OAuth, send customer messages, manage message templates, and inspect or update WhatsApp Business resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send live WhatsApp messages, including business messages to external recipients. <br>
Mitigation: Require manual approval before sending messages, and verify recipient phone numbers, message content, and the selected WhatsApp Business connection before execution. <br>
Risk: The skill includes mutating or destructive business-account actions such as deleting connections, deleting media, deleting templates, and changing business profile resources. <br>
Mitigation: Use least-privilege credentials, explicitly specify the intended connection for each mutating action, and require approval before deleting or changing business resources. <br>
Risk: The skill depends on a Maton API key and managed OAuth connections for WhatsApp Business access. <br>
Mitigation: Install only when the Maton provider is trusted for the workflow, keep MATON_API_KEY scoped and protected, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kenhee350-a11y/skill111) <br>
- [WhatsApp Business API Overview](https://developers.facebook.com/docs/whatsapp/cloud-api/overview) <br>
- [Send Messages](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages) <br>
- [Message Templates](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates) <br>
- [WhatsApp Media](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media) <br>
- [WhatsApp Error Codes](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes) <br>
- [Maton settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with HTTP examples and Python, JavaScript, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
