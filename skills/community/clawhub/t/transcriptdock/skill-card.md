## Description:

Fetch timed transcripts and captions from YouTube, TikTok and Instagram Reel links with the Transcript Dock API or hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afaqak](https://clawhub.ai/user/afaqak)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to retrieve captions or transcriptions from YouTube, TikTok, Instagram Reels, or media files they own. They can review the transcript with segment timing and export it in common text and subtitle formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media submitted for transcription may be sent to Transcript Dock for processing; the security evidence flags a missing privacy notice before upload.

Mitigation: Before submitting media, review Transcript Dock's privacy terms and confirm you are comfortable with its processing.

Risk: Requests require a Transcript Dock API key, which could be exposed if mishandled.

Mitigation: Keep the key private and send it only to the configured Transcript Dock origin.

## Reference(s):

- [Transcript Dock MCP documentation](https://www.transcriptdock.com/docs/mcp)
- [Transcript Dock hosted MCP server](https://www.transcriptdock.com/mcp)
- [Transcript Dock on ClawHub](https://clawhub.ai/afaqak/skills/transcriptdock)

## Skill Output:

**Output Type(s):** [Text, JSON, Subtitle files]

**Output Format:** [Transcript text with segment timing; exports as TXT, JSON, SRT, or VTT]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timed subtitle exports require usable timing in the transcript result.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
