## Description:

Replace video audio with TTS voice while preserving original timing, with optional subtitle generation from video using Whisper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synthere](https://clawhub.ai/user/synthere)

### License/Terms of Use:


## Use Case:

Developers and media automation users use this skill to generate subtitles from video, convert subtitle text into speech, and replace the video's original audio while preserving subtitle timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation and error messages encourage privileged package installation with sudo pip3 --break-system-packages.

Mitigation: Install dependencies in an isolated virtual environment with pinned package versions and avoid privileged package installation.

Risk: Subtitle text may be sent to third-party TTS services when using ElevenLabs or Edge TTS.

Mitigation: Use only subtitle text that is approved for those providers, and review provider privacy and retention terms before processing sensitive content.

Risk: The replacement workflow uses predictable temporary paths under /tmp.

Mitigation: Run the skill on a single-user or isolated machine and remove temporary files after processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/synthere/skills/video-audio-replace)
- [ElevenLabs Text-to-Speech API endpoint used by the skill](https://api.elevenlabs.io/v1/text-to-speech/{voice_id})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and Python-based workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installed scripts produce SRT subtitle files, generated TTS audio segments, and an MP4 video with replaced audio.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
