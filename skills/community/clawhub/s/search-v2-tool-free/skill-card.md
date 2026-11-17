## Description: <br>
搜索工具免费版 helps agents run lightweight Tavily-powered web searches with LLM-friendly result summaries, basic or advanced search depth, result limits, time filtering, and simple domain filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent builders use this skill to retrieve web search results and concise summaries for quick fact finding, technical troubleshooting, and everyday information lookup. It is not intended for secrets, regulated data, medical diagnosis, legal decisions, or other high-stakes decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and selected parameters are sent to Tavily as external API requests. <br>
Mitigation: Do not use the skill for secrets, private internal content, regulated data, or tasks that do not require web search. <br>
Risk: Search results and summaries can be incomplete, outdated, or unsuitable for high-stakes decisions. <br>
Mitigation: Verify important claims against authoritative sources and avoid using the skill for medical diagnosis, legal decisions, or other critical determinations. <br>
Risk: The skill depends on a Tavily API key, network access, and command execution support. <br>
Mitigation: Confirm the agent environment has the required API key and network access before relying on the skill in a workflow. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/search-v2-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON search-result examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search responses may include result titles, URLs, content summaries, relevance scores, optional answer summaries, and response timing; the free edition documents a maximum of 10 results per search.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
