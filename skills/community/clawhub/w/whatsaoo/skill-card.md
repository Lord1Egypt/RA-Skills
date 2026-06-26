## Description: <br>
WhatsApp Business API integration with managed OAuth for sending messages, managing templates, handling media, and working with customer conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notRellz](https://clawhub.ai/user/notRellz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and operators use this skill to interact with WhatsApp Business through Maton-managed OAuth, including customer messaging, message templates, media, phone numbers, and business profile actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send customer messages and perform account-changing WhatsApp Business actions through a third-party gateway. <br>
Mitigation: Require manual confirmation before sending messages, deleting media, deleting templates, deleting connections, or changing the business profile. <br>
Risk: Requests may use the wrong WhatsApp connection or phone number ID when multiple accounts are available. <br>
Mitigation: Explicitly choose the intended Maton connection and WhatsApp phone number ID before making API calls. <br>
Risk: The skill requires access to WhatsApp Business message content, recipient phone numbers, media, and account actions. <br>
Mitigation: Install only when Maton is trusted for this data and authority, and protect MATON_API_KEY as a sensitive credential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/notRellz/whatsaoo) <br>
- [WhatsApp Business API Overview](https://developers.facebook.com/docs/whatsapp/cloud-api/overview) <br>
- [Send Messages](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages) <br>
- [Message Templates](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates) <br>
- [Media](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media) <br>
- [Phone Numbers](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/phone-numbers) <br>
- [Business Profiles](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/business-profiles) <br>
- [Webhooks](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks) <br>
- [Error Codes](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes) <br>
- [Maton](https://maton.ai) <br>
- [Maton control panel](https://ctrl.maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, JavaScript, HTTP, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; generated commands can call Maton and WhatsApp Business APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved ClawHub release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
