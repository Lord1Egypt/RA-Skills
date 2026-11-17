## Description:

Multilingual Text-to-Speech (TTS) with intelligent Pinyin-to-Hanzi conversion for text that mixes Vietnamese, Chinese or Pinyin, and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaskies](https://clawhub.ai/user/jaskies)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare multilingual text segments, select suitable Vietnamese, Chinese, and English voices, and generate a merged MP3 narration file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text may be sent through the TTS provider data flow.

Mitigation: Avoid confidential, regulated, or sensitive text unless that provider data flow is acceptable.

Risk: The requested output path can overwrite an existing MP3 file.

Mitigation: Choose a unique workspace output path before generating audio.

Risk: Audio generation depends on edge-tts and ffmpeg being available in the runtime environment.

Mitigation: Confirm those dependencies are installed before relying on the skill for delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaskies/skills/smart-speak-vutran)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Audio files]

**Output Format:** [JSON segment list and shell command that produce an MP3 audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires edge-tts and ffmpeg; writes the generated audio to a workspace MP3 path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
