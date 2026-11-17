## Description:

Converts role-tagged story or script text into a multi-role audiobook by analyzing characters, matching voices from an editable library, synthesizing each segment with SenseAudio TTS, and returning a media reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinhao-96](https://clawhub.ai/user/xinhao-96)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and content creators use this skill to turn `[role]text` story, novel, or dialogue passages into multi-character narrated audio for OpenClaw or Feishu consumption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story text and the SenseAudio API key may be sent to the configured TTS endpoint.

Mitigation: Use only a trusted SenseAudio API base, avoid untrusted SENSEAUDIO_API_BASE or --api-base values, and do not process sensitive story text unless that transfer is approved.

Risk: The skill can automatically install Python packages during invocation.

Mitigation: Preinstall and review dependencies in a controlled environment before running the skill so runtime package installation is unnecessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinhao-96/skills/story-audio-adapter)
- [Role analysis prompt](artifact/references/role_analysis_prompt.md)
- [Voice library](artifact/references/voice_library.json)
- [SenseAudio API base](https://api.senseaudio.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, files, media reference]

**Output Format:** [Markdown or plain text with JSON payloads, local WAV or MP3 audio files, and a `MEDIA:./...` reference]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY; writes role analysis, voice mapping, segment manifest, synthesized audio segments, and final audio output.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
