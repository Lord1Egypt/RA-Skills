## Description: <br>
AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[petterhuang92-design](https://clawhub.ai/user/petterhuang92-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily web searches, request deeper search, search news, and extract readable content from specified URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and requested URLs are sent to Tavily using the configured API key. <br>
Mitigation: Avoid sending private, internal, secret-bearing, or access-token URLs unless disclosure to Tavily is intended. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/petterhuang92-design/tavily-search-1) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text printed to stdout, including answers, source lists, extracted page content, and failed URL notices.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY. Search requests can choose result count, basic or advanced depth, general or news topic, and news day limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
