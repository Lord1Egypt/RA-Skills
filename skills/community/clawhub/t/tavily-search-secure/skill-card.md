## Description:

Safely uses the Tavily API to run web searches, collect sourced results, extract text from URLs, and support summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabekar](https://clawhub.ai/user/fabekar)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Tavily-backed web searches and extract readable text from specific public URLs when they need sourced research inputs or summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, target URLs, and the Tavily API key are sent to Tavily's API.

Mitigation: Use only when that data transfer matches the applicable data policy, avoid confidential queries and private URLs, and keep the API key in the environment rather than files or output.

Risk: Extracted web content may be incomplete, misleading, or unsuitable for direct use without review.

Mitigation: Review sourced results and extracted text before relying on them in summaries, decisions, or downstream agent actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fabekar/skills/tavily-search-secure)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [Tavily Extract API endpoint](https://api.tavily.com/extract)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with answer and source sections for search, or URL-headed extracted text sections for extraction.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped at 10, extraction is capped at 5 URLs per request, and script output is sanitized and length-limited.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
