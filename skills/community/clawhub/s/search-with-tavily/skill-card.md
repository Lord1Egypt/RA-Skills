## Description: <br>
Web search using Tavily API - a powerful search engine for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chasehl](https://clawhub.ai/user/chasehl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to search the web through Tavily for current information, direct Q&A answers, and retrieval context for RAG workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to an external Tavily service and may reveal sensitive topics if users include secrets, credentials, regulated personal data, or confidential internal information. <br>
Mitigation: Use a dedicated, revocable Tavily API key and avoid searching for sensitive or confidential material. <br>
Risk: The fast search helper can write query-derived cached results to local storage for a short period. <br>
Mitigation: Disable caching with the no-cache option or clear the local cache when searches may contain sensitive information. <br>
Risk: Web search results and generated answers can be incomplete, stale, or misleading. <br>
Mitigation: Review returned source URLs and verify important claims before operational use. <br>


## Reference(s): <br>
- [Tavily API Reference](references/TAVILY_API.md) <br>
- [Tavily Documentation](https://docs.tavily.com) <br>
- [Tavily API Reference Documentation](https://docs.tavily.com/documentation/api-reference) <br>
- [Tavily Python SDK](https://github.com/tavily-ai/tavily-python) <br>
- [Tavily JavaScript SDK](https://github.com/tavily-ai/tavily-js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [JSON search results, plain-text answers, retrieval context, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY and sends search queries to Tavily; the fast search script may cache search results locally for five minutes unless disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
