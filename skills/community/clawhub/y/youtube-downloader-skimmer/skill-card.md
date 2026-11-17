## Description:

Downloads YouTube videos and automatically extracts key clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bg1avd](https://clawhub.ai/user/bg1avd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to download public YouTube videos, split them into chapter-based or custom clips, and generate MP4 or MP3 outputs for delivery through QQ or Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated media may be sent to QQ or Telegram by default without a clearly scoped opt-in.

Mitigation: Disable external delivery by default, use the none destination during review, and require explicit user confirmation before sending files to any platform.

Risk: The raw downloaded video may be deleted by default after clipping.

Mitigation: Make raw-file deletion explicit opt-in and retain source files until the user verifies the generated clips.

Risk: Media tooling dependencies may change behavior across versions.

Mitigation: Pin and review yt-dlp and ffmpeg versions before deployment.

Risk: Video titles or chapter names may produce unsafe or confusing output filenames.

Mitigation: Sanitize generated filenames before writing media files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bg1avd/skills/youtube-downloader-skimmer)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [MP4 or MP3 media files with console text listing generated clip paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written under the configured output directory, defaulting to /tmp/openclaw/.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
