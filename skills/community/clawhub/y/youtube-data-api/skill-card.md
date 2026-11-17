## Description:

Search YouTube and retrieve videos, shorts, comments, transcripts, streams, channel data, and community posts as structured data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content researchers use this skill to find YouTube videos and channels and retrieve metadata, transcripts, comments, community posts, and stream links through Scavio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube lookup requests go through Scavio as an intermediary.

Mitigation: Use the skill only when sharing the requested queries with Scavio is acceptable.

Risk: The required API key could be exposed if committed to source control.

Mitigation: Keep SCAVIO_API_KEY in a secure environment or secret store, not in checked-in files.

Risk: Paginated, transcript, stream, and bulk channel requests can consume paid credits.

Mitigation: Confirm credit costs before large or repeated requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/youtube-data-api)
- [Scavio documentation](https://scavio.dev/docs)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance and code examples; retrieved data is structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on available YouTube data; stream links expire.]

## Skill Version(s):

1.0.4 (source: ClawHub release; skill file lists 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
