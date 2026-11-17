## Description:

VoiceClaw lets OpenClaw agents transcribe inbound audio with local Whisper and synthesize voice replies with local Piper TTS without cloud APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use VoiceClaw to add local speech-to-text and text-to-speech workflows to OpenClaw agents, especially when inbound voice messages should receive both an audio reply and a text transcript. The skill is intended for systems where Whisper, Piper, ffmpeg, and the required local model files are managed on the host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local model and binary setup can introduce supply-chain risk if dependencies are downloaded without verification.

Mitigation: Use trusted sources, pin versions, and verify checksums for Whisper, Piper, ffmpeg, and model files before deployment.

Risk: Temporary audio files may be exposed or collide on shared machines because runtime paths are written under /tmp.

Mitigation: Run the skill as an unprivileged user and update temporary file handling to use mktemp or a private runtime directory before shared-host use.

Risk: Speech models can mis-transcribe adversarial, noisy, or ambiguous audio and affect downstream agent responses.

Mitigation: Show the transcript in text replies and have the agent confirm important spoken instructions before acting on them.

## Reference(s):

- [ClawHub VoiceClaw Skill Page](https://clawhub.ai/asif2bd/skills/voiceclaw)
- [OpenClaw](https://openclaw.ai)
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [Piper TTS](https://github.com/rhasspy/piper)
- [Whisper ggml-base.en.bin Model](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands; runtime scripts produce transcript text and WAV file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local whisper, piper, ffmpeg, Whisper model, and Piper voice model files; no operational network calls are declared.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
