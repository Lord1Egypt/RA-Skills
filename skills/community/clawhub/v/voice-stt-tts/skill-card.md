## Description:

Full voice message setup (STT + TTS) for OpenClaw using faster-whisper and Edge TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aksenkin](https://clawhub.ai/user/aksenkin)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure OpenClaw voice-message transcription and voice replies for Telegram bot workflows. It provides setup guidance for a Python faster-whisper transcription script, OpenClaw audio settings, and Edge TTS configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice messages and generated replies may contain sensitive content, and Edge TTS may involve remote processing.

Mitigation: Use the skill only in environments where this processing is acceptable and review data-handling requirements before deployment.

Risk: Runtime installation uses Python packages without a pinned lockfile, which can reduce reproducibility and supply-chain assurance.

Mitigation: Prefer pinned dependency versions or a reviewed lockfile for higher-assurance installations.

## Reference(s):

- [OpenClaw Audio Documentation](https://docs.openclaw.ai/nodes/audio)
- [OpenClaw TTS Documentation](https://docs.openclaw.ai/tts)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, Python, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation steps, an example transcription script, OpenClaw configuration, restart commands, testing steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
