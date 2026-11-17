## Description:

Queries minute-level market data for major Chinese stock indices including the Shanghai Composite, Shenzhen Component, ChiNext, CSI 300, and STAR 50.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer current-market questions about major Chinese stock indices and to retrieve JSON data that an agent can summarize or use for trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JisuAPI AppKey and sends requests to JisuAPI for its intended functionality.

Mitigation: Use a scoped or low-privilege JisuAPI key where available, avoid exposing logs that may include request details, and rotate the key if it may have been disclosed.

Risk: Market index data may be delayed, unavailable, or returned as API error responses.

Mitigation: Check the returned JSON for error fields and timestamps before using the data in trading, reporting, or user-facing summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/stockindex)
- [JisuAPI stock index API documentation](https://www.jisuapi.com/api/stockindex/)
- [JisuAPI provider website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON returned by a Python command-line script, with agent-facing Markdown guidance in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable; network calls are made to JisuAPI.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
