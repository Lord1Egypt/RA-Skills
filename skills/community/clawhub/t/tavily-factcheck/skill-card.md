## Description:

Enhanced Tavily web search for fact-checking and cross-verification, with support for time ranges, exact matching, domain filtering, finance search, images, raw content, and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkkkane84727](https://clawhub.ai/user/kkkkane84727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily searches that verify claims, current events, cited facts, and financial information. It is positioned as a fact-checking helper for cross-verification rather than a replacement for broader research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The search script can fall back to reading TAVILY_API_KEY from ~/.openclaw/.env or ~/.env when the environment variable is not set.

Mitigation: Set TAVILY_API_KEY explicitly for the agent process and avoid storing unrelated secrets in generic home .env files.

Risk: Queries and optional raw-content retrieval are sent to Tavily, which may be inappropriate for sensitive or proprietary topics.

Mitigation: Use the skill only for queries that are acceptable to send to Tavily, and avoid enabling raw content unless the extra page text is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kkkkane84727/skills/tavily-factcheck)
- [Tavily API](https://tavily.com)
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown search summaries by default, or raw JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tavily API key and can include answer text, source URLs, optional raw page content, optional image URLs, response timing, and request metadata.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
