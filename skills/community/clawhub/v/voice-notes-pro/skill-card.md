## Description:

Voice Notes Pro transcribes WhatsApp voice notes with OpenAI Whisper and routes the resulting text into local Markdown notes for songs, tasks, shopping, ideas, people, and watchlists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toniaczlog](https://clawhub.ai/user/toniaczlog)

### License/Terms of Use:

MIT

## Use Case:

People who capture notes through WhatsApp use this skill to turn voice recordings into categorized Markdown files. It is aimed at personal productivity workflows that include tasks, shopping lists, ideas, contacts, song drafts, and media watchlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A message-supplied local file path could cause the skill to read and upload unintended local files.

Mitigation: Run the skill in a tightly sandboxed account and restrict access to the intended WhatsApp media directory until path validation is fixed.

Risk: Voice audio and transcripts may contain personal or sensitive information and are sent to OpenAI and written to local Markdown files.

Mitigation: Use only with data appropriate for OpenAI transcription and protect the notes directory with least-privilege filesystem permissions.

Risk: The security verdict is suspicious.

Mitigation: Review and scan the release before installation, and avoid running it as root or with broad filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/toniaczlog/skills/voice-notes-pro)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Status text plus appended Markdown notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes categorized notes to local Markdown files under the configured notes directories.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
