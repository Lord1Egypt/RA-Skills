## Description: <br>
Full voice message setup (STT + TTS) for OpenClaw using faster-whisper and Edge TTS <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aksenkin](https://clawhub.ai/user/aksenkin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to set up speech-to-text transcription for incoming voice messages and text-to-speech voice replies for supported conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice-reply text may be synthesized through Edge/Microsoft TTS, which can be inappropriate for sensitive conversations. <br>
Mitigation: Disable automatic TTS for sensitive use cases or use a local TTS provider when available. <br>
Risk: faster-whisper installs dependencies and downloads speech models locally, which can affect disk usage and runtime behavior. <br>
Mitigation: Review the install commands before execution and confirm that local package and model downloads are acceptable for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aksenkin/voice-stt-tts) <br>
- [OpenClaw audio docs](https://docs.openclaw.ai/nodes/audio) <br>
- [OpenClaw TTS docs](https://docs.openclaw.ai/tts) <br>
- [OpenClaw docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, Python, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install commands, a transcription helper script, OpenClaw configuration examples, restart steps, testing guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
