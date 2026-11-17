## Description:

Installs and configures local whisper.cpp speech-to-text for OpenClaw, including ggml model downloads and an audio wrapper for inbound Telegram voice notes without paid provider APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[truenight](https://clawhub.ai/user/truenight)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to add local offline speech-to-text for inbound Telegram voice notes and configure OpenClaw to invoke the installed wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install workflow builds persistent local software from mutable external sources.

Mitigation: Review the scripts before installing and pin whisper.cpp to a reviewed commit before deployment.

Risk: Model downloads use external URLs without model hash verification.

Mitigation: Download only approved models and verify model file hashes before use.

Risk: The configuration patch changes OpenClaw's audio pipeline and restarts the gateway.

Mitigation: Back up current OpenClaw audio configuration and test in a low-privilege environment before using real inbound voice notes.

## Reference(s):

- [whisper.cpp upstream repository](https://github.com/ggerganov/whisper.cpp)
- [whisper.cpp ggml model downloads](https://huggingface.co/ggerganov/whisper.cpp/resolve/main)
- [Local Whisper ClawHub release page](https://clawhub.ai/truenight/skills/whisper-cpp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local installation, model download, wrapper setup, OpenClaw configuration, cleanup, and troubleshooting guidance.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
