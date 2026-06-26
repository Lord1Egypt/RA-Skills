## Description: <br>
Use this when the user asks to search the web, look up recent information, check current events, gather online sources, or research a topic using Tavily search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goktugcy](https://clawhub.ai/user/goktugcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run Tavily web searches for recent information, news, source gathering, and lightweight research from minimal Linux environments without installing third-party Python packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Tavily and may consume the user's Tavily API quota. <br>
Mitigation: Avoid confidential queries and install only where sending queries to Tavily is acceptable. <br>
Risk: The skill depends on a local Tavily API key. <br>
Mitigation: Store the key in .secrets/tavily.key with restrictive permissions and keep the key on the target machine. <br>
Risk: The advertised --api-key and TAVILY_API_KEY methods do not appear to work in this version. <br>
Mitigation: Use the .secrets/tavily.key path until the key-loading behavior is fixed and revalidated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goktugcy/tavily-web-search-for-openclaw) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to Tavily and a valid Tavily API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
