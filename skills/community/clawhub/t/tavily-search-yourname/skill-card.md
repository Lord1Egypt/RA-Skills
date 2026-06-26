## Description: <br>
AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yi307520559-droid](https://clawhub.ai/user/yi307520559-droid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent run Tavily web searches, tune result count and search depth, search general or news topics, and extract content from supplied URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary reports an undocumented wrapper that can turn a search query into local shell command execution. <br>
Mitigation: Review or remove openclaw-wrapper.js before installation and prefer the direct search.mjs and extract.mjs scripts when using the skill. <br>
Risk: Search queries and extracted URLs are sent to the Tavily API and may expose confidential queries, private URLs, or internal resources. <br>
Mitigation: Use a dedicated Tavily API key and avoid submitting confidential queries, private URLs, or internal resources. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/yi307520559-droid/tavily-search-yourname) <br>
- [Publisher Profile](https://clawhub.ai/user/yi307520559-droid) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with search answers, source lists, extracted URL content, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output is capped by script options at 1 to 20 results and requires TAVILY_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
