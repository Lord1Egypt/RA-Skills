## Description:

Create, produce, and schedule UGC-style short-form video reels at scale by sourcing UGC reaction hooks from DanSUGC, analyzing app demos with Gemini AI, assembling reels with ffmpeg, publishing via Post-Bridge, and tracking performance through DanSUGC's analytics proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjjohny228](https://clawhub.ai/user/jjjohny228)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use Reelclaw to plan and execute UGC-style short-form video campaigns, including hook sourcing, demo analysis, 15-second vertical reel assembly, social scheduling, and performance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload video content to public or third-party services.

Mitigation: Use only approved media, avoid confidential demos unless privacy handling is approved, and review destination services before upload.

Risk: The skill can purchase clips and act on connected social accounts.

Mitigation: Require explicit user approval before purchases, public uploads, scheduling, updates, or deletions.

Risk: The skill can change the host environment while checking or installing media tools and fonts.

Mitigation: Install ffmpeg and fonts manually from trusted sources and review setup commands before execution.

## Reference(s):

- [ReelClaw homepage](https://github.com/dansugc/reelclaw)
- [FFmpeg Patterns for ReelClaw](references/ffmpeg-patterns.md)
- [Green Zone Reference](references/green-zone.md)
- [Tool Setup Guide](references/tools-setup.md)
- [DanSUGC](https://dansugc.com)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, MCP call examples, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ffmpeg command recipes, captions, posting schedules, setup checks, and analytics summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
