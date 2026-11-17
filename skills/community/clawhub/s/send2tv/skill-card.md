## Description:

Send2tv helps agents push text messages, images, audio, or TTS playback to Huawei Smart Screen and other DLNA-compatible TVs over DLNA/UPnP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanshen-lec](https://clawhub.ai/user/seanshen-lec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to have an agent cast text, images, audio, or TTS messages from a local machine to a configured DLNA-compatible TV on the same network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill serves pushed media over the local network while casting.

Mitigation: Use it only on trusted networks and avoid sending sensitive text, images, or audio.

Risk: The skill can terminate whatever process is already using port 8082.

Mitigation: Review active services before running it, especially on shared machines or systems with critical local services.

Risk: TTS mode depends on a separately installed edge-tts converter.

Mitigation: Use TTS mode only after reviewing and trusting the separately installed converter.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seanshen-lec/skills/send2tv)
- [Microsoft Speech Voice Gallery](https://speech.microsoft.com/portal/voicegallery)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare temporary image or audio files and keep a local HTTP server running briefly while casting media.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
