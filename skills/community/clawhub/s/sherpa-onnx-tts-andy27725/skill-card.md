## Description:

Local text-to-speech via sherpa-onnx (offline, no cloud).

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure and run local, offline text-to-speech generation with sherpa-onnx, producing speech audio files from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads native sherpa-onnx runtime archives without declared checksum verification.

Mitigation: Verify upstream release provenance before installation or run the tool in a constrained environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andy27725/skills/sherpa-onnx-tts-andy27725)
- [sherpa-onnx runtime for macOS](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-osx-universal2-shared.tar.bz2)
- [sherpa-onnx runtime for Linux x64](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2)
- [sherpa-onnx runtime for Windows x64](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-win-x64-shared.tar.bz2)
- [Piper en_US lessac high TTS model](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance targets local audio generation and environment setup for sherpa-onnx.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
