## Description: <br>
Operate WhatsApp Business Platform Cloud API through UXC with a curated OpenAPI schema, bearer-token auth, and message/profile guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure UXC access to WhatsApp Business Platform Cloud API operations, inspect available request schemas, read phone number and business profile data, and perform guarded message or profile writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WhatsApp Business Cloud API credentials to send real messages or update a live business profile. <br>
Mitigation: Review message sends and business profile updates before execution, and use the least-privileged Meta token practical for the target assets. <br>
Risk: Successful authentication does not guarantee that a message is allowed by WhatsApp policy, conversation rules, template approval, recipient opt-in, or account state. <br>
Mitigation: Validate account setup with read operations first and require explicit user confirmation before message sends. <br>
Risk: The skill does not host an inbound webhook receiver or manage webhook verification. <br>
Mitigation: Keep webhook setup and receiver runtime outside this skill, using it only for documented request and response operations. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/whatsapp-cloud.openapi.json) <br>
- [WhatsApp Cloud API docs](https://developers.facebook.com/docs/whatsapp/cloud-api) <br>
- [Graph API access tokens](https://developers.facebook.com/docs/graph-api/overview/access-tokens/) <br>
- [ClawHub release page](https://clawhub.ai/jolestar/whatsapp-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead to live WhatsApp API calls when the user supplies credentials and confirms write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
