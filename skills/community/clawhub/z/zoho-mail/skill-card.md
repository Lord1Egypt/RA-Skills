## Description: <br>
Zoho Mail API integration with managed OAuth for sending, receiving, searching, and managing emails, folders, and labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide authenticated Zoho Mail API calls through Maton for reading and sending messages, searching mail, and managing folders and labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive Zoho Mail data through Maton-mediated access to a connected account. <br>
Mitigation: Install only when that access is intended, use the narrowest practical Maton and Zoho permissions, and remove the Maton connection when it is no longer needed. <br>
Risk: Write operations can send email, delete messages, move messages, apply labels, modify folders, or handle attachments. <br>
Mitigation: Confirm the target resource and intended effect with the user before any create, update, delete, send, move, label, folder, or attachment action runs. <br>
Risk: Multiple Zoho Mail connections can cause requests to affect the wrong account. <br>
Mitigation: Use the Maton-Connection header when multiple active Zoho Mail connections exist. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/zoho-mail) <br>
- [Maton](https://maton.ai) <br>
- [Zoho Mail API Overview](https://www.zoho.com/mail/help/api/overview.html) <br>
- [Zoho Mail API Index](https://www.zoho.com/mail/help/api/) <br>
- [Email Messages API](https://www.zoho.com/mail/help/api/email-api.html) <br>
- [Getting Started with Zoho Mail API](https://www.zoho.com/mail/help/api/getting-started-with-api.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, JavaScript, shell, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Zoho Mail OAuth account.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
