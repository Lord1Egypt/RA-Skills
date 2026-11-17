## Description:

通过 AISA 评估股票的股息率、派息安全性、增长情况和收益质量。触发条件：当用户关心股息安全、收益型投资、股息增长或股息贵族筛选时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze dividend yield, payout safety, dividend growth, and income quality for one or more stock tickers. It is intended for informational dividend-investing analysis and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undocumented AISA_BASE_URL override can redirect the AISA API key and requests to another server.

Mitigation: Run only in controlled environments where AISA_BASE_URL cannot be set by untrusted shell startup files, wrappers, CI variables, or other users; consider pinning the openai dependency.

Risk: Ticker prompts and AISA_API_KEY-backed requests leave the machine for the AISA service.

Mitigation: Use an approved AISA endpoint and avoid submitting sensitive non-public investment information.

Risk: The output is financial analysis and may be mistaken for investment advice.

Mitigation: Present results as informational only and require user review against current market data before any investment decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/stock-dividend-zh)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown dividend analysis with optional JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; sends ticker prompts and API-key-backed requests to the configured AISA-compatible service.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
