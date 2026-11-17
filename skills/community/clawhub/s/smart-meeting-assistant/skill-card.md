## Description:

Smart Meeting Assistant transcribes meeting audio, generates structured meeting minutes, and extracts action items from transcripts using the AstronClaw API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external collaborators use this skill to turn meeting recordings or transcripts into transcripts, meeting summaries, and action-item JSON for follow-up workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting recordings, transcripts, summaries, and action items may contain confidential or regulated information that is sent to AstronClaw or the configured enterprise endpoint.

Mitigation: Use the skill only for meetings approved for that endpoint, avoid sensitive or regulated recordings unless organizational policy permits it, and document retention expectations before use.

Risk: A custom ASTRONCLAW_API_BASE can direct uploaded meeting data and the API token to an untrusted service.

Mitigation: Do not set ASTRONCLAW_API_BASE to an untrusted URL; prefer a hardened version that validates the API host and requires HTTPS.

Risk: Network requests without explicit timeout behavior can hang or fail unclearly during transcription, summarization, or todo extraction.

Mitigation: Prefer a hardened version that uses request timeouts and warns users before upload.

## Reference(s):

- [AstronClaw API Reference](references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/skills/smart-meeting-assistant)
- [AstronClaw API Base](https://api.astronclaw.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Plain text transcripts, Markdown meeting minutes, JSON action items, and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The full pipeline writes timestamped transcript, summary, and todo files to the selected output directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
