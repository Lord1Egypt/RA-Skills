## Description:

Checks a YouTube channel's latest uploads through the BulkTranscripts API and fetches transcripts only for videos that are new.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratie](https://clawhub.ai/user/pratie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and analysts use this skill to monitor YouTube channels, identify newly posted videos, and request transcripts only when a new video should be processed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BulkTranscripts API keys could be exposed if copied into shared logs, prompts, or files.

Mitigation: Keep the key private, pass it through BULKTRANSCRIPTS_API_KEY, and avoid storing or echoing bearer tokens.

Risk: Channel identifiers and video requests are sent to BulkTranscripts, and transcript calls may consume API credits.

Mitigation: Tell users before making API calls, check billing.remaining in responses, and fetch transcripts only for videos that are new or relevant.

Risk: Recurring digests can accumulate unnecessary monitoring history.

Mitigation: Store only the minimal seen-video state needed to avoid duplicate processing.

## Reference(s):

- [BulkTranscripts Docs](https://bulktranscripts.co/docs)
- [BulkTranscripts OpenAPI Spec](https://bulktranscripts.co/openapi.json)
- [BulkTranscripts MCP Server](https://bulktranscripts.co/youtube-mcp-server)
- [ClawHub Skill Page](https://clawhub.ai/pratie/skills/youtube-upload-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON API responses, billing fields, video identifiers, and transcript text returned by BulkTranscripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
