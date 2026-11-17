## Description:

Local OpenVINO Qwen3-TTS skill for OpenClaw QQBOT workflows that supports voice cloning from short reference audio and styled text-to-speech generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aurora2035](https://clawhub.ai/user/aurora2035)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw QQBOT operators use this skill to install and run local TTS services for voice cloning and styled speech generation while keeping TTS separate from ASR/STT workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes local TTS and workflow services, including an unauthenticated Node gateway that can be powerful if reachable from a network.

Mitigation: Run only on a trusted local machine, firewall port 9002, and consider changing the gateway to bind to 127.0.0.1 before use.

Risk: The installation flow can register persistent user-level systemd services and download dependencies and models.

Mitigation: Review the systemd units and dependency sources before enabling autostart; disable autostart until the installation behavior is approved.

Risk: The direct clone-speak endpoint can operate on file paths and reference audio supplied to the local service.

Mitigation: Do not use the direct clone-speak endpoint with arbitrary file paths; prefer the guided workflow with duration checks and local file retention controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aurora2035/skills/xeontts)
- [Publisher profile](https://clawhub.ai/user/aurora2035)
- [Qwen3-TTS Base OpenVINO INT8 model](https://huggingface.co/aurora2035/Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8)
- [Qwen3-TTS CustomVoice OpenVINO INT8 model](https://huggingface.co/aurora2035/Qwen3-TTS-12Hz-0.6B-CustomVoice-OpenVINO-INT8)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local audio files through the installed services; generated files and reference audio default to seven-day retention.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
