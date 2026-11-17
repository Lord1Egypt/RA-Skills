## Description:

WhatsApp by Online Live Support integration helps agents manage WhatsApp Business support data, records, and workflows through Membrane.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratilsudra](https://clawhub.ai/user/pratilsudra)

### License/Terms of Use:

MIT-0

## Use Case:

Support agents, customer service teams, and developers use this skill to connect a Membrane account to WhatsApp by Online Live Support, discover available actions, run supported actions, and make authenticated proxy requests when required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use broad authenticated access to WhatsApp Business support data through Membrane.

Mitigation: Install only when that access is acceptable, use least-privilege Membrane connections where available, and require explicit user confirmation before sending messages, modifying records, or using non-read API methods.

Risk: The setup instructions use mutable CLI install commands.

Mitigation: Prefer a pinned and reviewed Membrane CLI version before deployment.

Risk: Raw proxy requests can bypass safer pre-built action behavior.

Mitigation: Use discovered pre-built actions first and reserve raw proxy calls for cases where an action does not cover the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pratilsudra/skills/whatsapp-pro2)
- [Membrane homepage](https://getmembrane.com)
- [WhatsApp Business Platform documentation](https://developers.facebook.com/docs/whatsapp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a valid Membrane account, and user authorization for the WhatsApp by Online Live Support connection.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
