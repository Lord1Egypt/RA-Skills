## Description: <br>
VoiceClaw lets OpenClaw agents transcribe inbound audio with local Whisper and generate spoken replies with local Piper TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asif2BD](https://clawhub.ai/user/Asif2BD) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use VoiceClaw to add local speech-to-text and text-to-speech behavior to OpenClaw agents. It is intended for voice messages, audio attachments, spoken replies, and workflows where text responses should also be synthesized as audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive recordings could be exposed if the local environment or installed voice tooling is not actually operating offline. <br>
Mitigation: Confirm the installed scripts and required binaries remain local-only before processing sensitive audio. <br>
Risk: Missing or misconfigured local binaries or model files can prevent transcription or speech synthesis. <br>
Mitigation: Verify whisper, piper, ffmpeg, WHISPER_MODEL, and VOICECLAW_VOICES_DIR before deployment. <br>


## Reference(s): <br>
- [VoiceClaw ClawHub Page](https://clawhub.ai/Asif2BD/voiceclaw) <br>
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp) <br>
- [Piper TTS](https://github.com/rhasspy/piper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Audio files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text transcript, WAV audio path, and Markdown guidance with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local whisper, piper, ffmpeg, Whisper model files, and Piper voice models.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
