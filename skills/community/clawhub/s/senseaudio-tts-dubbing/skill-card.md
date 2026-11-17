## Description:

Generates SenseAudio text-to-speech dubbing from user-provided copy for marketing, short-video narration, product introductions, and related content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klilyz](https://clawhub.ai/user/klilyz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to turn approved scripts, product copy, and short-video narration into SenseAudio-generated voiceover files with configurable voice, speed, pitch, volume, and output format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is sent to the SenseAudio remote service for speech synthesis.

Mitigation: Use the skill only for text approved for external processing, and do not submit sensitive or regulated content unless SenseAudio handling is acceptable.

Risk: The SenseAudio API key is required for operation.

Mitigation: Store SENSEAUDIO_API_KEY in the environment, avoid sharing shell logs that expose it, and rotate the key if exposure is suspected.

Risk: SENSEAUDIO_API_BASE can redirect requests if it is set to an unexpected endpoint.

Mitigation: Leave SENSEAUDIO_API_BASE unset or pin it to https://api.senseaudio.cn before running synthesis.

Risk: The script may install the requests package at runtime if it is missing.

Mitigation: Run in an isolated Python environment and preinstall dependencies through normal environment management rather than relying on automatic pip installation.

## Reference(s):

- [SenseAudio documentation](https://senseaudio.cn/docs)
- [ClawHub skill page](https://clawhub.ai/klilyz/skills/senseaudio-tts-dubbing)
- [ClawHub publisher profile](https://clawhub.ai/user/klilyz)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated audio files may be mp3, wav, pcm, or flac when the bundled script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY; optional SENSEAUDIO_API_BASE defaults to https://api.senseaudio.cn; metadata JSON is saved only when explicitly requested.]

## Skill Version(s):

1.0.1 (source: server release evidence, created 2026-06-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
