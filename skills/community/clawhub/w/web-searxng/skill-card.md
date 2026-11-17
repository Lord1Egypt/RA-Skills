## Description:

web-searxng lets agents query a configured SearXNG instance for privacy-oriented web search, aggregate results, and format either general search results or stock-style analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xumanzi](https://clawhub.ai/user/xumanzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route web-search tasks through SearXNG, including general result aggregation and finance-related searches that are formatted as stock analysis reports. It is useful when a workflow needs a configurable search endpoint and concise Markdown summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private search terms may be sent to an untrusted or unintended SearXNG endpoint.

Mitigation: Set SEARXNG_URL explicitly to a trusted instance before use and verify endpoint routing before submitting sensitive queries.

Risk: Search queries and results may be stored in the local scripts/.cache directory.

Mitigation: Avoid sensitive queries when local caching is unacceptable and clear scripts/.cache after use when needed.

Risk: Stock-mode output can look like financial analysis or recommendations.

Mitigation: Treat stock reports as generic generated analysis, verify market data against authoritative sources, and do not use the output as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xumanzi/skills/web-searxng)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown search summaries, Markdown stock-style reports, or a fallback search link when SearXNG is unavailable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be live or served from a local one-hour cache; general search output includes up to 20 processed results.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
