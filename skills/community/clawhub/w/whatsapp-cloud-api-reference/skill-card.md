## Description: <br>
Use when implementing WhatsApp messaging via Meta Cloud API, or diagnosing failures like message not delivered, template rejected, webhook issues, phone not registered, token errors, rate limiting, 24-hour window violations, quality rating drops, or setup mistakes on the WhatsApp Business API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RomanBaz](https://clawhub.ai/user/RomanBaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to implement WhatsApp Cloud API messaging and troubleshoot setup, delivery, template, webhook, token, rate limit, and 24-hour conversation window issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A helper for checking WhatsApp registration can send a real message while presenting itself as a validation check. <br>
Mitigation: Do not use probe-by-message validation; use the documented contacts lookup or verified opt-in records before sending. <br>
Risk: WhatsApp Cloud API integrations handle access tokens, phone numbers, webhook payloads, and message contents. <br>
Mitigation: Store Meta System User tokens in a secret manager, avoid logging message contents or full phone numbers, secure webhook verification, and message only opted-in recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RomanBaz/whatsapp-cloud-api-reference) <br>
- [Meta Graph API versions endpoint](https://graph.facebook.com/versions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WhatsApp Cloud API request examples, webhook patterns, troubleshooting checklists, and operational constraints; the skill itself does not generate files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
