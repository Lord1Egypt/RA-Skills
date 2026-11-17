## Description:

Searches AgentPMT's global news database for recent articles by topic, country, language, category, and date using a remote AgentPMT tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search and retrieve recent news articles for current-events lookup, topical monitoring, daily briefings, source discovery, and content generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News-search terms are sent to AgentPMT-hosted remote tool calls.

Mitigation: Avoid confidential, regulated, or sensitive queries and keep tool inputs scoped to the minimum content needed.

Risk: Live remote schema or instruction responses can change after installation.

Mitigation: Review returned schema and instructions before production use, and keep local safety, credential, and tool-use rules authoritative.

Risk: The artifact documents unpinned npx installer commands for supporting setup skills.

Mitigation: Prefer pinned installation paths or ClawHub/OpenClaw setup routes when installing dependencies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/recent-news-article-aggregator)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/recent-news-article-aggregator)
- [Action Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON article results with markdown usage guidance and example request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT calls can return article metadata, URLs, image URLs, source names, publication timestamps, categories, languages, and provider or filter warnings.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
