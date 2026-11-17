## Description:

Guides an agent through onboarding a user to WhatsApp via WAHA by collecting a phone number, creating and starting a session, requesting a pairing code, checking authentication status, and offering next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotfinity](https://clawhub.ai/user/lotfinity)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to connect a WhatsApp account through a trusted WAHA deployment and complete pairing-code onboarding before accessing recent conversations, contacts, or a specific chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill links a WhatsApp account through WAHA and exposes a phone number in session metadata.

Mitigation: Review before installing, use only a trusted WAHA deployment, avoid phone numbers in session names where possible, and remove the linked device in WhatsApp when access is no longer needed.

Risk: The security guidance says the artifact lacks explicit consent, scope, retention, and revocation instructions.

Mitigation: Define consent, allowed actions, data retention, and revocation steps before using the skill in a production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lotfinity/skills/waha-onboarding)
- [Publisher profile](https://clawhub.ai/user/lotfinity)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks and procedural text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a WAHA CLI deployment and a user phone number with country code.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
