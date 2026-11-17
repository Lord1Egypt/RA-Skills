## Description:

Local text-to-speech via sherpa-onnx (offline, no cloud).

This skill is ready for commercial/non-commercial use.

## Publisher:

[deichmann181](https://clawhub.ai/user/deichmann181)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure and run offline local text-to-speech with sherpa-onnx, including platform-specific runtime setup and model path configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation downloads native sherpa-onnx runtime archives from GitHub.

Mitigation: Install only when the listed GitHub release is acceptable for the deployment environment and run the skill as a normal user.

Risk: A text-to-speech output filename may overwrite an existing local file.

Mitigation: Choose a new output path or confirm the existing file can be replaced before running synthesis.

Risk: Incorrect runtime or model paths can cause local synthesis to fail.

Mitigation: Set SHERPA_ONNX_RUNTIME_DIR and SHERPA_ONNX_MODEL_DIR to the installed runtime and model directories before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deichmann181/skills/sherpa-onnx-tts-local)
- [sherpa-onnx runtime for macOS](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-osx-universal2-shared.tar.bz2)
- [sherpa-onnx runtime for Linux x64](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2)
- [sherpa-onnx runtime for Windows x64](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-win-x64-shared.tar.bz2)
- [Piper en_US Lessac high model archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON5 configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can synthesize local WAV audio through installed sherpa-onnx binaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
