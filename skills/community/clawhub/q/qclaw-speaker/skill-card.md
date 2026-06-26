## Description: <br>
Qclaw Speaker provides Chinese text-to-speech playback for QClaw/OpenClaw using Edge TTS, sherpa-onnx Piper, and Windows SAPI fallback engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forhonourlx](https://clawhub.ai/user/forhonourlx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to make QClaw/OpenClaw read generated text aloud, choose Chinese voices, configure automatic speech playback, and fall back between online and offline TTS engines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can install Python packages and download TTS model archives. <br>
Mitigation: Run installation only in environments where package installation and model downloads are approved; prefer pinned dependencies and verified model archives for sensitive deployments. <br>
Risk: Using the Edge TTS engine may send text to Microsoft's online speech service. <br>
Mitigation: Use the sherpa-onnx or Windows SAPI engines for offline speech when spoken text may be sensitive. <br>
Risk: The bundled xiao_ya model card identifies non-commercial dataset licensing for its dataset source. <br>
Mitigation: Confirm model and dataset license compatibility before using the offline Piper model in commercial deployments. <br>


## Reference(s): <br>
- [Qclaw Speaker on ClawHub](https://clawhub.ai/forhonourlx/qclaw-speaker) <br>
- [sherpa-onnx Piper xiao_ya model archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-zh_CN-xiao_ya-medium-int8.tar.bz2) <br>
- [sherpa-onnx Piper chaowen model archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-zh_CN-chaowen-medium-int8.tar.bz2) <br>
- [sherpa-onnx Piper huayan model archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-zh_CN-huayan-medium.tar.bz2) <br>
- [xiao_ya model dataset](https://huggingface.co/openspeech/BZNSYP) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local MP3 or WAV audio files and update skill configuration for voice, speed, engine, and auto-speak settings.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
