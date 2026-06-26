## Description: <br>
Uses the Tavily API to perform web searches optimized for LLMs and AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhc888007](https://clawhub.ai/user/jhc888007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily web searches with configurable depth, topic, country, date, domain, image, and output-format options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, domain filters, selected search options, and API-authenticated requests are sent to Tavily. <br>
Mitigation: Avoid sensitive internal terms, secrets, and regulated data in search queries or filters unless Tavily processing is approved for that use. <br>
Risk: The skill requires access to a Tavily API key. <br>
Mitigation: Set TAVILY_API_KEY as an environment variable or trusted local secret, and avoid exposing the key in prompts, logs, or shared configuration. <br>
Risk: README guidance may change OpenClaw web-search behavior. <br>
Mitigation: Review any suggested OpenClaw configuration changes before applying them so the agent uses the intended search provider. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jhc888007/tavily-search-simple) <br>
- [Tavily Search API Documentation](https://docs.tavily.com/documentation/api-reference/endpoint/search) <br>
- [Tavily Website](https://www.tavily.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Raw JSON, Brave-like JSON, or human-readable Markdown search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY and sends search queries plus selected search options to Tavily.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
