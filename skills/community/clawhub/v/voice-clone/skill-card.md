## Description:

Guide users through SenseAudio platform voice cloning, then generate TTS with cloned voice_id values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use this skill to prepare SenseAudio voice cloning, manage cloned voice_id values, and synthesize text-to-speech audio with a cloned voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends selected text, voice_id values, and the SENSEAUDIO_API_KEY credential to SenseAudio for TTS.

Mitigation: Use the skill only for content approved for SenseAudio processing, keep SENSEAUDIO_API_KEY scoped to this service, and avoid logging or storing credentials.

Risk: The skill depends on Python packages that are not version-pinned in the release evidence.

Mitigation: Install dependencies in a locked or otherwise controlled environment before production use.

Risk: Voice cloning and cloned-voice synthesis can be misused if voice samples or voice_id values are handled without consent.

Mitigation: Use only authorized voice samples and treat voice_id values as user-specific operational identifiers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/voice-clone)
- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key Page](https://senseaudio.cn/platform/api-key)
- [SenseAudio Voice Clone Page](https://senseaudio.cn/platform/voice-clone)
- [SenseAudio TTS API Endpoint](https://api.senseaudio.cn/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with Python helper code and optional JSON-style validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MP3, WAV, PCM, or FLAC audio through the SenseAudio TTS API when the agent executes the generated helper workflow with user credentials.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
