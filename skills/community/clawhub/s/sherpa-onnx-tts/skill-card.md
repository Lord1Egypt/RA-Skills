## Description: <br>
Local text-to-speech via sherpa-onnx (offline, no cloud). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure and run offline local text-to-speech with sherpa-onnx, producing local audio from text without relying on a cloud service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on referenced sherpa-onnx runtime archives and a model download. <br>
Mitigation: Install only if you trust those downloads and apply your organization's normal archive verification process. <br>
Risk: The reviewed artifact mentions a wrapper, but only SKILL.md was present in the evidence bundle. <br>
Mitigation: Inspect any wrapper file before adding it to PATH or running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielsinewe/sherpa-onnx-tts) <br>
- [sherpa-onnx runtime for macOS](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-osx-universal2-shared.tar.bz2) <br>
- [sherpa-onnx runtime for Linux x64](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2) <br>
- [sherpa-onnx runtime for Windows x64](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-win-x64-shared.tar.bz2) <br>
- [Piper en_US lessac high TTS model](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local WAV audio files when the wrapper command is run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
