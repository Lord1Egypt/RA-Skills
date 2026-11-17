## Description:

Use UniFuncs Search for real-time web search when users need current information, articles, news, resources, or market data from the internet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinlic](https://clawhub.ai/user/vinlic)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to run authenticated UniFuncs web searches for current web results when no specific source URL is already known.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the UniFuncs API key are sent to UniFuncs for authenticated lookup.

Mitigation: Use a dedicated UniFuncs API key and avoid sending sensitive or confidential queries unless that data sharing is acceptable.

Risk: Broad search-trigger wording can cause the skill to be used for many web lookup requests.

Mitigation: Reserve the skill for requests that genuinely require current web retrieval, and apply freshness filters only when recency is necessary.

## Reference(s):

- [UniFuncs account and API key setup](https://unifuncs.com/account)
- [UniFuncs Web Search API endpoint](https://api.unifuncs.com/api/web-search/search)
- [ClawHub skill page](https://clawhub.ai/vinlic/skills/unifuncs-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown, or plain text search results returned through a shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports freshness filters, image inclusion, pagination, result count selection, and stock-query handling.]

## Skill Version(s):

0.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
