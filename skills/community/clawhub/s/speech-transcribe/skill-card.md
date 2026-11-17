## Description:

Transcribes local audio and video files with sentence-level timestamps using remote L4 GPU Whisper inference, returning plain-text transcripts and SRT subtitle files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speech2srt](https://clawhub.ai/user/speech2srt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run speech-to-text transcription on local audio or video files through a remote GPU workflow and retrieve transcript and subtitle outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled slugs may escape intended paths and affect cleanup behavior in the remote runtime.

Mitigation: Use a fixed simple slug format with only letters, numbers, underscores, and hyphens; reject path separators and special path components before running or cleaning up a job.

Risk: Media files are uploaded to a remote Modal volume for processing.

Mitigation: Use only media that is approved for remote processing, and make retention and cleanup expectations clear before upload.

Risk: Unpinned dependencies can change runtime behavior between installs.

Mitigation: Pin runtime dependencies before treating the skill as routine to install or deploy.

## Reference(s):

- [Error Handling](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and expected transcript and subtitle file names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow can produce .txt transcript files and .srt subtitle files for processed media.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
