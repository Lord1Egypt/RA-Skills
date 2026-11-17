## Description:

Multi-language video subtitle translation and automatic dubbing skill that can produce translated subtitle files and muxed multi-track video outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbjincheng](https://clawhub.ai/user/zbjincheng)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and content localization teams use this skill to translate source-video subtitles and optionally synthesize target-language dubbing for multilingual video delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subtitle text, generated speech text, and bearer credentials can be sent to user-supplied translation or TTS endpoints.

Mitigation: Use HTTPS endpoints you control or trust, review provider retention and privacy terms before processing confidential videos, and use limited-scope credentials.

Risk: Translation and dubbing behavior depends on configured external providers and local media tools.

Mitigation: Review translation, TTS, ffmpeg, and ffprobe configuration before running the skill in a production workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zbjincheng/skills/video-subtitle-translation-dubbing)
- [Project homepage](https://github.com/zbjincheng/openclaw-skill-videotranslate)
- [OpenClaw framework](https://github.com/OpenClaw)

## Skill Output:

**Output Type(s):** [Files, Text, Configuration]

**Output Format:** [Path strings to a muxed MKV video file and a UTF-8 SRT/VTT subtitle file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source and target subtitle tracks, source audio, and optional target-language dubbing; requires ffmpeg and ffprobe.]

## Skill Version(s):

0.1.4 (source: skill.md frontmatter, manifest.yaml, pyproject.toml, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
