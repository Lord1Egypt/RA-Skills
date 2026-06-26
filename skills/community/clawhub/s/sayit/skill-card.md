## Description: <br>
Text-to-speech using Kokoro local TTS. Use when the user wants to convert text to audio, read aloud, or generate speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[babysor](https://clawhub.ai/user/babysor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to convert chosen text, documents, or streams into local speech audio with Kokoro TTS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the third-party kokoro-tts CLI and downloaded model files. <br>
Mitigation: Install only if third-party CLI and model downloads are acceptable for the environment, and verify the package and GitHub release when supply-chain provenance matters. <br>
Risk: The skill can process local files selected by the user. <br>
Mitigation: Use it only on files intentionally chosen by the user and keep model files in a known location. <br>


## Reference(s): <br>
- [Kokoro TTS Reference](artifact/reference.txt) <br>
- [Kokoro TTS](https://github.com/nazdridoy/kokoro-tts) <br>
- [Kokoro model download](https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/kokoro-v1.0.onnx) <br>
- [Kokoro voices download](https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/voices-v1.0.bin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Kokoro TTS commands that read selected text or files and produce WAV or MP3 audio.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
