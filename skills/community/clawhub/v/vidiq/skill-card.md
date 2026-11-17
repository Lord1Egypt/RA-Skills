## Description:

AI-powered video intelligence for downloading, analyzing, clipping, and creating GIFs from URLs or local video files using ffmpeg and yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassh100k](https://clawhub.ai/user/cassh100k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use VidIQ to inspect videos, download supported URL sources, extract frames, audio, clips, GIFs, and mosaics, and prepare frames for vision-model analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provided security evidence reports input-validation and temporary-file safety issues that could expose files or run unintended commands.

Mitigation: Use trusted arguments and non-sensitive media, review commands before execution, validate numeric inputs, and use a private permission-restricted cache with clear cleanup behavior.

Risk: The artifact script downloads external video URLs and processes local media with ffmpeg and yt-dlp.

Mitigation: Use trusted URLs and media sources, keep ffmpeg and yt-dlp patched, and avoid running the skill against sensitive or untrusted files without sandboxing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cassh100k/skills/vidiq)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, textual video metadata, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and yt-dlp; generated media is written under /tmp/vidiq/ by the artifact script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
