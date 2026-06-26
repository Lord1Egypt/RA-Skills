## Description: <br>
Resend API integration with managed authentication for sending transactional emails and managing domains, contacts, templates, broadcasts, webhooks, and API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage a connected Resend account through Maton, including sending transactional or broadcast email and administering domains, templates, contacts, webhooks, and API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MATON_API_KEY grants access to connected Resend account operations. <br>
Mitigation: Keep MATON_API_KEY private and install the skill only when you intend to manage a Resend account through Maton. <br>
Risk: Write operations can send email, modify account resources, configure webhooks, or create and delete API keys. <br>
Mitigation: Approve create, update, send, and delete operations only after checking recipients, sender, content, webhook destination, resource IDs, and API key impact. <br>
Risk: Multiple Resend connections can cause requests to target the wrong account. <br>
Mitigation: Use the intended Maton connection and include the Maton-Connection header when multiple connections exist. <br>


## Reference(s): <br>
- [ClawHub Resend Skill](https://clawhub.ai/byungkyu/resend-api) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Resend API Documentation](https://resend.com/docs/api-reference/introduction) <br>
- [Resend Dashboard](https://resend.com) <br>
- [ClawHub API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python, JavaScript, shell command, HTTP endpoint, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
