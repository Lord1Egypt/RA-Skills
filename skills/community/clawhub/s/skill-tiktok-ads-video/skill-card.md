## Description:

Generate TikTok-style short-form ad videos by overlaying animated captions on a base MP4 with built-in product presets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and developers use this skill to produce short-form product ad videos for TikTok, Reels, and YouTube Shorts from an existing MP4. It supports preset product scripts and caption styles for fast ad-video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python video-processing script that resolves third-party packages.

Mitigation: Use a locked dependency environment or sandbox before running it in sensitive environments.

Risk: The implementation is narrower than the README for background audio mixing and captions JSON handling.

Mitigation: Review the current script behavior and test the intended workflow before relying on those documented options.

Risk: Built-in ad copy includes UAE/AED-specific text.

Mitigation: Review and adjust product presets before using generated ads in other markets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-tiktok-ads-video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated video file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces a local MP4 output when its Python overlay script is run with a source video, product preset, and caption style.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
