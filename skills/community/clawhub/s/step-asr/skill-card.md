## Description:

Transcribe audio files to text via Step ASR streaming API (HTTP SSE). Supports Chinese and English, multiple audio formats (PCM, WAV, MP3, OGG/OPUS), real-time streaming output, and terminology correction prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[randzero](https://clawhub.ai/user/randzero)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to transcribe selected audio files with StepFun's Step ASR API, including streaming text output, saved transcript files, and optional JSON results with usage statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files and optional prompt text are sent to StepFun for remote transcription.

Mitigation: Use the skill only for recordings and prompt content approved for StepFun processing under the user's privacy and data-handling requirements.

Risk: The skill requires a StepFun API key in STEPFUN_API_KEY.

Mitigation: Provide credentials through the environment or approved ClawHub configuration and avoid embedding API keys in shared commands, files, or transcripts.

## Reference(s):

- [Step ASR Streaming API Documentation](https://platform.stepfun.com/docs/zh/api-reference/audio/asr-stream)
- [Step Platform](https://platform.stepfun.com/)
- [ClawHub Skill Page](https://clawhub.ai/randzero/skills/step-asr)
- [ClawHub Publisher Profile](https://clawhub.ai/user/randzero)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, configuration]

**Output Format:** [Plain text transcript, optional JSON object with usage statistics, or saved transcript file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports streaming or final-only output, Chinese or English language selection, optional terminology prompt, explicit audio format selection, inverse text normalization toggle, and rerun correction toggle.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
