## Description: <br>
Query TradingView screener data for HK, A-share, A-share ETF, and US symbols using deepentropy/tvscreener for stock lookups, technical indicators, symbol filters, and custom market queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Subway-chenyan](https://clawhub.ai/user/Subway-chenyan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and market analysts use this skill to build TradingView screener queries and retrieve JSON or CSV snapshots for stocks, ETFs, and technical indicators across supported markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell wrappers may install or upgrade an unpinned tvscreener dependency. <br>
Mitigation: Use a virtual environment and review or pin the tvscreener dependency before running wrapper scripts. <br>
Risk: Optional CSV exports write to user-selected paths and may overwrite important files. <br>
Mitigation: Choose output paths deliberately and avoid writing CSV results over existing critical files. <br>
Risk: Some interval field combinations may fail with FieldWithInterval errors in certain tvscreener versions. <br>
Mitigation: Use base daily fields or the single-symbol query script when interval fields fail. <br>


## Reference(s): <br>
- [README_USAGE](references/README_USAGE.md) <br>
- [Screeners API Reference](references/api/screeners.md) <br>
- [Fields API Reference](references/api/fields.md) <br>
- [Filters API Reference](references/api/filters.md) <br>
- [Enums API Reference](references/api/enums.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python snippets, plus JSON or CSV data from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts require Python 3.10+ and can write optional CSV files to user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
