## Description:

Phone number formatting, cache inspection, contact export, and message ID generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosrippel](https://clawhub.ai/user/marcosrippel)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation operators use this skill to run small WhatsApp utility commands for normalizing phone numbers, inspecting local OpenClaw WhatsApp cache state, exporting contacts, and generating WhatsApp-style message IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export-contacts command can print the full local WhatsApp contact list into agent output.

Mitigation: Run export-contacts only when full contact export is intentional, and prefer confirmation, filtering, or redaction before routine use with real contacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcosrippel/skills/whatsapp-utils)
- [Publisher profile](https://clawhub.ai/user/marcosrippel)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON objects printed by Node.js utility commands, with Markdown command examples in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Phone formatting defaults local 10- or 11-digit numbers to Brazil country code +55; cache and contact commands read from the local OpenClaw WhatsApp credential state directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
