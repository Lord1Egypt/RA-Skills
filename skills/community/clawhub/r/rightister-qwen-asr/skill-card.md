## Description:

Offline Chinese and mixed Chinese-English speech-to-text recognition in pure C without Python or FFmpeg dependencies, suitable for edge devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rightister](https://clawhub.ai/user/rightister)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to transcribe Chinese or mixed Chinese-English audio locally with a C-based Qwen ASR implementation, including edge deployments where Python and external runtime dependencies are undesirable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill builds and runs an unverified third-party ASR checkout from the user's home directory.

Mitigation: Clone and pin a known qwen-asr commit, review the repository and build output, and verify the binary before running the skill.

Risk: Submitted audio may contain sensitive data, and temporary converted audio can remain if execution fails before cleanup.

Mitigation: Treat input audio as sensitive, run in an appropriate local environment, and remove temporary audio artifacts after failures.

## Reference(s):

- [qwen-asr reference README](references/README.md)
- [antirez/qwen-asr GitHub repository](https://github.com/antirez/qwen-asr)
- [Qwen3-ASR-0.6B model](https://huggingface.co/antirez/qwen3-asr-0.6b)
- [Qwen3-ASR-1.7B model](https://huggingface.co/antirez/qwen3-asr-1.7b)
- [ClawHub skill page](https://clawhub.ai/rightister/skills/rightister-qwen-asr)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcription with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports small and large model selection plus configurable thread count; returns transcription text after local audio preprocessing and offline inference.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
