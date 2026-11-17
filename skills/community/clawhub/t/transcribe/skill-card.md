## Description:

Transcribe audio files to text using local Whisper in Docker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javicasper](https://clawhub.ai/user/javicasper)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe local audio files, including voice messages and common audio formats, into plain text for responses or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer attempts a privileged global CLI install.

Mitigation: Review the installer before running it and prefer a user-local install path when possible.

Risk: The Docker build uses mutable upstream content and unpinned Python dependencies.

Mitigation: Pin and review the base image and dependencies before deployment.

Risk: The artifact references a scripts/transcribe wrapper that is not present in the provided files.

Mitigation: Confirm the wrapper is supplied or update the installer before use.

Risk: Transcriptions may be inaccurate or use the wrong language setting.

Mitigation: Review transcribed text before using it for decisions, records, or user-facing responses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/javicasper/skills/transcribe)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text transcription with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally through Docker; default language is Spanish unless a language or auto-detection is requested.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
