## Description:

Generate Xiaohongshu (小红书) cover images with Chinese text overlays, supporting split-screen comparisons, gradient backgrounds, and card layouts with Pollinations.ai base images and PIL typography.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-focused agents use this skill to generate publication-ready Xiaohongshu or RED post cover images with Chinese titles, subtitles, labels, and optional AI-generated base art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Base-image prompts are sent to Pollinations.ai, which may expose private or proprietary text included in --base-prompt.

Mitigation: Avoid private or proprietary content in --base-prompt and review prompts before execution.

Risk: The skill downloads a CJK font from GitHub and contacts external services during normal image generation.

Mitigation: Install and run only in environments where these network calls are acceptable, and prefer a normal user context rather than elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huuuwnnn-droid/skills/xhs-cover-gen)
- [Noto Sans CJK Simplified Chinese Bold font](https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf)
- [Pollinations.ai image prompt endpoint](https://image.pollinations.ai/prompt/)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated JPEG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default image size is 1080x1440 at 95% JPEG quality; supports split, gradient, and card styles.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
