## Description: <br>
Local TTS router for Apple Silicon that helps agents pull models, serve OpenAI-compatible APIs, synthesize speech, and clone voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hrhrng](https://clawhub.ai/user/hrhrng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators on macOS with Apple Silicon use this skill to install and operate tts-router, pull local TTS models, serve OpenAI-compatible APIs, synthesize speech, and perform consented voice-cloning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice-cloning workflows can use arbitrary online media or uploaded audio without built-in consent checks. <br>
Mitigation: Use only reference audio from speakers who explicitly permitted cloning; avoid public videos, podcasts, or links unless you have rights to that audio; disclose generated speech as synthetic. <br>
Risk: The skill can start a local server with speech-generation, reference-upload, and reference-fetch endpoints. <br>
Mitigation: Keep the server local or restricted to trusted networks, review requests before execution, and avoid processing sensitive audio unless authorized. <br>
Risk: The workflow installs an external tts-router package and downloads model weights from HuggingFace Hub. <br>
Mitigation: Install only when you trust the package and selected models, review model sources before use, and keep model serving local unless a deployment review approves broader exposure. <br>


## Reference(s): <br>
- [Tts Router ClawHub release](https://clawhub.ai/hrhrng/tts-router) <br>
- [OpenClaw Integration](references/openclaw.md) <br>
- [Voice Cloning - Advanced Guide](references/voice-cloning.md) <br>
- [OpenClaw TTS configuration docs](https://docs.openclaw.ai/gateway/configuration-reference#tts-text-to-speech) <br>
- [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local audio files or local API requests when the user executes the suggested commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
