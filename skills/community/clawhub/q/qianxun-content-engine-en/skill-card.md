## Description:

Content Engine helps agents deconstruct Xiaohongshu posts into structured cards and generate brand-adapted scripts, captions, covers, descriptions, tags, reference frames, and optional Seedance video outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and marketing teams use this skill to study Xiaohongshu content patterns, maintain a reusable content graph, and generate adapted campaign assets from a reference post and brand context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key handling can expose an OpenRouter key to the wrong provider when generation is run with only OPENROUTER_API_KEY configured.

Mitigation: Use a dedicated OFOX_API_KEY, avoid relying on OPENROUTER_API_KEY with this version, and rotate the OpenRouter key if generation was already run with only that key configured.

Risk: Project-level environment files and overridden base URLs can increase credential exposure or route requests unexpectedly.

Mitigation: Keep API keys out of project-level .env files where possible, and verify OFOX_BASE_URL and ARK_BASE_URL before use.

Risk: Real Seedance video generation can trigger paid network actions.

Mitigation: Use --no-real-video for prompt-only runs, or avoid --no-confirm unless paid Seedance calls are explicitly acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dizhu/skills/qianxun-content-engine-en)
- [Output template](references/output-template.md)
- [Example image output](references/example-image.md)
- [Example video output](references/example-video.md)
- [TikHub API](https://tikhub.io)
- [Ofox](https://ofox.ai)
- [Volcengine Ark API key console](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)
- [OpenRouter](https://openrouter.ai)
- [Ronin Skill Graph inspiration](https://x.com/DeRonin_/status/2042604279077237170)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text files with optional generated image or video assets and local workspace paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation can invoke metered external APIs; video mode may create per-shot MP4 files and an ffmpeg-concatenated final video.]

## Skill Version(s):

0.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
