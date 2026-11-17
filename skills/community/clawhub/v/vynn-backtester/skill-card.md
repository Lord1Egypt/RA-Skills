## Description:

Run trading strategy backtests with natural language -- powered by Vynn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beee003](https://clawhub.ai/user/beee003)

### License/Terms of Use:


## Use Case:

External users, developers, and trading strategy builders use this skill to run and compare strategy backtests from natural language or structured entry and exit rules. It returns performance metrics such as Sharpe ratio, total return, drawdown, win rate, trade count, and equity-curve related results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends strategy descriptions, ticker lists, lookback periods, and the Vynn API key to the configured Vynn endpoint.

Mitigation: Use a dedicated Vynn API key and avoid submitting confidential trading logic or sensitive portfolio information unless the Vynn service and its retention claims are trusted.

Risk: Changing VYNN_BASE_URL can send authenticated requests to a non-default endpoint.

Mitigation: Set VYNN_BASE_URL only to a trusted endpoint before running backtests.

## Reference(s):

- [Vynn Backtester on ClawHub](https://clawhub.ai/beee003/skills/vynn-backtester)
- [Vynn](https://the-vynn.com)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown or plain text summaries with structured backtest metrics and optional Python usage snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VYNN_API_KEY; optional VYNN_BASE_URL can redirect requests to a trusted self-hosted endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
