## Description: <br>
AI Video Enhancement - Upscale video resolution, denoise, sharpen. Supports local files and YouTube/Bilibili URLs. HD/4K upscaling with real-time progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alouhaou](https://clawhub.ai/user/alouhaou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to route local video files or supported video URLs through verging.ai for denoising, sharpening, HD/4K upscaling, progress polling, and optional result download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos, including private local clips or downloaded URL media, are sent to verging.ai for processing. <br>
Mitigation: Use the skill only for media you are authorized to process, and confirm that the provider's retention and sharing terms are acceptable before sending sensitive content. <br>
Risk: The skill requires a VERGING_API_KEY credential. <br>
Mitigation: Set the key through the environment, avoid placing it in prompts or public files, and use a scoped or revocable key where available. <br>
Risk: Temporary media files may remain under /tmp/verging-video-enhancement/ if cleanup is not completed. <br>
Mitigation: Inspect and remove temporary files after processing, especially when handling private or regulated media. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alouhaou/video-enhancement) <br>
- [verging.ai](https://verging.ai) <br>
- [Verging API Docs](https://verging.ai/docs/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include result URLs and optional downloaded video files when requested.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
