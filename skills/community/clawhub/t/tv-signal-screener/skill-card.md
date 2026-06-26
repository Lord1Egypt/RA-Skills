## Description: <br>
Screen markets across 6 asset classes using TradingView data with API pre-filters, pandas computed signals, and YAML-driven strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NomadRex](https://clawhub.ai/user/NomadRex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to run TradingView-backed market screens across stocks, crypto, forex, bonds, futures, and coins, then review results as Markdown tables. It supports one-time filters and reusable YAML signal definitions for technical screening workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs Python packages into a local virtual environment. <br>
Mitigation: Install only in trusted workspaces and consider pinning dependencies before use in sensitive or reproducible environments. <br>
Risk: The skill contacts TradingView-related market data services and screening results may be incomplete, delayed, or unsuitable for financial decisions. <br>
Mitigation: Use outputs as screening signals only, verify important findings independently, and avoid treating them as trading or investment advice. <br>
Risk: Custom signal YAML can change filter behavior and computed expressions. <br>
Mitigation: Use trusted signal files and review YAML definitions before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/NomadRex/tv-signal-screener) <br>
- [TradingView Screener API Guide](references/tvscreener-api-guide.md) <br>
- [Computed Signals Guide](references/computed-signals-guide.md) <br>
- [Strategy Templates](references/strategy-templates.md) <br>
- [Field Presets](references/field-presets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables, CLI text output, and YAML signal configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on TradingView market data availability and the selected filters, columns, timeframe, and signal YAML.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
