## Description:

Convert images into WebP stickers and send native WhatsApp stickers through an existing Baileys bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakumdisinipa](https://clawhub.ai/user/sakumdisinipa)

### License/Terms of Use:

MIT

## Use Case:

Hermes Agent users with a trusted, authenticated WhatsApp bridge can turn a local image into a native sticker and send it to a user-confirmed chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An untrusted or exposed bridge could access private images or misuse the authenticated WhatsApp session.

Mitigation: Use only a trusted bridge and account; bind the bridge to localhost or secure remote access, and avoid sensitive images or credentials.

Risk: A sticker could be sent to the wrong chat.

Mitigation: Confirm the recipient chat ID with the user before sending.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/SakumDisiniPa/whatsapp-sticker)
- [ClawHub skill release](https://clawhub.ai/sakumdisinipa/skills/whatsapp-sticker-v2)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, converts an image to a WebP sticker and requests delivery through the existing bridge; a successful request does not guarantee recipient receipt.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
