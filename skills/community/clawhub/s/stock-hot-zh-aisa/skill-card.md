## Description:

Scans real-time stock and cryptocurrency movers through AISA to identify hot assets, large price swings, market momentum, gainers, losers, and news-driven activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate current market-mover reports for stocks and cryptocurrencies, including momentum summaries, top gainers and losers, active-volume names, news catalysts, and watchlist candidates. The output is informational and is not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AISA_BASE_URL can redirect requests, including the AISA API key, to a configured endpoint.

Mitigation: Leave AISA_BASE_URL unset unless the endpoint is intentionally configured and trusted.

Risk: Prompts that trigger the scanner may be sent to the external AISA service.

Mitigation: Avoid including sensitive personal, account, or proprietary information in scanner prompts.

Risk: The script declares a broad OpenAI client dependency for runtime use.

Mitigation: Use a reviewed, pinned dependency version for operational deployments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aisadocs/skills/stock-hot-zh-aisa)
- [AISA API endpoint](https://api.aisa.one/v1)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown market report, with an optional compact JSON summary when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; supports focus modes for both markets, stocks only, or crypto only.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
