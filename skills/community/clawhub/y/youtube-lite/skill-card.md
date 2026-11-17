## Description:

Complete YouTube toolkit for transcripts, search, channels, playlists, and metadata via TranscriptAPI.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liliangjie91](https://clawhub.ai/user/liliangjie91)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve YouTube transcripts, search videos and channels, browse playlists, inspect channel content, and combine search-to-transcript workflows through TranscriptAPI.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends YouTube queries and the TranscriptAPI.com API key to a third-party service.

Mitigation: Use it only when the user accepts TranscriptAPI.com processing and keep the API key scoped and revocable.

Risk: The skill can save the API key in local OpenClaw configuration and creates a backup file.

Mitigation: Avoid saving keys on shared machines, review file permissions, and remove plaintext config or backup files when no longer needed.

Risk: Several endpoints consume TranscriptAPI.com credits.

Mitigation: Confirm before using credit-based endpoints and prefer free endpoints when they satisfy the task.

## Reference(s):

- [TranscriptAPI.com](https://transcriptapi.com)
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json)
- [Youtube Lite on ClawHub](https://clawhub.ai/liliangjie91/skills/youtube-lite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TRANSCRIPT_API_KEY and may call free or credit-based TranscriptAPI.com endpoints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
