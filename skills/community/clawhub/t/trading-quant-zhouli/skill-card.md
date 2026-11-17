## Description:

A quantitative trading data analysis skill for real-time A-share, US, Hong Kong, and precious-metals quotes, with multidimensional scoring across technical, capital-flow, fundamentals, news, and sentiment signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to retrieve market data, run stock and commodity analysis commands, inspect capital-flow and anomaly signals, and summarize multi-market conditions. Outputs are informational analysis and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data scores and BUY/SELL-style labels can be mistaken for investment advice.

Mitigation: Present outputs as informational analysis, preserve the investment-risk disclaimer, and require human judgment before any trading decision.

Risk: The skill contacts public market and news APIs and writes local cache files.

Mitigation: Run it only where network access and cache storage are acceptable, and review configured cache paths before use in sensitive environments.

Risk: Sentiment analysis may download model artifacts when local caches are missing.

Mitigation: Pin and pre-approve dependencies and model revisions, or pre-populate trusted local model caches for controlled deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/trading-quant-zhouli)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-formatted CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact public market and news APIs, write local caches, and rely on optional sentiment-model artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
