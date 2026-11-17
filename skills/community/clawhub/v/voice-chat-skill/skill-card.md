## Description:

Provides bidirectional voice chat integration with speech-to-text and text-to-speech for OpenClaw-based agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangkelvin](https://clawhub.ai/user/fangkelvin)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add microphone-driven speech recognition, spoken responses, and voice conversation flows to OpenClaw-based agents. It supports local simulation as well as optional online speech services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Microphone audio or generated text may be sent to third-party speech services.

Mitigation: Use the offline or simulated mode when cloud sharing is not acceptable, and obtain clear user consent before enabling online STT or TTS providers.

Risk: The artifact includes a shell=True TTS playback example.

Mitigation: Do not copy that pattern into production code; use explicit platform playback commands without shell expansion and validate file paths.

Risk: Unpinned speech and audio dependencies can change behavior across installs.

Mitigation: Install in a virtual environment with pinned dependency versions and avoid administrator-level package installs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fangkelvin/skills/voice-chat-skill)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw TTS Documentation](https://docs.openclaw.ai/tools/tts)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
- [ElevenLabs Text-to-Speech API](https://api.elevenlabs.io/v1/text-to-speech/{voice_id})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, setup commands, and configuration notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference microphone input, generated speech output, local simulation mode, and optional cloud speech services.]

## Skill Version(s):

1.0.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
