## Description:

Fetch voice note emails via IMAP, transcribe attachments with OpenAI Whisper, and save transcripts to an Obsidian vault's fleeting notes folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and productivity-focused developers use this skill to turn voice-note email attachments into searchable Obsidian fleeting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires mailbox credentials and an OpenAI API key.

Mitigation: Use an app-specific email password and a limited OpenAI key where available.

Risk: Matching audio attachments are uploaded to OpenAI for transcription.

Mitigation: Install only when this data flow is acceptable for the voice recordings being processed.

Risk: The skill writes Markdown files to the configured Obsidian vault path.

Mitigation: Keep the fleeting-notes folder to a simple relative folder under the intended vault.

Risk: Processed emails may be marked as read.

Mitigation: Set MARK_EMAIL_READ=false unless marking source emails as read is desired.

## Reference(s):

- [Voice Note Transcriber on ClawHub](https://clawhub.ai/terrycarter1985/skills/voice-note-transcriber)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)
- [OpenAI audio transcription endpoint](https://api.openai.com/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Files]

**Output Format:** [Markdown notes with YAML frontmatter plus console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcript notes to the configured Obsidian fleeting-notes folder.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
