## Description:

Zhipu Web Search provides cURL-based web search through Zhipu AI's dedicated web_search API with configurable engine, count, intent, and recency options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyhit2005](https://clawhub.ai/user/whyhit2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search current web information through Zhipu AI when they need configurable search engines, result counts, recency filters, or API-level JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and request parameters are sent to Zhipu AI using the configured ZHIPU_API_KEY.

Mitigation: Avoid secrets, personal data, regulated data, and sensitive internal project names in search queries.

Risk: The wrapper has input-validation and documentation gaps around engine, count, recency, and the advertised domain-filter feature.

Mitigation: Validate allowed parameter values before use and either implement or remove domain-filter documentation for operational workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whyhit2005/skills/zhipu-web-search)
- [Zhipu Web Search API endpoint](https://open.bigmodel.cn/api/paas/v4/web_search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples; API responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY and curl; search queries and request parameters are sent to Zhipu AI.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
