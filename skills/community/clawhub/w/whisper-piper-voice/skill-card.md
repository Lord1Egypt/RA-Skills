## Description:

Set up and run a fully local voice pipeline that combines Whisper STT and Piper TTS behind a single HTTP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgrobelny](https://clawhub.ai/user/danielgrobelny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, and run a local speech-to-text and text-to-speech service for voice assistants or audio workflows. It provides setup guidance, server commands, API examples, and model selection guidance for CPU or CUDA deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unauthenticated local HTTP service can be exposed beyond the intended host.

Mitigation: Bind the service to localhost unless authentication and TLS are added, and run it as a dedicated unprivileged user.

Risk: Downloaded Piper executables and model files may be used without verification.

Mitigation: Pin and verify downloaded executables and model artifacts before running them.

Risk: Persistent systemd autostart can keep an insufficiently hardened service running.

Mitigation: Avoid enabling autostart until binding, authentication, TLS, user isolation, and request limits are in place.

## Reference(s):

- [Voice Pipeline Setup Guide](references/setup-guide.md)
- [Piper Linux release archive](https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz)
- [Piper voice samples](https://rhasspy.github.io/piper-samples/)
- [Thorsten Emotional Piper voice model](https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx)
- [Thorsten Emotional Piper voice model config](https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten_emotional/medium/de_DE-thorsten_emotional-medium.onnx.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides a local HTTP voice server that accepts audio transcription requests and text-to-speech requests.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
