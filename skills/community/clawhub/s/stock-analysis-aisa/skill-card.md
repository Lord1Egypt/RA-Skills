## Description:

Analyze stocks and cryptocurrencies with live AISA-backed scoring, signals, confidence, and risk flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request stock or cryptocurrency analysis, compare tickers, and review market positioning with scored signals and risk flags. The skill is informational only and does not provide financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AISA_API_KEY and may send requested ticker analysis to an AISA-compatible API.

Mitigation: Run it in a minimal environment with only the required API key exposed.

Risk: An optional AISA_BASE_URL override can redirect requests to a different endpoint.

Mitigation: Do not set AISA_BASE_URL unless the endpoint is fully trusted.

Risk: Stock and cryptocurrency outputs can be mistaken for investment advice.

Mitigation: Treat outputs as informational analysis only and require user review before financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/stock-analysis-aisa)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown analysis with optional fenced JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ticker scores, BUY/HOLD/SELL-style signals, confidence levels, comparison summaries, and risk flags.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
