## Description:

VoxCPM2 - Tokenizer-Free TTS model guide covering installation, Python and CLI usage for TTS, voice design, voice cloning, streaming, vLLM-Omni deployment, and SFT/LoRA fine-tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate VoxCPM2 for multilingual text-to-speech, voice design, voice cloning, streaming, deployment, and fine-tuning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation and repository checkout steps may introduce unreviewed dependencies or code into the user's environment.

Mitigation: Install in a virtual environment or container and prefer pinned versions or reviewed commits before use.

Risk: Demo and API server examples may expose text-to-speech functionality if bound to a public interface.

Mitigation: Keep demo and API servers bound to localhost unless authentication and network restrictions are added.

Risk: Voice cloning and fine-tuning workflows can be misused for impersonation or unauthorized voice reproduction.

Mitigation: Use only voices and transcripts for which rights and consent are available, and do not use generated speech for impersonation or fraud.

## Reference(s):

- [VoxCPM GitHub repository](https://github.com/OpenBMB/VoxCPM.git)
- [vLLM-Omni GitHub repository](https://github.com/vllm-project/vllm-omni.git)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/voxcpm)

## Skill Output:

**Output Type(s):** [text, guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing setup, usage, deployment, and fine-tuning guidance; generated audio files are produced by the referenced VoxCPM tools, not by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
