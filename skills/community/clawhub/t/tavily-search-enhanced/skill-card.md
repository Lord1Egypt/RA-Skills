## Description: <br>
Provides Tavily-powered web, news, Q&A, image, and context search for agents, returning structured results with titles, URLs, snippets, and optional answer summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nowhere1975](https://clawhub.ai/user/nowhere1975) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run current web research, news lookups, direct Q&A, image search, and domain-restricted searches through the Tavily API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, domains, mode choices, and related parameters are sent to Tavily. <br>
Mitigation: Use a dedicated revocable Tavily API key and avoid submitting secrets or confidential data in queries. <br>
Risk: Returned search results and AI answer summaries are external content and may be incomplete or inaccurate. <br>
Mitigation: Review the cited source URLs before relying on results for decisions or downstream content. <br>
Risk: The skill needs a Tavily API key to run. <br>
Mitigation: Store only a scoped Tavily key for this workflow and rotate or revoke it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nowhere1975/tavily-search-enhanced) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [Tavily News API endpoint](https://api.tavily.com/news) <br>
- [Tavily Q&A API endpoint](https://api.tavily.com/qna) <br>
- [Tavily Images API endpoint](https://api.tavily.com/images) <br>
- [Tavily Context API endpoint](https://api.tavily.com/context) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, or plain text depending on the selected CLI output format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY; result counts are bounded by the script's mode-specific limits.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
