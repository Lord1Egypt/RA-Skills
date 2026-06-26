## Description: <br>
SendGrid API integration with managed OAuth for sending emails and managing contacts, templates, suppressions, statistics, sender identities, unsubscribe groups, and SendGrid API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with SendGrid accounts from an agent session, including sending transactional or marketing email, managing audience and suppression resources, and reviewing delivery statistics. It requires a Maton API key and a connected SendGrid account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email to real recipients and change SendGrid resources. <br>
Mitigation: Confirm the target account, recipients, sender, content, and intended resource changes before any write operation. <br>
Risk: API key management can create or modify long-lived SendGrid credentials. <br>
Mitigation: Use API-key endpoints only when the user explicitly requests credential management, and do not expose created key values in output. <br>
Risk: Access depends on trusting Maton as the OAuth and API proxy and on handling a sensitive MATON_API_KEY. <br>
Mitigation: Install only if the publisher and Maton proxy are trusted, and provide only a Maton API key intended for SendGrid access. <br>


## Reference(s): <br>
- [ClawHub SendGrid skill](https://clawhub.ai/byungkyu/sendgrid) <br>
- [SendGrid API Documentation](https://www.twilio.com/docs/sendgrid/api-reference) <br>
- [SendGrid Mail Send API](https://www.twilio.com/docs/sendgrid/api-reference/mail-send) <br>
- [SendGrid Marketing Contacts API](https://www.twilio.com/docs/sendgrid/api-reference/contacts) <br>
- [SendGrid Suppressions Overview](https://www.twilio.com/docs/sendgrid/api-reference/suppressions) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with JSON examples and inline shell, Python, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute SendGrid API requests through Maton when the user provides MATON_API_KEY and explicitly approves write operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
