## Description:

AI-powered search agent that performs intelligent web searches, aggregates results, and provides summarized answers with source citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and other external users use this skill to search current web, news, academic, and code sources, then receive summarized answers with citations, confidence information, and related queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and fetched page URLs may be sent to external services.

Mitigation: Avoid secrets, private personal information, regulated data, and sensitive business queries unless provider and logging practices have been reviewed.

Risk: Dependency behavior and transitive dependency versions may change in controlled environments.

Mitigation: Use a lockfile or reviewed dependency versions before deployment.

Risk: Language selection may affect returned sources and summaries.

Mitigation: Set SEARCH_LANGUAGE explicitly for the intended audience and locale.

Risk: Search results depend on external source availability, indexing, and rate limits.

Mitigation: Review cited sources and configure result limits, timeouts, and source filters for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgta23/skills/search-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON objects from the API and Markdown-style CLI summaries with citations, source lists, confidence scores, and related queries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include external URLs, credibility scores, timestamps, configured language, and search metadata.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
