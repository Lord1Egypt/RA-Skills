## Description:

Converts a recorded video or SRT transcript into editable video resources such as B-roll, overlays, web references, AI-generated pixel assets, tutorial UI captures, and a MANIFEST.md for assembly in an editor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and agents use this skill to collect real web resources, AI-generated pixel overlays, tutorial captures, and a keyword-based MANIFEST.md for a talking-head video. The skill prepares editing inputs only; it does not edit or render the final video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private videos, screenshots, or selfies may be exposed through web searches, Telegram delivery, or Higgsfield processing.

Mitigation: Review inputs before running the skill and use it only when the user is comfortable with those external processing and delivery paths.

Risk: Personal face photos may be uploaded to an external service for pixel-avatar generation.

Mitigation: Require explicit user confirmation before uploading any personal face photo.

Risk: The artifact contains conflicting generic and OpenClaw-specific instructions for TikTok downloads, frame processing, and delivery.

Mitigation: In OpenClaw, follow the header rules: do not download TikToks with yt-dlp, do not use ffmpeg for TikTok or frame processing, and deliver the zip through Telegram.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/recursos-de-video-formula100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown manifest plus organized asset files and concise user-facing delivery guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an entregables folder with IA, USER, and WEB assets, a MANIFEST.md, and a compressed zip delivered through Telegram when run in OpenClaw.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
