## Description:

Creates AI-narrated short videos from existing clips and scripts through a two-phase workflow that generates narration and subtitle review materials before assembling the final FFmpeg-rendered video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content teams use this skill to turn existing video clips and narration scripts into social-media-ready short videos with AI voiceover, burned subtitles, transitions, and human review checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary states that unsafe config and FFmpeg handling can run unintended local commands.

Mitigation: Review config.py before execution, allow only trusted paths and segment names, and run the scripts in an isolated project environment.

Risk: Narration text is sent through edge-tts for speech generation.

Mitigation: Avoid sending sensitive or unpublished narration text unless the user accepts that external TTS data flow.

Risk: Unpinned Python and media-processing dependencies can change behavior over time.

Mitigation: Pin dependencies where possible and verify FFmpeg and edge-tts versions before production use.

## Reference(s):

- [FFmpeg Downloads](https://ffmpeg.org/download.html)
- [Configuration Example](references/config-example.py)
- [FFmpeg on Windows: Pitfalls & Solutions](references/ffmpeg-pitfalls.md)
- [ClawHub Skill Page](https://clawhub.ai/jessy-huang/skills/video-short-creator)
- [Publisher Profile](https://clawhub.ai/user/jessy-huang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python configuration, shell commands, review files, subtitle files, audio files, and rendered video outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a subtitle review sheet before final assembly and final MP4 output after explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
