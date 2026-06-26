## Description: <br>
Provides a unified JavaScript pipeline for image understanding, OCR, speech recognition, and text-to-speech synthesis using OpenAI-compatible APIs, Tesseract.js, local Whisper, and Edge TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add multimodal input and output handling to agents, including image descriptions, OCR extraction, speech-to-text transcription, and synthesized speech responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images or audio may be sent to configured OpenAI-compatible services when API mode is used. <br>
Mitigation: Use local speech/OCR modes for sensitive content when possible, disclose external processing to users, and keep API keys scoped and rotated. <br>
Risk: Generated speech files, temporary audio, or SSML text may contain confidential content in the configured output directory. <br>
Mitigation: Use private per-run output directories, avoid shared locations for sensitive content, and clean temporary files after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-multimodal-base) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Package manifest](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown documentation with JavaScript and shell examples; runtime APIs return JavaScript objects and generated audio file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call OpenAI-compatible services, local Whisper, Tesseract.js, and edge-tts; text-to-speech writes audio files to the configured output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
