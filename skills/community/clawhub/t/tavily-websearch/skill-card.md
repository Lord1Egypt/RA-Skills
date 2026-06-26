## Description: <br>
Searches the web using Tavily's Search API and returns relevant results with snippets, scores, and metadata for research or source lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanYDL](https://clawhub.ai/user/evanYDL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to issue Tavily web searches when they need current web results, source links, snippets, scores, or metadata for a user request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search request JSON is sent to Tavily under the user's Tavily API key. <br>
Mitigation: Use only non-sensitive queries and avoid sending secrets, credentials, proprietary data, or sensitive personal data. <br>
Risk: API usage may consume Tavily quota or incur billing under the configured key. <br>
Mitigation: Use an API key with appropriate quota and billing limits for the deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evanYDL/tavily-websearch) <br>
- [Tavily Documentation](https://docs.tavily.com/documentation) <br>
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and TAVILY_API_KEY; sends the provided JSON body to Tavily's search endpoint.] <br>

## Skill Version(s): <br>
7.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
