## Description:

Upscale an existing HTTPS video via WeryAI (video-upscaler). Use when the user wants higher resolution output, not text-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to upscale an existing public HTTPS video through WeryAI, choosing 1080p, 2k, or 4k output. It is scoped to upscaling only and does not generate new videos from text or images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends public HTTPS video URLs to WeryAI and may incur paid API usage.

Mitigation: Use dry-run first, confirm the video URL and any non-default resolution before submit or wait, and install only when WeryAI processing and paid usage are acceptable.

Risk: Passing undocumented fields or relying on unrelated sibling scripts can broaden behavior beyond the reviewed upscaler workflow.

Mitigation: Use only scripts/video_upscaler.js with video_url and optional resolution, and keep only WERYAI_API_KEY in the runtime environment.

## Reference(s):

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-upscaler)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final video URLs are shared as Markdown links when a WeryAI task completes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
