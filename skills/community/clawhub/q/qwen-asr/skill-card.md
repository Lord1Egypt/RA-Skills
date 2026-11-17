## Description:

Transcribes audio files using Qwen ASR (千问STT) when users want voice messages converted to text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[al-one](https://clawhub.ai/user/al-one)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe user-provided audio files or stdin audio into plain text through the Qwen ASR demo service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files are uploaded to the external qwen-qwen3-asr-demo.ms.show service, and retention or consent handling is not documented.

Mitigation: Use only audio that can be shared with that service; obtain appropriate consent for sensitive speech and review terms before operational use.

Risk: Runtime dependencies are not pinned in the artifact.

Mitigation: Pin and review Python dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/al-one/skills/qwen-asr)
- [Qwen ASR demo service](https://qwen-qwen3-asr-demo.ms.show)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text transcript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single transcript returned to stdout; no local output file is written unless the caller redirects it.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
