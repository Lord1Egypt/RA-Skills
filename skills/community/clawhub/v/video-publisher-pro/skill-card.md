## Description:

根据IP背景和视频文案，为短视频生成一套完整的发布策略，包括发布时间、话题标签、封面文案和发布标题，并能将文案合成为封面图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, short-video operators, and agents use this skill to turn IP background, weekly goals, video scripts, and video positioning into publishing recommendations. It can also prepare cover-image generation prompts and commands for placing generated cover copy on user-supplied images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External image upload and configurable API endpoints can expose user images or prompts to an untrusted provider.

Mitigation: Use only a fixed trusted HTTPS provider, a dedicated low-privilege API key, and images the user owns or is allowed to edit.

Risk: The cover workflow can create official-looking, watermark-free edits or alter third-party branded assets.

Mitigation: Do not use the workflow on official documents, third-party branded assets, watermarks, or provenance marks.

Risk: The image script writes api_response_content.log, which can persist sensitive request or response content.

Mitigation: Disable or delete the log when sensitive material is processed and use a clean output directory.

Risk: Publishing recommendations may be inaccurate or misaligned with audience behavior or platform norms.

Mitigation: Have a human operator review publish timing, hashtags, titles, and cover copy before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahsbnb/skills/video-publisher-pro)
- [Skill definition](artifact/SKILL.md)
- [Strategy prompt template](artifact/prompt_template.txt)
- [Replication mode prompt](artifact/scripts/replication_prompt.txt)
- [Fusion mode prompt](artifact/scripts/fusion_prompt.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown strategy report with optional shell command guidance and generated image output path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided background information, weekly goals, video script, video positioning, and optionally an image plus cover text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
