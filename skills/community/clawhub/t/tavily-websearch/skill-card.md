## Description:

Searches the web with Tavily's Search API and returns relevant results with content snippets, scores, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanydl](https://clawhub.ai/user/evanydl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform web searches through Tavily when a task needs current information, source links, or research context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and selected request fields are sent to Tavily using the configured API key.

Mitigation: Use concise search queries and domain or date filters where possible, and do not include secrets, credentials, private user data, or long prompt contents in the JSON body.

## Reference(s):

- [Tavily Documentation](https://docs.tavily.com/documentation)
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)

## Skill Output:

**Output Type(s):** [Text, JSON, Links, Shell commands, Configuration guidance]

**Output Format:** [JSON search results with titles, URLs, content snippets, relevance scores, and response metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and TAVILY_API_KEY; request bodies are sent to the Tavily Search API.]

## Skill Version(s):

7.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
