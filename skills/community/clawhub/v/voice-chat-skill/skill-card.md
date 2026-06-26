## Description: <br>
Voice Chat Skill helps an agent set up bidirectional voice conversations with speech-to-text input, text-to-speech output, and conversation flow management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangkelvin](https://clawhub.ai/user/fangkelvin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to add voice input, speech recognition, text-to-speech responses, and voice-chat testing workflows to an OpenClaw-based assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microphone audio, transcripts, or generated responses may be sent to Google, ElevenLabs, or another configured speech provider. <br>
Mitigation: Use local or offline modes for sensitive conversations, review provider settings before use, and avoid entering confidential speech when cloud providers are enabled. <br>
Risk: Console transcripts and generated audio files may expose sensitive conversation content. <br>
Mitigation: Treat logs and generated audio as sensitive data, limit retention, and review output locations before sharing or deploying the skill. <br>
Risk: The documentation includes a shell-based playback sample. <br>
Mitigation: Prefer safer platform playback APIs or review any shell invocation before copying it into production code. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fangkelvin/voice-chat-skill) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw TTS documentation](https://docs.openclaw.ai/tools/tts) <br>
- [SpeechRecognition package](https://pypi.org/project/SpeechRecognition/) <br>
- [PyAudio documentation](https://people.csail.mit.edu/hubert/pyaudio/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and microphone access; optional cloud STT or TTS providers may process audio, transcripts, or generated responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
