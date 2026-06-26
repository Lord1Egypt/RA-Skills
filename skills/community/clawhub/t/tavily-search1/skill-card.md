## Description: <br>
AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp33333333333](https://clawhub.ai/user/cp33333333333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run Tavily-backed web search, news search, and URL content extraction from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and submitted URLs are sent to Tavily, including any sensitive or internal information included by the user. <br>
Mitigation: Avoid submitting internal, localhost, private, or sensitive URLs and queries unless sharing them with Tavily is acceptable. <br>
Risk: The skill requires a Tavily API key and sends requests to an external API provider. <br>
Mitigation: Use a dedicated Tavily API key where possible and manage it through the TAVILY_API_KEY environment variable. <br>
Risk: Search and extracted content may be incomplete, stale, or affected by Tavily result ranking. <br>
Mitigation: Review returned sources and verify important facts against authoritative references before relying on the output. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown text with answers, source lists, extracted URL content, or failed URL notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search supports result count up to 20, basic or advanced depth, general or news topics, and optional news date filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
