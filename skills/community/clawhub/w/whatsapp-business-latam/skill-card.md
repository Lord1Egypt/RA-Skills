## Description: <br>
Guides OpenClaw users through configuring Meta's official WhatsApp Business Cloud API for SMBs in Argentina and LATAM, including setup, Spanish HSM templates, compliance guidance, and curl examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[centriqs](https://clawhub.ai/user/centriqs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators supporting SMBs in Argentina and LATAM use this skill to set up official WhatsApp Business messaging, prepare Meta-approved HSM templates, configure OpenClaw, and apply opt-in and compliance checklists before production sends. <br>

### Deployment Geography for Use: <br>
Latin America, with Argentina-specific examples and guidance. <br>

## Known Risks and Mitigations: <br>
Risk: Meta access tokens, webhook verify tokens, phone number IDs, or WABA IDs may be exposed through chat transcripts, repositories, configuration files, or logs. <br>
Mitigation: Keep credentials out of chats and repositories, restrict local config and log permissions, prefer environment variables, and rotate any exposed tokens. <br>
Risk: Sending WhatsApp messages without valid opt-in or outside Meta's template and service-window rules can lead to account quality issues or number suspension. <br>
Mitigation: Confirm explicit recipient opt-in, use approved templates when required, monitor quality rating and messaging tiers, and follow Meta policy before production sends. <br>
Risk: Webhook traffic may be routed through an endpoint the user does not fully control or trust. <br>
Mitigation: Use a webhook endpoint controlled by the deploying organization, or explicitly approve and monitor any managed-service endpoint before connecting production WhatsApp traffic. <br>


## Reference(s): <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [WhatsApp Business Platform](https://business.whatsapp.com/) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Centriqs](https://centriqs.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/centriqs/whatsapp-business-latam) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, JavaScript, and bash/curl code blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Spanish HSM template text and placeholder credentials; users must supply Meta account IDs, tokens, recipient numbers, and webhook URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
