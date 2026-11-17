## Description:

Fetch every transcript on a YouTube channel (up to 1,000) as one background bulk job via the BulkTranscripts API, list a channel's videos, or search inside one channel for a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratie](https://clawhub.ai/user/pratie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to collect or search transcripts from a creator's YouTube channel for research, summarization, knowledge-base, or RAG workflows. It guides the agent through BulkTranscripts API authentication, bulk jobs, polling, transcript retrieval, error handling, and credit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested YouTube or TikTok references to the third-party BulkTranscripts service, and fetched transcripts may be stored in that account's library.

Mitigation: Confirm the user's intent before submitting sensitive video, channel, playlist, or TikTok references, and review BulkTranscripts account and data-handling expectations before use.

Risk: Bulk channel jobs can consume credits when adding new transcripts to the account library.

Mitigation: Check billing.remaining, explain expected credit use before large jobs, cap max_videos where appropriate, and stop when the service reports out_of_credits.

Risk: The skill requires a BulkTranscripts API key.

Mitigation: Use BULKTRANSCRIPTS_API_KEY as a bearer token only for BulkTranscripts requests, avoid exposing it in chat or logs, and ask the user to rotate invalid or misplaced keys.

## Reference(s):

- [BulkTranscripts documentation](https://bulktranscripts.co/docs)
- [BulkTranscripts OpenAPI specification](https://bulktranscripts.co/openapi.json)
- [BulkTranscripts YouTube MCP server](https://bulktranscripts.co/youtube-mcp-server)
- [ClawHub skill page](https://clawhub.ai/pratie/skills/youtube-channel-transcripts)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, markdown, configuration]

**Output Format:** [Markdown with curl command examples and JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BULKTRANSCRIPTS_API_KEY and may return transcript text, transcript metadata, bulk job status, search results, or account balance details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
