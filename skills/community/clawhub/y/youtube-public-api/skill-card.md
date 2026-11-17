## Description:

Read-only YouTube data API for video, channel, playlist, comments, related-video, search, and transcript research through ReplyNodes prepaid credits with one long-lived Bearer fetcher key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to retrieve public YouTube search results, video and channel metadata, playlist details, public comments, related videos, and transcripts through ReplyNodes. It is intended for read-only research and integration workflows that can use prepaid credits and a bearer fetcher key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer key exposure could allow unauthorized use of ReplyNodes credits.

Mitigation: Store REPLYNODES_API_KEY only in the agent secret store, never place it in prompts, URLs, logs, source files, or returned data, and rotate or revoke it if exposed.

Risk: YouTube lookup parameters are sent to ReplyNodes and requests consume prepaid credits.

Mitigation: Use the skill only when that data sharing and credit model are acceptable, monitor credit usage, and configure explicit paid overage caps.

Risk: Public upstream YouTube data may be unavailable, incomplete, or unsupported for a requested item.

Mitigation: Treat unavailable upstream data as unavailable, preserve gateway response envelopes and request IDs, and do not fabricate missing fields or success states.

## Reference(s):

- [Operations catalog](artifact/references/operations.json)
- [ClawHub skill page](https://clawhub.ai/replynodes-ai/skills/youtube-public-api)
- [ReplyNodes account setup](https://app.replynodes.com/auth)
- [ReplyNodes developer keys](https://app.replynodes.com/developers)
- [ReplyNodes YouTube API gateway](https://api.replynodes.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with HTTP endpoint guidance, inline shell commands, and JSON API response references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only GET operations for public YouTube data; requires REPLYNODES_API_KEY as a bearer token and uses prepaid credits.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter, manifest.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
