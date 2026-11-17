## Description:

TranscriptAPI lets agents retrieve YouTube transcripts, search videos and channels, browse channel and playlist videos, and support video-based research through transcriptapi.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[therohitdas](https://clawhub.ai/user/therohitdas)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to fetch and summarize YouTube transcripts, search and browse videos, channels, and playlists, and compare video content when YouTube sources are relevant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may expose sensitive credentials, email addresses, OTP codes, API keys, and temporary auth files if the agent handles or stores them carelessly.

Mitigation: Prefer creating the account yourself, entering OTPs directly on the provider site, and storing TRANSCRIPT_API_KEY in a dedicated secret manager rather than chat, shell profiles, or temporary files.

Risk: The skill makes TranscriptAPI requests for YouTube lookups using a TranscriptAPI key.

Mitigation: Install only if you are comfortable letting the agent use TranscriptAPI for YouTube lookup tasks, and restrict use to the documented transcript, search, channel, and playlist workflows.

## Reference(s):

- [TranscriptAPI homepage](https://transcriptapi.com)
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json)
- [TranscriptAPI auth setup](references/auth-setup.md)
- [ClawHub skill page](https://clawhub.ai/therohitdas/skills/transcriptapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples and JSON API response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and internet access to transcriptapi.com; most API requests consume TranscriptAPI credits.]

## Skill Version(s):

1.5.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
