## Description:

Text-to-Speech via macOS say command with Siri Natural Voices. Use for generating speech audio, TTS clips, or speaking text aloud on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobihagemann](https://clawhub.ai/user/tobihagemann)

### License/Terms of Use:


## Use Case:

Developers and content creators use this skill on macOS to generate spoken audio, preview text aloud, and create AIFF or converted WAV/MP3 text-to-speech clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Siri language-switch examples change a persistent macOS speech preference.

Mitigation: Record the current speech language before using defaults write, restore it after batch generation, and prefer say -v for non-Siri voices when suitable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobihagemann/skills/say)
- [Publisher profile](https://clawhub.ai/user/tobihagemann)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance may produce macOS say invocations and ffmpeg conversion commands for generated audio files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
