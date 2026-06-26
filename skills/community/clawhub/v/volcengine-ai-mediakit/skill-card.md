## Description: <br>
Volcengine AI MediaKit helps agents upload, edit, enhance, analyze, translate, and query audio/video assets through Volcengine VOD workflows, returning task IDs and generated playback links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-ai-mediakit](https://clawhub.ai/user/volc-ai-mediakit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, media operators, and content teams use this skill to run Volcengine-backed audio and video processing workflows such as clipping, stitching, enhancement, subtitle handling, translation, and media metadata lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Volcengine VOD credentials to upload, process, store, bill for, and in some cases publish media. <br>
Mitigation: Install only when the publisher is trusted, use least-privilege Volcengine credentials, and confirm account, storage, billing, and publishing expectations before running media workflows. <br>
Risk: Media information lookup can expose or publish private or draft asset information. <br>
Mitigation: Avoid running get_media_info on private or draft assets unless making those assets accessible is acceptable. <br>
Risk: Generated playback links and processed outputs may reveal user media or derived content. <br>
Mitigation: Review links before sharing them and keep source media, generated outputs, and task IDs within the intended audience. <br>


## Reference(s): <br>
- [Capabilities overview](references/00-detail.md) <br>
- [Billing instructions](references/00-billing-instructions.md) <br>
- [Video and audio stitching](references/01-stitching.md) <br>
- [Clipping](references/02-clipping.md) <br>
- [Speed adjustment](references/04-speedup.md) <br>
- [Image to video](references/05-image-to-video.md) <br>
- [Audio extraction](references/07-extract-audio.md) <br>
- [Quality enhancement](references/12-quality-enhance.md) <br>
- [Super resolution](references/13-super-resolution.md) <br>
- [ASR speech to text](references/15-asr-speech-to-text.md) <br>
- [OCR text extraction](references/16-ocr-text-extract.md) <br>
- [Video translation](references/24-video-translation.md) <br>
- [Drama recap](references/25-drama-recap.md) <br>
- [Drama script](references/26-drama-script.md) <br>
- [Media information lookup](references/27-get-media-info.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON script output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Volcengine task IDs, resume commands, media metadata, generated asset references, and playback URLs.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
