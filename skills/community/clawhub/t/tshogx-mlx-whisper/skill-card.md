## Description:

Local speech-to-text with MLX Whisper (Apple Silicon optimized, no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tshogx](https://clawhub.ai/user/tshogx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users on Apple Silicon Macs use this skill to run local MLX Whisper speech-to-text transcription, subtitle generation, language-hinted transcription, and translation to English without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated transcripts and subtitle files may contain sensitive audio-derived content.

Mitigation: Choose output folders deliberately, manage file permissions, and delete outputs when no longer needed.

Risk: MLX Whisper models are cached locally under the user's Hugging Face cache.

Mitigation: Delete cached models when they are no longer needed or when local storage policy requires cleanup.

## Reference(s):

- [MLX Whisper examples](https://github.com/ml-explore/mlx-examples/tree/main/whisper)
- [ClawHub skill page](https://clawhub.ai/tshogx/skills/tshogx-mlx-whisper)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may produce local transcript or subtitle files depending on the mlx_whisper command options.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
