## Description:

Transcribes audio from an uploaded file_id or public HTTPS URL into text, SRT, WebVTT, or JSON with optional word timestamps, profanity filtering, alternatives, and speaker diarization through AgentPMT-hosted remote calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit meeting recordings, voice memos, interviews, podcasts, webinars, and similar audio for transcription, then poll task status and retrieve transcript outputs with optional speaker labels and timing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio supplied by file_id or public URL is processed by AgentPMT and transcription providers.

Mitigation: Avoid confidential or regulated recordings unless the user's organization permits that processing.

Risk: npx-based setup steps may introduce supply-chain exposure.

Mitigation: Prefer the OpenClaw install route, or verify and pin setup dependencies before running npx commands.

Risk: Selecting a tier below the recording length can fail after submission and may still consume credits.

Mitigation: Choose the tier from the known recording length and review error_details.recommended_actions before resubmitting.

## Reference(s):

- [Speech To Text With Speakers ClawHub Page](https://clawhub.ai/agentpmt/skills/speech-to-text-with-speakers)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/speech-to-text-with-speakers)
- [Speech To Text With Speakers Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [AgentPMT File Management](https://clawhub.ai/agentpmt/file-management)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration guidance]

**Output Format:** [Markdown guidance with JSON tool-call examples; task outputs may include plain text, SRT, WebVTT, or structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription jobs run asynchronously; completed tasks can include inline transcript content, speaker data, timing metadata, and File Manager artifact identifiers.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
