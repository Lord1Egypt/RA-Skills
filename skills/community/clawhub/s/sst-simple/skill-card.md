## Description:

Local speech-to-text using OpenAI Whisper for transcribing audio files, voice messages, and multilingual recordings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkisme](https://clawhub.ai/user/lkisme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run local speech-to-text transcription for audio files, voice messages, and multilingual recordings. It is suited for workflows that need transcript text or JSON command output while keeping processing local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled session identifiers can write transcript files outside the intended folder.

Mitigation: Avoid arbitrary session_id values; restrict them to trusted, validated identifiers before running the skill.

Risk: The installer makes broad host changes while setting up runtime dependencies.

Mitigation: Install only in a constrained environment under an unprivileged runtime account, and review host changes before production use.

Risk: Generated transcripts may contain sensitive local data.

Mitigation: Treat transcript outputs as sensitive files and apply local access controls and retention limits.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin dependencies before production use and review updates before deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkisme/skills/sst-simple)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text transcripts, JSON command output, and Markdown usage guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcript files to a local output directory; optional session identifiers separate outputs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
