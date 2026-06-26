## Description: <br>
Transform raw Roblox gameplay footage into platform-ready promotional content for TikTok, YouTube Shorts, Reels, and YouTube with smart trimming, aspect-ratio conversion, music sync, captions, and brand overlays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cogniwatchdev](https://clawhub.ai/user/cogniwatchdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game developers, content creators, and marketing teams use this skill to turn raw Roblox gameplay recordings into social and promotional video outputs for platforms such as TikTok, YouTube Shorts, Instagram Reels, and YouTube. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local video-processing commands can overwrite output files or folders selected by the user. <br>
Mitigation: Choose output paths deliberately, avoid pointing exports at important files, and review generated commands before execution. <br>
Risk: The skill depends on local tools and Python packages such as FFmpeg, ffmpeg-python, librosa, and optional Whisper support. <br>
Mitigation: Use a virtual environment, install dependencies from trusted sources, and process media files from trusted locations. <br>


## Reference(s): <br>
- [Brand Templates](references/brand-templates.md) <br>
- [Platform Specifications](references/platform-specs.md) <br>
- [Asset Guidance](assets/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated video-processing files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local video-editing plans, analysis JSON, captions, and platform-specific MP4 outputs when supporting scripts and dependencies are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
