## Description: <br>
Enhanced Tavily web search for fact-checking and cross-verification, aligned with the official Tavily API and supporting time range, exact match, domain filtering, and finance-topic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkkkane84727](https://clawhub.ai/user/kkkkane84727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to cross-check research results, validate cited facts for content production, and retrieve timely Tavily search results for news or finance queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and API-key-authenticated requests are sent to Tavily. <br>
Mitigation: Install only when Tavily receiving search queries is acceptable, and avoid sending sensitive or confidential content in queries. <br>
Risk: The script can read a Tavily API key from local fallback env files if TAVILY_API_KEY is not set. <br>
Mitigation: Prefer setting TAVILY_API_KEY explicitly in the runtime environment and review local ~/.openclaw/.env or ~/.env usage before deployment. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search) <br>
- [ClawHub Skill Page](https://clawhub.ai/kkkkane84727/tavily-factcheck) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown search summaries by default, with optional raw JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include answer text, source URLs, relevance scores, optional image links, optional raw page markdown, response timing, and request metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
