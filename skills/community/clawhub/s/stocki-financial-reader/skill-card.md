## Description:

Institutional-grade financial data skill for OpenClaw that retrieves real-time quotes, financials, valuation time series, OHLCV history, industry membership, consensus forecasts, and composite analysis across cn/hk/us markets and multiple asset types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17817942676](https://clawhub.ai/user/17817942676)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw agent users use this skill to retrieve and summarize structured market and financial data from Stocki for quotes, OHLCV, financial statements, valuation panels, industry and index membership, consensus forecasts, and composite company analysis. It is not for investment advice or transaction execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer executes a remote shell script.

Mitigation: Review the installer before use, prefer a version-pinned or otherwise inspectable install path, and run it only if SkillHub is trusted.

Risk: STOCKI_API_KEY can be sent to any configured gateway URL.

Mitigation: Set STOCKI_GATEWAY_URL only to https://skill.stocki.com.cn or a trusted local development gateway, avoid remote http:// endpoints, and rotate the key if it may have reached an untrusted service.

Risk: Financial queries, symbols, date ranges, and credentials are sent to the configured Stocki service.

Mitigation: Avoid including sensitive personal data in requests and confirm the Stocki service terms for the intended data use.

Risk: Returned financial data may be delayed, incomplete, adjusted, or misunderstood as advice.

Mitigation: Present outputs as non-advisory data, preserve freshness and availability warnings, and require independent verification before decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/17817942676/skills/stocki-financial-reader)
- [README](README.md)
- [Install and setup](INSTALL.md)
- [Market calendar](references/market-calendar.md)
- [Realtime quote](references/realtime-quote.md)
- [Price history](references/price-history.md)
- [Industry and symbols](references/industry-and-symbols.md)
- [Fundamentals panel](references/fundamentals-panel.md)
- [Consensus and target](references/consensus-and-target.md)
- [Financial context](references/financial-context.md)
- [Metric resolver](references/metric-resolver.md)
- [Name resolver](references/name-resolver.md)
- [Stocki gateway service](https://skill.stocki.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with structured financial figures, request examples, setup commands, and diagnostic guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tabular financial data, API request payloads, diagnostic exit codes, and non-advisory caveats.]

## Skill Version(s):

0.4.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
