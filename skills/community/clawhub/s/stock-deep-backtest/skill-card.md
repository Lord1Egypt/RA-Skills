## Description:

Stock Deep Backtest helps agents diagnose completed QuantAll stock strategy backtests by attributing why a strategy worked or failed across summary, detail, segment, timeline, grouping, and entry-factor screening views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mifochen](https://clawhub.ai/user/mifochen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quant researchers, and agent users use this skill after a stock strategy backtest to inspect return drivers, style exposures, segment behavior, timeline effects, and whether entry-factor filters improve results. It supports diagnostic analysis and report generation, not standalone investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports hard-coded local WorkBuddy paths and the ability to read or write prior backtest artifacts without tight user-controlled scoping.

Mitigation: Run the skill in a scoped workspace, pass input files explicitly, and review or adjust hard-coded paths before executing scripts.

Risk: The security review warns that generated local HTML reports should not consume untrusted JSON without sanitization.

Mitigation: Use trusted local analysis inputs for report generation and review generated HTML before sharing or opening it in broader environments.

Risk: The artifact presents stock backtest diagnostics that can be mistaken for investment advice.

Mitigation: Treat outputs as analytical support only, verify conclusions against source data and independent review, and keep the included investment-disclaimer posture in public reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mifochen/skills/stock-deep-backtest)
- [Skill documentation](artifact/SKILL.md)
- [Task template README](artifact/tasks/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON task-file references and Python or shell command examples; included scripts may produce JSON, CSV, XLSX, and local HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local QuantAll market data and write local analysis reports or artifacts when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
