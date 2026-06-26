## Description: <br>
AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huihui-hb](https://clawhub.ai/user/huihui-hb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-powered web searches, including deeper searches, news queries, and date-limited news searches. They can also extract clean content from specific URLs for downstream analysis or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and URLs are sent to Tavily for processing. <br>
Mitigation: Use the skill only with searches and URLs that are appropriate to share with Tavily. <br>
Risk: The skill requires a Tavily API key. <br>
Mitigation: Provide TAVILY_API_KEY through the environment or OpenClaw configuration rather than hard-coding it in files. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [Tavily Extract API endpoint](https://api.tavily.com/extract) <br>
- [ClawHub skill page](https://clawhub.ai/huihui-hb/tavily-search-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands] <br>
**Output Format:** [Markdown text printed by Node.js command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes an optional answer and source list; extraction output includes fetched page content and failed URL notices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
