## Description:

Transcribe audio files (voice notes, recordings, podcasts) to text via the Speechmatics batch transcription API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyh](https://clawhub.ai/user/coreyh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to submit permitted audio recordings to Speechmatics batch transcription and retrieve transcripts for review, notes, subtitles, or downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio recordings and API credentials may be exposed if endpoint controls are pointed at an untrusted service.

Mitigation: Use only the official Speechmatics HTTPS endpoint or a trusted proxy, and prevent untrusted users or prompts from setting --base-url or SPEECHMATICS_BASE_URL.

Risk: The security evidence reports a confirmed command-execution weakness.

Mitigation: Review and harden the script before installation, keep timeout and polling values under trusted control, and rescan the skill before deployment.

Risk: Transcription sends audio content to an external service.

Mitigation: Use the skill only with recordings the user is allowed to send to Speechmatics and review transcripts before taking destructive or externally visible follow-up actions.

## Reference(s):

- [Speechmatics batch transcription documentation](https://docs.speechmatics.com/introduction/batch-transcription)
- [ClawHub Speechmatics skill page](https://clawhub.ai/coreyh/skills/speechmatics)
- [ClawHub publisher profile](https://clawhub.ai/user/coreyh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript, Speechmatics JSON, or SRT subtitle file, with shell command guidance for invocation and configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a Speechmatics API key; writes transcript output to a requested path or next to the input audio file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
