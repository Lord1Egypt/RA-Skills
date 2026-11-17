## Description:

Get YouTube autocomplete suggestions with FlashData. Use for YouTube keyword research, discovering search phrases, expanding a topic or comparing suggestions across languages and regions. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketers can use the skill to explore YouTube search phrasing, expand topic ideas, and compare autocomplete suggestions across languages or regions. It requires a FlashData API key with access to YouTube suggestions, and data queries spend paid Credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner verdict is benign, but the review is incomplete; using hosted FlashData sends the API key and query arguments to the service, and data queries spend paid Credits.

Mitigation: Use a protected key with only the required source access, send only task-relevant query inputs, and check the expected Credit use before querying.

## Reference(s):

- [FlashData YouTube suggestions documentation](https://flashdata.dev/docs/sources/youtube_suggestions?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_suggestions-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_suggestions-task)
- [FlashData API key signup](https://flashdata.dev/signup?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=youtube_suggestions-task)
- [ClawHub release](https://clawhub.ai/flashdatadev/skills/youtube-autocomplete-flashdata)
- [Publisher profile](https://clawhub.ai/user/flashdatadev)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Suggestion phrases with the query and locale; can be returned as a list or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggestions are not search-volume estimates or video results. Regional comparisons require a separate billed request for each region.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
