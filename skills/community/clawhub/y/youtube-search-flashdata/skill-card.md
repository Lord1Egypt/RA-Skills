## Description:

Search YouTube with FlashData by keyword, upload date, duration and other filters. Use for finding videos, tutorials and talks, sorting by views or recency, and collecting video IDs and channel information. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers can use this skill to find YouTube videos for tutorials, talks, recommendations, and other research or application workflows. They can narrow searches by upload date, duration, subtitles, and other filters, then use returned video IDs and channel details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search requests send the API key and query arguments to FlashData MCP, and data queries spend paid FlashData Credits.

Mitigation: Keep the key in protected environment or secret-manager settings, review query scope and cost before running it, and check an existing job or the FlashData console before retrying a timed-out paid submission.

Risk: Security review evidence is incomplete because Skillspector marked coverage partial after two local references could not be resolved.

Mitigation: Review the skill and its dependencies and resolve the missing-reference coverage before relying on the scan as a complete assessment.

## Reference(s):

- [FlashData YouTube Search documentation](https://flashdata.dev/docs/sources/youtube_search?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_search-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_search-task)
- [Sample query](references/query.json)
- [Input schema](references/schema.json)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON search results with video and channel metadata, plus usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standard searches accept 1–20 results and may return fewer; returned fields depend on available video metadata.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
