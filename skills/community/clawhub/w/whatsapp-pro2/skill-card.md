## Description: <br>
WhatsApp by Online Live Support integration for managing WhatsApp Business API support data, records, and workflows through Membrane. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratilsudra](https://clawhub.ai/user/pratilsudra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support agents, customer service teams, and developers use this skill to connect a WhatsApp Business account through Membrane, discover available actions, run support workflows, and make supervised API requests when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw proxy requests or write actions could change WhatsApp Business account data. <br>
Mitigation: Prefer Membrane's listed actions and require explicit user confirmation before POST, PUT, PATCH, DELETE, message-sending, template-changing, or deletion operations. <br>
Risk: A connected WhatsApp Business account may expose customer support data to automated workflows. <br>
Mitigation: Review requested permissions during connection setup and limit use to intended support workflows. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/pratilsudra/whatsapp-pro2) <br>
- [Membrane homepage](https://getmembrane.com) <br>
- [WhatsApp Business Platform documentation](https://developers.facebook.com/docs/whatsapp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with shell commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid Membrane account, and user-approved connections before interacting with WhatsApp Business data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
