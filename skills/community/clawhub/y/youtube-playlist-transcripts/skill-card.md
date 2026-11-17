## Description:

Fetch every transcript of a YouTube playlist as one background bulk job via the BulkTranscripts API, or list the playlist in order and fetch videos one by one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratie](https://clawhub.ai/user/pratie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need YouTube playlist transcripts for lecture series, courses, study notes, or text extraction workflows. The skill guides an agent through bulk playlist transcript jobs, ordered playlist listing, individual transcript retrieval, balance checks, and API error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends playlist or video identifiers, transcript request parameters, and the BulkTranscripts bearer token to bulktranscripts.co.

Mitigation: Avoid sensitive private or unlisted playlists unless appropriate, keep the API key in BULKTRANSCRIPTS_API_KEY, and avoid pasting bearer tokens into locations where they may be logged.

## Reference(s):

- [BulkTranscripts](https://bulktranscripts.co)
- [BulkTranscripts Docs](https://bulktranscripts.co/docs)
- [BulkTranscripts OpenAPI Spec](https://bulktranscripts.co/openapi.json)
- [BulkTranscripts YouTube MCP Server](https://bulktranscripts.co/youtube-mcp-server)
- [ClawHub Skill Page](https://clawhub.ai/pratie/skills/youtube-playlist-transcripts)
- [Publisher Profile](https://clawhub.ai/user/pratie)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown with inline shell commands and API response field guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for third-party API calls and downstream transcript handling; it does not itself persist transcript data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
