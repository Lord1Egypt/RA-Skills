## Description:

Transcribe audio or video into text or captions with a Wiro AI speech to text model. Use when the user wants a recording or a video turned into text, captions or subtitles with Wiro AI or through the Wiro MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn audio or video recordings into transcripts or captions. They can request language selection, timestamps, speaker labels, SRT or VTT captions, and optionally save the resulting file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings may contain sensitive information; the workflow can send local files to Wiro, and the security review noted missing privacy disclosure.

Mitigation: Check that a recording is appropriate to share with Wiro before processing, especially when it contains sensitive information.

## Reference(s):

- [Wiro MCP Server documentation](https://wiro.ai/docs/wiro-mcp-server)
- [Wiro AI Transcription on ClawHub](https://clawhub.ai/wiroai/skills/wiro-transcribe)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text transcript or SRT/VTT caption file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional language, timestamps, speaker labels, caption format, and save path.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
