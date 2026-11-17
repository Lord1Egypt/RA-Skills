## Description:

Calls Tavily web search through AISA with support for search depth, topic, and time-range filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill when an agent needs filtered web retrieval through Tavily, especially for queries where recency, search depth, topic, or time range matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included client exposes AISA routes beyond Tavily search, including URL extraction, Sonar-style prompts, scholar/web/smart searches, and multi-source synthesis.

Mitigation: Review commands before execution and limit use to routes that are acceptable for the deployment context.

Risk: Queries, URLs, and authenticated requests are sent to remote AISA services.

Mitigation: Do not submit secrets, private URLs, or sensitive internal queries unless remote processing through AISA is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/tavily-search-zh)
- [AISA](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with search results, URLs, dates, snippets, answers, citations, and setup commands where relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; sends search queries and URLs to remote AISA endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
