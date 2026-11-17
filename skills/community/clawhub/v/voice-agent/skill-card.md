## Description:

Local Voice Input/Output for Agents using the AI Voice Agent API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardotrevisan](https://clawhub.ai/user/ricardotrevisan)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to transcribe user-provided audio files with a local Whisper-backed service and synthesize agent responses into audio files through the configured Voice Agent API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthesized text is processed through an AWS Polly-backed path.

Mitigation: Avoid sending sensitive text for synthesis unless AWS Polly processing is acceptable for the intended use.

Risk: Audio output can overwrite writable files at the requested output path.

Mitigation: Direct generated audio to a dedicated output folder and use non-sensitive filenames.

Risk: Large files or special device paths may cause reliability or safety issues during transcription.

Mitigation: Use ordinary audio files of reasonable size and do not ask the agent to transcribe special device paths.

Risk: The skill depends on a trusted backend API at localhost:8000.

Mitigation: Use the skill only with a trusted local backend and review backend setup before execution.

## Reference(s):

- [Voice Agent ClawHub page](https://clawhub.ai/ricardotrevisan/skills/voice-agent)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file-path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill invokes a localhost API for transcription, synthesis, and health checks; synthesized audio is written to a user-specified file path.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
