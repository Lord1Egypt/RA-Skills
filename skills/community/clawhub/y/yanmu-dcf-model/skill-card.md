## Description:

Provides DCF valuation modeling for equity research, including five-year free cash flow forecasts, terminal value discounting, and WACC/growth sensitivity heatmaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and equity-research users can run the skill to generate DCF valuation outputs for supported A-share, Hong Kong, and U.S. tickers. The outputs support analysis workflows and should be reviewed as financial modeling assistance rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script makes outbound requests to Sina Finance for live quote data.

Mitigation: Run it only in environments where this network access is acceptable, and review network policy before deployment.

Risk: The script writes a PNG heatmap into the selected output directory.

Mitigation: Use a trusted, scoped output directory and review generated files before sharing or publishing them.

Risk: DCF valuation outputs can be incomplete or misleading if assumptions, market data, or embedded company data are stale or unsuitable.

Mitigation: Treat results as modeling support and require qualified human review before making investment or business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoling7878-arch/skills/yanmu-dcf-model)
- [Sina Finance](https://finance.sina.com.cn)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; the script can emit text or JSON and write a PNG sensitivity heatmap.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on ticker, market, WACC, terminal growth, output directory, and selected text or JSON format.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
