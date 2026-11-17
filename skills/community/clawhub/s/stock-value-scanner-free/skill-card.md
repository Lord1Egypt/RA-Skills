## Description:

Scans 11 U.S. stocks for pullback and value-style signals using five technical factors, then returns scores, action labels, and recent backtest examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to screen a fixed watchlist of U.S. stocks for technical pullback signals and JSON-formatted action labels. It supports market monitoring workflows, not standalone investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market scores and buy, watch, or hold labels could be mistaken for financial advice.

Mitigation: Treat outputs as informational screening signals only, review the underlying market data and assumptions, and require independent investment analysis before acting.

Risk: The skill describes daily automatic backtest behavior, which may create recurring activity in the host environment.

Mitigation: Confirm whether the installed skill creates a schedule, and keep the schedule disabled or explicitly controlled unless recurring runs are intended.

Risk: Signals depend on a fixed watchlist and Yahoo Finance data, so coverage or data availability may be incomplete.

Mitigation: Validate symbols, prices, and results against another market data source before using the output in decision workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/skills/stock-value-scanner-free)
- [ClawHub publisher profile](https://clawhub.ai/user/sg345662365-oss)
- [Repository declared in skill metadata](https://github.com/sgready/vane-signals)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown usage guidance with shell command snippets and JSON signal objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs fixed-watchlist stock scores and action labels based on Yahoo Finance data; no API key is described.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
