## Description:

Helps agents send PushPlus notifications across messaging channels and manage messages, recipients, bots, and delivery settings through its API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcstx](https://clawhub.ai/user/pcstx)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers use this skill to send alerts and reminders through PushPlus channels, check delivery, and manage related messaging settings when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages may disclose confidential or personal content to PushPlus and selected recipients.

Mitigation: Review the title, content summary, and recipients before approving a send; avoid secrets or personal data unless intentional.

Risk: PushPlus tokens and Open API credentials could be exposed in responses or logs.

Mitigation: Do not display full credentials; read only required variables and avoid persisting credentials.

Risk: Optional Open API actions can delete content, change rules, blacklist users, or alter bot bindings.

Mitigation: Require explicit confirmation before destructive or account-changing actions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/pcstx/skills/pushplus-notification)
- [PushPlus messaging API documentation](https://www.pushplus.plus/doc/guide/api.html)
- [PushPlus Open API documentation](https://www.pushplus.plus/doc/guide/openApi.html)
- [Skill Open API reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and delivery status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A request acceptance does not establish delivery; check the message result when confirmation is needed.]

## Skill Version(s):

1.3.6 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
