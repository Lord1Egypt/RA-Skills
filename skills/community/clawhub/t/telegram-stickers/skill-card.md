## Description:

Create Telegram stickers from images: static PNG stickers or animated WebM video stickers with background removal, resizing, animation, and Telegram upload guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saintsola13](https://clawhub.ai/user/saintsola13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to turn photos or artwork into Telegram-ready sticker files and to follow the @Stickers bot workflow for static and video sticker packs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Animated sticker generation uploads files to tmpfiles.org by default, which may expose private images or proprietary artwork.

Mitigation: Use --no-upload for local-only output and avoid processing sensitive images unless uploads are disabled.

Risk: The skill depends on local image processing packages, ffmpeg, and the rembg model download.

Mitigation: Install dependencies in a non-privileged virtual environment and review generated commands before execution.

## Reference(s):

- [@Stickers Bot Step-by-Step Guide](references/stickers-bot-guide.md)
- [ClawHub release page](https://clawhub.ai/saintsola13/skills/telegram-stickers)
- [tmpfiles.org upload endpoint](https://tmpfiles.org/api/v1/upload)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG and WebM files with Markdown guidance and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Animated WebM stickers may upload to tmpfiles.org by default unless --no-upload is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
