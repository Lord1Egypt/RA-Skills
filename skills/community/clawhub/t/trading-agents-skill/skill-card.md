## Description:

Orchestrates a multi-agent trading research workflow that analyzes stocks through fundamental, technical, sentiment, news, debate, trading, risk, and portfolio review roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huahang](https://clawhub.ai/user/huahang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to coordinate stock research, debate competing investment theses, and produce trading recommendations with risk and portfolio review. It is intended as AI-assisted market research, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided tickers may be placed into shell commands and output filenames.

Mitigation: Run the skill in a sandboxed workspace, use simple validated stock symbols, avoid untrusted ticker text, and prefer a version that validates tickers and confines output paths.

Risk: The skill may produce incorrect or misleading trading recommendations.

Mitigation: Treat outputs as research assistance only, require human review before decisions, cite primary sources, and keep the financial-advice disclaimer in user-facing reports.

Risk: Market data, news, and sentiment inputs may be stale or incomplete.

Mitigation: Verify source dates, current prices, and authoritative filings before relying on the analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huahang/skills/trading-agents-skill)
- [TradingAgents framework paper (arXiv 2412.20138)](https://arxiv.org/abs/2412.20138)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON market data files, shell commands, and conversational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analyst reports, a debate record, a final recommendation summary, and a required financial-advice disclaimer.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
