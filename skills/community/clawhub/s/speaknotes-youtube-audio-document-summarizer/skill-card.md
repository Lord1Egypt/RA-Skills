## Description:

Use when OpenClaw needs to call SpeakNotes API routes directly using an API key and generate transcripts or summaries from YouTube URLs, media files, or document files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacklillie](https://clawhub.ai/user/jacklillie)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect OpenClaw to SpeakNotes for YouTube, media-file, and document summarization workflows. It helps create uploads, poll note status, retrieve notes, and access folders through the SpeakNotes API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a SpeakNotes API key that can create uploads and read notes or folders available to that key.

Mitigation: Use a scoped or revocable API key where supported, store it only as SPEAKNOTES_API_KEY, and ask the agent to access existing notes or folders only when needed.

Risk: A user or agent could expose the API key by sending it to an untrusted host or printing it in output.

Mitigation: Use only https://api.speaknotes.io for API calls and do not print, log, or send the key to user-provided hosts.

## Reference(s):

- [SpeakNotes OpenClaw Integration](https://speaknotes.io/integrations/openclaw)
- [SpeakNotes API Host](https://api.speaknotes.io)
- [ClawHub Skill Page](https://clawhub.ai/jacklillie/skills/speaknotes-youtube-audio-document-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown or structured task response with action, endpoints_used, noteId, status, result, and next_step fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SpeakNotes API key supplied via SPEAKNOTES_API_KEY and uses the official SpeakNotes API host.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
