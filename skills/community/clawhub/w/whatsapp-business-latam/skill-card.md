## Description:

Configuracion completa de WhatsApp Business API oficial de Meta para PyMEs de Argentina y LATAM, including setup, Spanish HSM templates, OpenClaw configuration, compliance guidance, and curl examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[centriqs](https://clawhub.ai/user/centriqs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and SMB teams in Argentina and LATAM use this skill to configure Meta's official WhatsApp Business Cloud API, prepare reusable Spanish message templates, and connect WhatsApp messaging workflows to OpenClaw.

### Deployment Geography for Use:

Argentina and Latin America (LATAM)

## Known Risks and Mitigations:

Risk: The skill guides users through live customer messaging with long-lived Meta credentials.

Mitigation: Store Meta tokens in a secret manager, avoid non-expiring or admin tokens where possible, and explicitly review recipient numbers and message content before live sends.

Risk: Webhook handling and logging may expose customer message data or full webhook bodies.

Mitigation: Use a webhook endpoint under the user's own domain or cloud account, remove full webhook-body logging, and redact customer fields in logs.

Risk: WhatsApp account quality or compliance failures can affect production messaging access.

Mitigation: Confirm opt-in evidence, approved templates, Meta service-window rules, and anti-ban checklist items before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/centriqs/skills/whatsapp-business-latam)
- [Centriqs Homepage](https://centriqs.io)
- [OpenClaw](https://openclaw.ai)
- [WhatsApp Business Platform](https://business.whatsapp.com/)
- [WhatsApp Platform Pricing](https://business.whatsapp.com/products/platform-pricing)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON, JavaScript, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Spanish WhatsApp template copy, Meta Cloud API curl examples, OpenClaw configuration snippets, and compliance checklists.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
