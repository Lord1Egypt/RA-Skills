## Description:

List, search, and lookup WhatsApp contacts from the Baileys session cache.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosrippel](https://clawhub.ai/user/marcosrippel)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agents use this skill to list, search, and inspect WhatsApp contacts previously cached for the default local Baileys session. It is useful when a workflow needs contact names, phone numbers, or cached contact details without opening a live WhatsApp connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can display private contact metadata from the local WhatsApp Baileys cache.

Mitigation: Install and use it only where exposing cached contact names, phone numbers, statuses, group identifiers, and image URLs is acceptable.

Risk: Contact results can be reused in later agent conversations or workflows.

Mitigation: Treat output as private and avoid passing it into contexts where contact names or phone numbers should not be disclosed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marcosrippel/skills/whatsapp-contacts)
- [Publisher Profile](https://clawhub.ai/user/marcosrippel)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [JSON emitted by a Node CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contact output may include private names, phone numbers, group identifiers, statuses, and image URLs from the local cache.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
