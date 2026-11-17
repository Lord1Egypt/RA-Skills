## Description:

One-stop multi-platform video publishing workflow. From video clipping to multi-platform publishing, full process automation. Supports automatic clipping for platform formats, intelligent title optimization, tag recommendation, best publish time recommendation, one-click publishing to WeChat, Bilibili, Xiaohongshu, Douyin, YouTube, TikTok and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earthwalking](https://clawhub.ai/user/earthwalking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams can use this skill to plan and run a local workflow for adapting video files to platform-specific formats, generating titles and tags, and reviewing simulated publish status across WeChat, Bilibili, Xiaohongshu, Douyin, YouTube, and TikTok.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release materially overstates real publishing, analytics, and automation capabilities.

Mitigation: Treat the skill as a local video transcoding and publishing simulation tool, and do not rely on it for actual uploads or analytics.

Risk: Users may assume the workflow is safe for real platform credentials.

Mitigation: Do not provide platform credentials unless a future version clearly documents authenticated APIs, per-platform consent, and data-sharing behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earthwalking/skills/video-multi-publish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python examples; runtime output includes local video files and console status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local ffmpeg and ffprobe commands for video inspection and clipping; publishing and analytics behavior should be treated as simulated unless future evidence documents authenticated platform integrations.]

## Skill Version(s):

1.0.0 (source: release metadata, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
