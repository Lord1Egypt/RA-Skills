## Description: <br>
Manage temporary email addresses and messages using the chat-tempmail.com API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Selenium39](https://clawhub.ai/user/Selenium39) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create disposable email addresses, check inbox messages, delete temporary addresses or messages, and configure message webhooks through the chat-tempmail.com API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request or use a chat-tempmail.com API key. <br>
Mitigation: Configure TEMP_EMAIL_API_KEY through an environment variable or secret manager instead of pasting secrets into chat. <br>
Risk: Webhook configuration can forward email contents and metadata to a configured endpoint. <br>
Mitigation: Configure webhooks only for trusted endpoints that you control and that are approved to receive message content. <br>
Risk: Delete operations can remove temporary email addresses or individual messages. <br>
Mitigation: Confirm exact email and message IDs before running delete requests. <br>


## Reference(s): <br>
- [Temporary Email skill page](https://clawhub.ai/Selenium39/temp-email) <br>
- [chat-tempmail.com API](https://chat-tempmail.com) <br>
- [chat-tempmail.com API Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with curl commands and readable summaries of JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEMP_EMAIL_API_KEY for authenticated requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
