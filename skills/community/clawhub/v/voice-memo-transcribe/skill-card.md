## Description:

Transcribe Apple Voice Memos recordings to text, organize the content, and save structured notes to Apple Notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[my12121-beep](https://clawhub.ai/user/my12121-beep)

### License/Terms of Use:

MIT-0

## Use Case:

Mac users and agent operators use this skill to find iCloud-synced Apple Voice Memos, extract or generate transcripts, summarize recordings with timestamps, and save reviewed notes to Apple Notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks the terminal for broad access to protected Mac Voice Memos and Notes data.

Mitigation: Install only in an environment where that access is acceptable, prefer exporting selected recordings manually, and grant Full Disk Access only after reviewing the skill and dependencies.

Risk: Private transcript content may be written to local temporary files or synced through Apple Notes and iCloud.

Mitigation: Review transcripts before saving or syncing them, avoid including sensitive recordings when possible, and delete temporary transcript or note-content files after use.

Risk: Transcription or speaker/name identification can be inaccurate.

Mitigation: Confirm unclear names, speakers, relationships, and topic labels with the user before finalizing notes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell commands and timestamped transcript text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local Voice Memos data and produce temporary transcript or note-content files when the user chooses file output or Apple Notes export.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
