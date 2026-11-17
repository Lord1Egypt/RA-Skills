## Description:

Create, produce, and publish UGC-style short-form video reels by sourcing DanSUGC reaction hooks, analyzing demos with Gemini, assembling videos with FFmpeg, publishing to TikTok and Instagram, and tracking performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielhangan](https://clawhub.ai/user/danielhangan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use ReelClaw to generate short-form UGC reel concepts, produce 1080x1920 videos, score virality, and publish or schedule them to connected TikTok or Instagram accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent system changes through package installation or font download steps.

Mitigation: Require explicit human approval before installing packages, running sudo, downloading fonts, or changing user font directories.

Risk: The skill can upload local video files to Gemini, DanSUGC, and a public temporary file host.

Mitigation: Use non-sensitive demo footage where possible and require approval before any media upload or public URL creation.

Risk: The skill can spend DanSUGC credits when purchasing clips or using analytics.

Mitigation: Check balances and require explicit approval before credit-spending purchase or analytics actions.

Risk: The skill can publish, schedule, update, or delete posts on real TikTok and Instagram accounts.

Mitigation: Use test social accounts where possible and require approval before publish, schedule, update, or delete operations.

Risk: The workflow depends on API keys for Gemini and DanSUGC.

Mitigation: Use restricted keys, avoid printing full secrets, and redact credentials in logs and generated output.

## Reference(s):

- [ReelClaw Source Homepage](https://github.com/dansugc/reelclaw)
- [ReelClaw ClawHub Listing](https://clawhub.ai/danielhangan/skills/reelclaw-dansugc)
- [DanSUGC LLM-Friendly API Docs](https://dansugc.com/llms.txt)
- [DanSUGC Interactive Docs](https://dansugc.com/docs)
- [ReelClaw README](artifact/README.md)
- [Tool Setup Guide](artifact/tools-setup.md)
- [Green Zone Reference](artifact/green-zone.md)
- [FFmpeg Patterns](artifact/ffmpeg-patterns.md)
- [Virality Rules and Best Practices](artifact/virality.md)
- [Virality Scoring](artifact/virality-scoring.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, MCP tool calls, JSON scoring outputs, captions, and generated video file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local MP4 reel files, public media URLs, scheduled social posts, analytics summaries, and ranked virality scorecards.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
