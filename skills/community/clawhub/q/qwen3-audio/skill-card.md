## Description:

High-performance audio library for Apple Silicon with text-to-speech (TTS) and speech-to-text (STT).

This skill is ready for commercial/non-commercial use.

## Publisher:

[darknoah](https://clawhub.ai/user/darknoah)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill on Apple Silicon Macs to run local Qwen3 audio workflows, including text-to-speech, speech-to-text, voice cloning, style-controlled voice generation, and reusable voice profile management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install unpinned code at runtime.

Mitigation: Use a pre-provisioned, locked dependency environment before running the skill.

Risk: The skill uses a third-party Hugging Face mirror by default.

Mitigation: Opt out of the mirror unless it is explicitly trusted, and prefer a reviewed model endpoint.

Risk: Custom voice IDs can create unsafe voice-profile paths.

Mitigation: Use only trusted voice IDs without path components and review stored profile paths before use.

Risk: Created voice profiles retain reference audio, transcript text, and style descriptions.

Mitigation: Treat voice profiles as sensitive data, restrict access to the skill directory, and remove profiles when they are no longer needed.

## Reference(s):

- [Qwen3 Audio skill page](https://clawhub.ai/darknoah/skills/qwen3-audio)
- [Environment checklist](references/env-check-list.md)
- [Hugging Face](https://huggingface.co)
- [Hugging Face mirror](https://hf-mirror.com)
- [Qwen3 ASR sample audio](https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; runtime commands return JSON and audio, transcript, or subtitle files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice profiles may persist reference audio, transcript text, and voice style descriptions under the skill's voices directory.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
