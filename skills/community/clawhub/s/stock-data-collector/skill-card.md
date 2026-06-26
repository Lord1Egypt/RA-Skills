## Description: <br>
Collects historical A-share and Hong Kong stock data for specified securities, supports single-stock and batch collection across multiple documented periods, and exports results as CSV files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang-junjian](https://clawhub.ai/user/wang-junjian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to collect historical Chinese A-share and Hong Kong equity data for individual stocks or watchlists and save it as CSV for downstream analysis in spreadsheets or data tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documented data sources and minute-level support may not match the skill's actual behavior. <br>
Mitigation: Verify the provider, market, interval, and fallback behavior on known symbols before relying on outputs for financial analysis or trading decisions. <br>
Risk: The skill depends on external market-data services whose coverage and returned fields can vary. <br>
Mitigation: Validate generated CSV files for expected date ranges, columns, and record counts before using them in downstream analysis. <br>
Risk: The security verdict flags the release as suspicious and recommends review before installation. <br>
Mitigation: Review the skill carefully, install dependencies in an isolated environment, and use the skill only if the external data-service behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wang-junjian/stock-data-collector) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Quickstart guide](artifact/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown instructions with Python CLI commands; runtime scripts write UTF-8 CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to market-data providers and Python dependencies including akshare, yfinance, and pandas.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
