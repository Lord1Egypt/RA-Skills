## Description:

Starts a persistent macOS voice assistant that captures speech, sends it to SenseAudio ASR, routes the recognized text to the audioclaw agent, and reads responses with SenseAudio TTS or macOS say.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced macOS users use this skill to run a hands-free AudioClaw/OpenClaw voice assistant for local desktop conversations, voice control, and prototyping with SenseAudio ASR/TTS. It is intended for environments where long-running microphone capture and third-party speech APIs are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a long-lived macOS microphone workflow.

Mitigation: Deploy only where continuous microphone capture is acceptable, make wake/sleep and stop behavior clear to users, and stop the process when it is not in use.

Risk: Captured speech and recognized text are sent to SenseAudio services.

Mitigation: Review SenseAudio data handling before deployment, avoid sensitive speech unless approved, and protect the SENSEAUDIO_API_KEY credential.

Risk: The skill stores local state and can store voice preferences, runtime state, credentials, and optional voiceprint data under ~/.audioclaw.

Mitigation: Restrict file permissions on the local state directory, protect or rotate stored API keys, and delete voiceprint samples that are no longer needed.

Risk: The optional WeSpeaker service was flagged as not well constrained.

Mitigation: Avoid enabling WeSpeaker until the local service is hardened with authentication, loopback-only binding, path validation, and pinned dependencies.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/kikidouloveme79/skills/senseaudio-let-claw-talk)
- [Runtime Tuning](artifact/references/runtime_tuning.md)
- [WeSpeaker User Environment Guide](artifact/references/wespeaker_user_setup.md)
- [WeSpeaker Repository](https://github.com/wenet-e2e/wespeaker.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and runtime configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch a long-running macOS microphone process and optional local WeSpeaker voiceprint service.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
