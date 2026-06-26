## Description: <br>
AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhjack](https://clawhub.ai/user/hhjack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to run Tavily web searches, retrieve concise source snippets, search current news, and extract page content from URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The search script lets an external API response choose JavaScript to load and run locally. <br>
Mitigation: Review or patch scripts/search.mjs before installing by replacing response-controlled formatter imports with fixed bundled formatting or a hardcoded local allowlist. <br>
Risk: Queries and URLs are sent to Tavily, which may expose sensitive or private information to a third-party service. <br>
Mitigation: Avoid sending sensitive queries or private/internal URLs unless that sharing is acceptable, and use a limited Tavily API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hhjack/t-web-searcher) <br>
- [Tavily](https://tavily-search.com) <br>
- [Tavily Search API endpoint](https://api.tavily-search.com/search) <br>
- [Tavily Extract API endpoint](https://api.tavily-search.com/extract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-like command-line text with answers, source lists, URLs, snippets, and extracted page content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; search results are capped between 1 and 20.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
