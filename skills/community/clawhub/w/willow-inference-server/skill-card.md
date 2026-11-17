## Description:

Provides guidance for using a local Willow Inference Server to transcribe audio with ASR and generate speech with TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deantiwang](https://clawhub.ai/user/deantiwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and call a trusted Willow Inference Server for local speech-to-text transcription and text-to-speech generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs and runs unpinned code from an external repository.

Mitigation: Use a pinned and trusted Willow server revision, inspect utils.sh before execution, and avoid elevated privileges unless clearly required.

Risk: Audio recordings and TTS text may contain personal, confidential, or regulated information.

Mitigation: Send audio and text only to a Willow server that the user trusts and controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deantiwang/skills/willow-inference-server)
- [Willow Inference Server upstream repository referenced by setup](https://github.com/toverainc/willow-inference-server.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides guidance and commands for ASR and TTS requests; generated audio or transcripts come from the configured Willow server.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
