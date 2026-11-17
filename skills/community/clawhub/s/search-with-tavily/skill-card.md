## Description:

Tavily Search provides Tavily API powered web search for current information, direct Q&A answers, and RAG-oriented context retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chasehl](https://clawhub.ai/user/chasehl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve up-to-date web results, direct answers, and search context for retrieval-augmented generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and returned content are sent to Tavily, which creates ordinary privacy considerations for sensitive prompts or confidential data.

Mitigation: Do not submit secrets, private customer data, or confidential internal text in searches.

Risk: The fast helper can cache search results locally under ~/.cache/tavily_search.

Mitigation: Use --no-cache for sensitive searches and delete ~/.cache/tavily_search when cached sensitive results should not remain on disk.

Risk: The skill depends on the tavily-python package and external Tavily API behavior.

Mitigation: Install tavily-python in a virtual environment and pin a reviewed version.

## Reference(s):

- [Tavily API Reference](references/TAVILY_API.md)
- [Tavily Documentation](https://docs.tavily.com)
- [Tavily API Reference Documentation](https://docs.tavily.com/documentation/api-reference)
- [Tavily Python SDK](https://github.com/tavily-ai/tavily-python)
- [Tavily JavaScript SDK](https://github.com/tavily-ai/tavily-js)

## Skill Output:

**Output Type(s):** [text, json, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; CLI helpers return JSON or plain text search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; the fast helper may cache results in ~/.cache/tavily_search unless --no-cache is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
