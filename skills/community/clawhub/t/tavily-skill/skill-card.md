## Description: <br>
Uses the Tavily API for real-time web search and content extraction when an agent needs current web information, with a Tavily API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangkelvin](https://clawhub.ai/user/fangkelvin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search the live web, research current topics, retrieve recent news, and request Tavily search results or extracted content through documented curl examples or the bundled shell script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Tavily's service and may reveal sensitive research terms or private context. <br>
Mitigation: Avoid secrets, private internal URLs, regulated data, confidential research terms, or other sensitive content in Tavily queries. <br>
Risk: The Tavily API key is required for operation and could be exposed if hardcoded into files or shared examples. <br>
Mitigation: Keep TAVILY_API_KEY in a scoped environment variable or protected runtime configuration, and do not commit it to skill files or logs. <br>


## Reference(s): <br>
- [Tavily homepage](https://tavily.com) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [ClawHub release page](https://clawhub.ai/fangkelvin/tavily-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash and JSON examples; script output is JSON formatted with jq.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and TAVILY_API_KEY; supports query, search depth, max results, answer inclusion, and image inclusion options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
