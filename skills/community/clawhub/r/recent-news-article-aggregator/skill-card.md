## Description: <br>
Searches AgentPMT's recent news database for articles by topic, category, country, language, and publication age. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to retrieve current news articles for briefings, topical monitoring, source discovery, and current-event or market research through AgentPMT-hosted remote calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics and filters are sent to an AgentPMT-hosted remote service. <br>
Mitigation: Keep queries concise and avoid sending private, sensitive, or unnecessary user text as search topics. <br>
Risk: Searches may consume paid AgentPMT credits. <br>
Mitigation: Use broad, deliberate queries first and retry only after fixing schema, authentication, payment, or parameter issues. <br>
Risk: News schemas, endpoint behavior, and examples can change over time. <br>
Mitigation: Fetch live schema or instructions before production integration or whenever parameters, outputs, or examples are unclear. <br>


## Reference(s): <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/recent-news-article-aggregator) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/recent-news-article-aggregator) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, text] <br>
**Output Format:** [Markdown instructions with JSON request examples and schema tables; remote tool responses are JSON article objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requests can include topic, news_type, categories, exclude_categories, max_age_in_days, country, and language; each search is priced at 10 AgentPMT credits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
