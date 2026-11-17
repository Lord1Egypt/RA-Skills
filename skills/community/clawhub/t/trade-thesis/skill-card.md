## Description:

Structured pre-trade thesis builder for bull and bear cases, invalidation criteria, data checks, and sizing rationale before live trade deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to structure pre-trade analysis for a proposed live trade, including two-sided market reasoning, a measurable invalidation level, required data checks, and position sizing rationale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill output may influence live-capital trading decisions.

Mitigation: Confirm trade direction, sizing, invalidation level, and stoploss manually before placing or deploying any live trade.

Risk: The skill asks the agent to inspect trading data and wallet balance information for risk sizing.

Mitigation: Use only authorized market and balance data sources, and review the resulting position-size calculation before acting on it.

## Reference(s):

- [Trade Thesis skill page](https://clawhub.ai/superior-ai/skills/trade-thesis)
- [superior-ai publisher profile](https://clawhub.ai/user/superior-ai)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown checklist with concise bullet points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a six-section pre-trade thesis covering thesis statement, bull case, bear case, invalidation level, data checks, and sizing rationale.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
