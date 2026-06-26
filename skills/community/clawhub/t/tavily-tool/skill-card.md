## Description: <br>
Use Tavily web search/discovery to find URLs/sources, do lead research, gather up-to-date links, or produce a cited summary from web results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tylordius](https://clawhub.ai/user/tylordius) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily searches from the terminal, collect current source URLs, support lead research, and gather web evidence for cited summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and any included sensitive context are sent to Tavily. <br>
Mitigation: Use a revocable Tavily API key, scope TAVILY_API_KEY only to trusted agents, and avoid placing secrets or private data in search queries. <br>


## Reference(s): <br>
- [Tavily API notes](references/tavily-api.md) <br>
- [Tavily search endpoint](https://api.tavily.com/search) <br>
- [ClawHub skill page](https://clawhub.ai/tylordius/tavily-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search responses, URL lists, and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY and sends explicit search queries to Tavily.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
