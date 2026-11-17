## Description:

Qclaw Speaker provides text-to-speech playback for QClaw/OpenClaw with Edge TTS, local Sherpa-ONNX Piper, and Windows SAPI fallback engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forhonourlx](https://clawhub.ai/user/forhonourlx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QClaw/OpenClaw users use this skill to convert assistant responses or supplied text into spoken Chinese audio with online and local fallback engines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe installation practices and unverified model downloads can affect the local Python environment.

Mitigation: Review the installer first, install in an isolated virtual environment, and verify downloaded model sources before use.

Risk: Cloud TTS can expose sensitive text to an online service.

Mitigation: Prefer the offline Sherpa-ONNX or Windows SAPI engines for confidential content.

Risk: Auto-speak can disclose responses in shared or confidential settings.

Mitigation: Keep auto-speak disabled unless the runtime environment is appropriate for audible output.

Risk: The runtime may mutate installed Python package files while applying the ONNX Runtime DLL fix.

Mitigation: Avoid administrator installs and validate the runtime package state before deploying beyond a disposable environment.

## Reference(s):

- [Qclaw Speaker ClawHub release](https://clawhub.ai/forhonourlx/skills/qclaw-speaker)
- [Bundled Xiao Ya model card](models/vits-piper-zh_CN-xiao_ya-medium-int8/MODEL_CARD)
- [Sherpa-ONNX Piper Xiao Ya model archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-zh_CN-xiao_ya-medium-int8.tar.bz2)
- [Sherpa-ONNX Piper Chinese model mirror](https://www.modelscope.cn/models/manyeyes/sherpa-onnx-piper-zh/resolve/master/vits-piper-zh_CN-xiao_ya-medium-int8.tar.bz2)
- [BZNSYP dataset](https://huggingface.co/openspeech/BZNSYP)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files]

**Output Format:** [CLI output, JSON status, and generated MP3 or WAV audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update local voice, speed, engine, and auto-speak settings in config.json.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
