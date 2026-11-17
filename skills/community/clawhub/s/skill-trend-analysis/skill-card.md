## Description:

Helps agents analyze ClawHub Skills growth trends, ranking changes, search filters, statistics, tags, authors, time windows, exports, and related API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingdingdemao](https://clawhub.ai/user/dingdingdemao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query read-only ClawHub trend endpoints, compare skill rankings over time, and summarize growth, search, author, tag, and statistics results with supporting parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend-analysis queries and query parameters are sent to skills.easytoken.cc, and the default endpoint uses unencrypted HTTP.

Mitigation: Avoid sensitive search terms or query parameters, prefer HTTPS or a trusted network where available, and review generated commands before execution.

Risk: API rate limiting may return HTTP 429 responses during repeated trend queries.

Mitigation: Wait at least 3 seconds before retrying the same endpoint and keep requests focused on the necessary time window and metric.

## Reference(s):

- [Skill Trend Analysis API Endpoints](references/api-endpoints.md)
- [Skill Trend Analysis on ClawHub](https://clawhub.ai/dingdingdemao/skills/skill-trend-analysis)
- [ClawHub Skills Trend API](http://skills.easytoken.cc/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise conclusions, supporting data, and optional curl, jq, or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint names, query parameters, time windows, metrics, rank limits, and rate-limit retry guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
