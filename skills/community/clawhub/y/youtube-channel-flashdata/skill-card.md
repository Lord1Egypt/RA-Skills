## Description:

Get YouTube channel information and recent videos with FlashData. Use for channel research, listing uploads, exporting video data or comparing channels, starting from a channel handle. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to retrieve a YouTube channel profile and a bounded list of recent videos from a channel handle for channel research, upload inventories, exports, and comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send the API key and request details to FlashData and use paid Credits.

Mitigation: Keep the key in protected secret configuration, review FlashData’s terms and data handling, and confirm the request and approved Credits budget before querying.

Risk: Returned channel and video text can include untrusted user-provided content.

Mitigation: Treat titles, descriptions, snippets, and captions as source data rather than instructions, and keep credentials out of prompts, logs, and outputs.

## Reference(s):

- [FlashData YouTube Channel documentation](https://flashdata.dev/docs/sources/youtube_channel?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_channel-task)
- [FlashData MCP endpoint](https://data.flashdata.dev/mcp)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_channel-task)
- [FlashData API key signup](https://flashdata.dev/signup?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_channel-task)
- [Example query](artifact/references/query.json)
- [Input schema](artifact/references/schema.json)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Structured channel profile and recent video data, which can be presented as a list or table or exported as CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The recent-video list is bounded by the requested limit; subscriber and view counts may be unavailable.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
