## Description:

Windows-first video localization pipeline for downloading, transcribing, translating, dubbing, and retiming YouTube or Bilibili videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bzxcup-afk](https://clawhub.ai/user/bzxcup-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video localization operators use this skill to turn YouTube or Bilibili source videos into dubbed localized videos with aligned subtitle files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release was flagged suspicious because channel rules can silently change opening translated speech for configured channels.

Mitigation: Review video_pipeline/data/channel_rules.json before use and disable intro override unless inserted narration is explicitly desired.

Risk: The pipeline has broad network behavior for downloading videos and using translation or TTS providers.

Mitigation: Install and run it in an isolated environment, pin dependencies where possible, and assume subtitle or TTS text may be sent to external providers.

Risk: Browser-cookie access may expose sensitive session material if used casually.

Mitigation: Avoid YTDLP_COOKIES_FILE unless it is necessary for a blocked download, and use a purpose-limited cookies file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bzxcup-afk/skills/video-dub)
- [Release bundle layout](references/release_bundle.md)
- [Troubleshooting](references/troubleshooting.md)
- [Pipeline README](video_pipeline/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell commands, configuration steps, and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying pipeline can produce MP4 video, SRT subtitle, JSON structured subtitle, audio, and debug files.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
