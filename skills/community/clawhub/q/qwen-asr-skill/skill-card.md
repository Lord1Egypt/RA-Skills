## Description:

Provides CPU-based speech-to-text conversion for audio messages using Qwen3-ASR-0.6B, with automatic language detection for Chinese dialects and multiple languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yszheda](https://clawhub.ai/user/yszheda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to transcribe uploaded or webhook-delivered audio into text, with optional language or dialect hints for Chinese dialects and other supported languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network endpoints and webhook audio inputs may be exposed without adequate access controls.

Mitigation: Run behind trusted local access or add authentication and signature checks before deployment.

Risk: The artifact exposes forced-alignment behavior even though the minimal-edition documentation says forced alignment is absent.

Mitigation: Remove or explicitly gate the alignment endpoint and timestamp/alignment paths if releasing the minimal edition.

Risk: Dependency and model version ranges can change behavior across installations.

Mitigation: Pin Node, Python, and model revisions before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yszheda/skills/qwen-asr-skill)
- [Qwen3-ASR-0.6B model identifier](Qwen/Qwen3-ASR-0.6B)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and Markdown/chat guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recognized text, detected language, confidence, duration, and optional timestamp or alignment data when enabled.]

## Skill Version(s):

1.3.0 (source: server release metadata, package.json, OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
