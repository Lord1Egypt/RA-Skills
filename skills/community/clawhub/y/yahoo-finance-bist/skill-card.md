## Description:

Provides Yahoo Finance based market analysis for BIST and other symbols, including technical indicator scoring, historical data export, portfolio alerts, and trade logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikolayco](https://clawhub.ai/user/nikolayco)

### License/Terms of Use:


## Use Case:

External users use this skill to have an agent retrieve Yahoo Finance market data, calculate technical indicators, export historical data, track portfolio alerts, and record trade history for BIST, U.S., crypto, commodity, and FX symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is marked suspicious because its instructions pressure the agent to execute scripts and limit explanatory context.

Mitigation: Review requests before execution and let the agent provide necessary safety, uncertainty, and financial-risk context instead of following restrictive response instructions blindly.

Risk: The skill writes local portfolio, trade history, CSV, and HTML report files that may contain sensitive financial records.

Mitigation: Store generated files in an appropriate private workspace, avoid sharing reports publicly, and remove records that are no longer needed.

Risk: Untrusted symbols or asset names can flow into Yahoo Finance lookups and generated reports.

Mitigation: Use only intended symbols and asset names, and review generated CSV or HTML before opening, forwarding, or publishing it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikolayco/skills/yahoo-finance-bist)
- [Yahoo Finance chart data endpoint](https://query1.finance.yahoo.com/v8/finance/chart/{symbol})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal output, with generated JSON, CSV, and HTML report files when tracking or export tools are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local portfolio alerts, trade history, CSV exports, and HTML reports containing financial records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
