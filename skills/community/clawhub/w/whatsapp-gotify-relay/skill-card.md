## Description:

Helps agents operate and extend a WhatsApp-Gotify relay that bridges OpenClaw outbound messages and inbound WhatsApp events through Gotify, webhooks, Docker, and command-line workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jr551](https://clawhub.ai/user/jr551)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain a WhatsApp-Gotify relay for OpenClaw, including testing, queue inspection, webhook validation, Docker rebuilds, and payload contract changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands may interact with live Gotify, webhook, Docker, or WhatsApp relay environments.

Mitigation: Review configured Gotify and webhook URLs, protect bearer and app tokens, and confirm manual smoke-test recipients before running curl or Docker operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jr551/skills/whatsapp-gotify-relay)
- [Gotify WhatsApp Queue Repository](https://github.com/jr551/gotify-whatsapp-queue)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command proposals for Docker, npm, curl, Gotify queue inspection, webhook validation, and relay configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
