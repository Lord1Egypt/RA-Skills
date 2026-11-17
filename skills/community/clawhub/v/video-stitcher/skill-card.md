## Description:

Video Stitcher helps agents combine video clips into a complete video with transitions, background music, subtitles, and export settings using FFmpeg or Remotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliviapp8](https://clawhub.ai/user/oliviapp8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and media automation agents use this skill to turn a list of video clips into a finished video with optional transitions, music, subtitles, and platform-specific export settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may generate commands that read local video, subtitle, music paths, or media URLs supplied by the user.

Mitigation: Use trusted media inputs and review generated FFmpeg or Remotion commands before running them on sensitive files.

Risk: Generated video-processing commands may overwrite outputs or produce unintended edits if paths, timing, resolution, or transition settings are wrong.

Mitigation: Run on copies or preview outputs first, and verify paths and render settings before executing long or destructive workflows.

## Reference(s):

- [Video Stitcher ClawHub Skill Page](https://clawhub.ai/oliviapp8/skills/video-stitcher)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with YAML examples and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose FFmpeg commands or Remotion project guidance for producing video files from user-provided media.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
