## Description:

web-search-minimax uses the Minimax Coding Plan Search API to run web searches and return results with related search suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbos1314](https://clawhub.ai/user/xbos1314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search for current information, technical documentation, news, and tutorials through Minimax-backed web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the external Minimax API and may disclose sensitive terms if users include them.

Mitigation: Do not include secrets, credentials, private customer data, or sensitive business terms in search queries.

Risk: The skill requires a MINIMAX_API_KEY, and exposure of that key could allow unauthorized API use.

Mitigation: Store the API key as an environment secret, avoid writing it into skill files or prompts, and rotate it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xbos1314/skills/web-search-minimax)
- [Publisher profile](https://clawhub.ai/user/xbos1314)
- [Minimax API host](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Console text with search result titles, links, snippets, dates, and related search suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and MINIMAX_API_KEY; sends search query text to the external Minimax API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
