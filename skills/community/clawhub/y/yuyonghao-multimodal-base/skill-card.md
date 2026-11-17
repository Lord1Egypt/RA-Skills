## Description:

Supports image understanding, OCR, speech-to-text, and text-to-speech synthesis with multi-voice output through a unified multimodal processing pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to add multimodal input and output handling to workflows that need image analysis, OCR, audio transcription, and synthesized speech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive images, recordings, transcripts, or API credentials may be sent to configured external endpoints.

Mitigation: Use only trusted API endpoints and keys, and avoid processing private media unless third-party transmission is acceptable.

Risk: Under-scoped file handling can delete unrelated files when cleanup is invoked on a shared output directory.

Mitigation: Keep outputDir dedicated to generated audio and avoid cleanup on shared directories.

Risk: Dependency and model download integrity controls may need additional review before production use.

Mitigation: Review and update dependency and model download integrity controls before installing in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-multimodal-base)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, configuration snippets, structured result objects, and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image and audio processing may rely on configured external APIs, local OCR, Whisper, Edge TTS, and filesystem paths supplied by the user.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
