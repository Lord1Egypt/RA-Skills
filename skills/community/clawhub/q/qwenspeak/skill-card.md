## Description:

Text-to-speech generation via Qwen3-TTS over SSH, including preset voices, voice cloning, and voice design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit YAML-driven Qwen3-TTS jobs to a trusted qwenspeak SSH instance, monitor job status, and retrieve generated speech audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can run a remote installer as root.

Mitigation: Pin the installer to an immutable release or commit, verify a signed checksum when available, and review exactly what sudo will execute before installation.

Risk: Text, YAML job configuration, transcripts, and audio files are transmitted to the configured SSH server.

Mitigation: Use only a qwenspeak instance you run or explicitly trust, verify the server host key out of band, and use a dedicated SSH key.

Risk: Voice cloning can misuse sensitive biometric voice data or enable impersonation.

Mitigation: Clone only voices with explicit speaker consent, ask for provenance when unclear, and do not support impersonation, fraud, harassment, or deceptive synthetic-media use.

## Reference(s):

- [qwenspeak setup](references/setup.md)
- [docker-qwenspeak project](https://github.com/psyb0t/docker-qwenspeak)
- [docker-lockbox project](https://github.com/psyb0t/docker-lockbox)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with shell commands and YAML configuration examples; remote commands may return JSON job status and audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QWENSPEAK_HOST and QWENSPEAK_PORT to target a running, trusted qwenspeak SSH instance.]

## Skill Version(s):

1.5.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
