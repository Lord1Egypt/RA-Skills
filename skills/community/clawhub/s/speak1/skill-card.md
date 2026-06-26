## Description: <br>
Text-to-speech using Kokoro local TTS. Use when the user wants to convert text to audio, read aloud, or generate speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[babysor](https://clawhub.ai/user/babysor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users use this skill to run local text-to-speech with Kokoro TTS, including converting text, EPUB, and PDF inputs to audio, selecting voices, blending voices, adjusting speed, and streaming playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a third-party Kokoro TTS CLI and model files downloaded from GitHub. <br>
Mitigation: Install and use the CLI only after reviewing the third-party project and verifying the downloaded model and voices files are acceptable for the deployment environment. <br>
Risk: Generated audio from private documents can contain sensitive local output. <br>
Mitigation: Store, share, retain, or delete generated audio according to the sensitivity of the source documents. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/babysor/speak1) <br>
- [Kokoro TTS Project](https://github.com/nazdridoy/kokoro-tts) <br>
- [Kokoro v1.0 ONNX Model](https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/kokoro-v1.0.onnx) <br>
- [Kokoro v1.0 Voices File](https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/voices-v1.0.bin) <br>
- [Kokoro TTS Reference](reference.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers local CLI installation, model download commands, voice and language options, and audio output choices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
