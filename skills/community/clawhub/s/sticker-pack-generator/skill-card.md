## Description:

Generates custom WhatsApp, Telegram, emoji-style, chibi, reaction, kawaii, and cartoon sticker images from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request AI-generated sticker pack images from text descriptions, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's prompt, optional reference image UUID, and Neta API token to api.talesofai.com.

Mitigation: Avoid private prompts or personal data, use a limited or disposable token, and install only if this external API use is acceptable.

Risk: The npx installation command can resolve mutable package or source state.

Mitigation: Pin the installer or source version when repeatability matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/skills/sticker-pack-generator)
- [Neta API Token Page](https://www.neta.art/open/)
- [Neta Image Generation Endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Image URL]

**Output Format:** [Text output containing a direct generated image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided text prompt, Neta API token, optional size, and optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
