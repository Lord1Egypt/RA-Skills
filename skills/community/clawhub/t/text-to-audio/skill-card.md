## Description:

Converts Chinese or English text, including OCR-extracted image text, into natural-sounding MP3 speech using edge-tts and Microsoft Edge TTS voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenzje228](https://clawhub.ai/user/kenzje228)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn provided text or OCR-extracted image text into MP3 narration for lessons, essays, stories, articles, and batch audio generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for audio generation is sent to an online Microsoft TTS service.

Mitigation: Do not submit confidential, regulated, or private text unless cloud processing is acceptable for the user and organization.

Risk: The environment check can install edge-tts without a pinned version.

Mitigation: Run the skill in a virtual environment and install a pinned, reviewed edge-tts version before use.

Risk: Audio generation depends on network access to the Microsoft TTS service.

Mitigation: Confirm network access before relying on the skill, especially for batch generation workflows.

## Reference(s):

- [edge-tts voice catalog](artifact/references/voice_catalog.md)
- [Microsoft TTS service endpoint](https://speech.platform.bing.com)
- [ClawHub skill page](https://clawhub.ai/kenzje228/skills/text-to-audio)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [MP3 audio files, JSON batch configuration, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads UTF-8 text files, supports voice and speech-rate options, and can process multiple files from a batch JSON configuration.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
