## Description:

Search YouTube for videos, channels, playlists or Shorts, filtered by upload date, duration or sort order, through the YTAPI API, then read the transcripts of the results. Use when the user wants to find YouTube videos on a topic, recent talks or tutorials, reviews, or what creators say about something. 中文：搜索 YouTube 视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytapi](https://clawhub.ai/user/ytapi)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can find YouTube videos, channels, playlists, and Shorts for a topic or time period, then retrieve relevant transcripts for research, learning, reviews, or understanding creator commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key setup can persist the key across sessions without asking, and temporary files have no specified access protections.

Mitigation: Choose a secure storage location before setup, restrict key access to the agent that needs it, and use private temporary files.

Risk: Optional account creation sends an email address and verification code to YTAPI; search and transcript requests use account credits.

Mitigation: Get consent before account creation, explain credit use, and prefer an existing YTAPI connector when available.

## Reference(s):

- [YTAPI documentation](https://docs.ytapi.dev)
- [API key setup guidance](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Search result and transcript text or structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and transcript requests consume YTAPI credits.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
