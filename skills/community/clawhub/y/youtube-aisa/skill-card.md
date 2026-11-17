## Description:

Search YouTube videos, channels, and playlists through the AISA YouTube endpoint with one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search YouTube videos, channels, and playlists with query, locale, pagination, and filter parameters through the AISA YouTube API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube search queries and the AISA_API_KEY are sent to api.aisa.one.

Mitigation: Avoid private or sensitive search terms, use a revocable key where possible, and install only when this data flow is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/youtube-aisa)
- [Publisher profile](https://clawhub.ai/user/bibaofeng)
- [OpenClaw homepage](https://openclaw.ai)
- [AISA YouTube search endpoint](https://api.aisa.one/apis/v1/youtube/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and structured API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and AISA_API_KEY; API responses may include videos or grouped sections.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
