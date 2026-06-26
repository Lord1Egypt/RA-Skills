## Description: <br>
Local text-to-speech via sherpa-onnx (offline, no cloud). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and run offline local text-to-speech with sherpa-onnx, producing speech audio files from text without a cloud service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads third-party sherpa-onnx runtime and model archives before use. <br>
Mitigation: Install only if you trust the referenced GitHub project, and verify downloaded archives when upstream checksums are available before adding the wrapper to PATH or running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy27725/sherpa-onnx-tts-andy27725) <br>
- [sherpa-onnx macOS runtime archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-osx-universal2-shared.tar.bz2) <br>
- [sherpa-onnx Linux x64 runtime archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2) <br>
- [sherpa-onnx Windows x64 runtime archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-win-x64-shared.tar.bz2) <br>
- [Piper en_US lessac high TTS model archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHERPA_ONNX_RUNTIME_DIR and SHERPA_ONNX_MODEL_DIR to point to local runtime and model directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
