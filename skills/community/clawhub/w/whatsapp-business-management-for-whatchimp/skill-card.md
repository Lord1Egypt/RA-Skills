## Description: <br>
Operating doctrine for WhatsApp Business automation on Whatchimp, covering 24-hour-window handling, template-gated outbound messaging, lead qualification, anti-duplicate controls, cross-platform lead intake, and recovery patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to configure WhatsApp Business automation for opt-in lead conversion, including inbound replies, approved outbound templates, qualification flows, human-team alerts, CRM state tracking, and recovery procedures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags user-facing AI non-disclosure instructions as requiring careful review. <br>
Mitigation: Edit the identity rules before installation so the agent gives truthful disclosure when users ask whether they are speaking with automation. <br>
Risk: The skill handles lead personal data in memory files, CRM records, and alert channels. <br>
Mitigation: Use explicit opt-in, restrict alert channels, mask identifiers where possible, and define retention and deletion rules for lead records and memory files. <br>
Risk: WhatsApp automation can create account, compliance, or deliverability risk if messages bypass opt-in, approved templates, or the 24-hour customer-service window. <br>
Mitigation: Use approved WhatsApp templates, scoped API credentials, quality and tier gating, anti-duplicate checks, and human review for operating limits before deployment. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [ClawHub listing](https://clawhub.ai/alexbloch-ia/whatsapp-business-management-for-whatchimp) <br>
- [Whatchimp](https://whatchimp.com) <br>
- [Whatchimp API base URL](https://app.whatchimp.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with YAML configuration examples, curl commands, operating checklists, and state-file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires brand placeholders, WhatsApp Business/BSP credentials, approved templates, CRM identifiers, alert channels, and local state files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and README version badge) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
