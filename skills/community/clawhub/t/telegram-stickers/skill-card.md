## Description: <br>
Create Telegram stickers from images as static PNG stickers or animated WebM video stickers, including background removal, resizing to Telegram specifications, animation, and upload workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saintsola13](https://clawhub.ai/user/saintsola13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to convert images into Telegram-ready sticker assets and to follow the correct @Stickers bot workflow for static or video sticker packs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Animated sticker creation can upload generated WebM files to tmpfiles.org by default. <br>
Mitigation: Use the documented --no-upload option for personal photos, private artwork, copyrighted material, or any content that should not be sent to tmpfiles.org. <br>
Risk: The workflow depends on local image processing packages and ffmpeg. <br>
Mitigation: Install Python packages and ffmpeg from trusted sources and review generated files before sharing or uploading them. <br>


## Reference(s): <br>
- [@Stickers Bot Step-by-Step Guide](references/stickers-bot-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/saintsola13/telegram-stickers) <br>
- [Publisher profile](https://clawhub.ai/user/saintsola13) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated PNG or WebM sticker files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static output is a 512x512 PNG sticker; animated output is a VP9 WebM video sticker generated from PNG frames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
