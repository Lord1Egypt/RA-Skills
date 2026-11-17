## Description:

Market data analysis toolkit with technical indicators and portfolio tracking for educational use.

This skill is for research and development only.

## Publisher:

[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, OpenClaw users, and technical-analysis learners use this skill to retrieve market data, calculate indicators, generate educational buy/hold/sell labels, size positions, and track portfolios. It is not a financial-advice or trade-execution skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags review-worthy API-key exposure risk when using documented container examples that mount .env files.

Mitigation: Install from reviewed or pinned artifacts, avoid unpinned Docker ':latest' images unless the publisher is trusted, and use limited, revocable market-data API keys.

Risk: Generated buy, sell, and position-sizing labels can be mistaken for financial advice.

Mitigation: Present outputs as educational analysis only, require independent user review, and do not connect the skill to automated trade execution.

Risk: A-share market-data paths use unauthenticated HTTP sources, which can affect data integrity.

Mitigation: Treat A-share results as lower-assurance data, cross-check important outputs against trusted sources, and prefer authenticated HTTPS data providers where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuxuclassmate/skills/trading-assistant-core)
- [Project Homepage](https://github.com/XuXuClassMate/trading-assistant)
- [Documentation Website](https://xuxuclassmate.github.io/trading-assistant/)
- [Installation Guide](https://xuxuclassmate.github.io/trading-assistant/guides/install-overview/)
- [Docker Hub Image](https://hub.docker.com/r/xuxuclassmate/trading-assistant)
- [Twelve Data API](https://twelvedata.com/pricing)
- [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain-text analysis with optional Python, shell, configuration, and JSON-like result snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided market-data API keys for live data paths; generated labels are educational analysis, not trade execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
