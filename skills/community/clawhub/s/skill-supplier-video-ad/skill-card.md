## Description: <br>
Transforms supplier or CJ source videos into 1080x1920 TikTok and Instagram Reels ads with clean zone detection, Pillow text overlays, a CTA card, and audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and ecommerce operators use this skill to turn raw supplier or CJ Dropshipping footage into ready-to-post short-form product ads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An unvalidated configuration value can write or delete files outside the intended output folder. <br>
Mitigation: Use only trusted configs, keep output_name to a simple filename, reject absolute paths or ../ segments, and run from a scratch directory. <br>
Risk: Supplier footage, logos, or music may not be licensed for commercial advertising. <br>
Mitigation: Verify usage rights for all source media, logos, fonts, and audio before publishing generated ads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-supplier-video-ad) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, code, files, guidance] <br>
**Output Format:** [Markdown instructions with bash commands, JSON configuration, Python scripts, extracted frame files, and MP4 video output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 1080x1920 H.264/AAC MP4 ads and helper frame extracts when run with ffmpeg, ffprobe, Pillow, source videos, fonts, audio, and brand assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
