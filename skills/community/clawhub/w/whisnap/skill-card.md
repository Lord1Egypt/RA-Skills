## Description:

macOS CLI for transcribing audio and video files using local Whisper models or Whisnap Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neolio42](https://clawhub.ai/user/neolio42)

### License/Terms of Use:


## Use Case:

Developers, engineers, and other macOS users use this skill to run Whisnap CLI transcription workflows for audio or video files, including local Whisper transcription, optional cloud transcription, JSON output, model selection, and diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio or video files may contain sensitive content, and cloud transcription sends selected content to Whisnap Cloud.

Mitigation: Use local models for sensitive recordings, and use --cloud only when cloud transcription is acceptable for that content.

Risk: The skill depends on the local Whisnap macOS app, its CLI symlink, downloaded models, and app authentication for cloud mode.

Mitigation: Install and trust the Whisnap app, enable the CLI from app settings, download at least one model, and sign in before using cloud transcription.

Risk: Commands operate on user-supplied file paths and the CLI validates paths but does not search for missing files.

Mitigation: Confirm the target file path exists before running transcription commands.

## Reference(s):

- [Whisnap homepage](https://whisnap.com)
- [ClawHub skill listing](https://clawhub.ai/neolio42/skills/whisnap)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide use of Whisnap JSON output with timestamps, segments, model information, and processing time.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
