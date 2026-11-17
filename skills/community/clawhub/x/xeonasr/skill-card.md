## Description:

Installs and operates a local OpenVINO Qwen3-TTS voice synthesis workflow for OpenClaw QQBOT, supporting short reference-audio voice cloning and styled TTS generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aurora2035](https://clawhub.ai/user/aurora2035)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add local TTS workflows to OpenClaw QQBOT, including 3 to 5 second reference-audio voice cloning and styled speech generation. It is intended for machines trusted to run local model services and manage generated audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release exposes powerful unauthenticated local TTS and voice-cloning services, including a Node workflow gateway on port 9002.

Mitigation: Run only on trusted machines, firewall or reconfigure the gateway to bind to 127.0.0.1, and do not expose port 9002 to a LAN or the internet.

Risk: The installer creates persistent user-level systemd services and modifies OpenClaw QQBOT configuration.

Mitigation: Inspect the generated systemd units and OpenClaw config changes before enabling them, and avoid running installation as root except where package installation requires it.

Risk: Voice cloning can reproduce a speaker from short reference audio.

Mitigation: Restrict access to trusted users, require consent for reference audio, and review generated files under the configured retention policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aurora2035/skills/xeonasr)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Qwen3-TTS Base OpenVINO INT8 model](https://huggingface.co/aurora2035/Qwen3-TTS-12Hz-0.6B-Base-OpenVINO-INT8)
- [Qwen3-TTS CustomVoice OpenVINO INT8 model](https://huggingface.co/aurora2035/Qwen3-TTS-12Hz-0.6B-CustomVoice-OpenVINO-INT8)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated audio and reference files locally with a default 7-day retention policy.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
