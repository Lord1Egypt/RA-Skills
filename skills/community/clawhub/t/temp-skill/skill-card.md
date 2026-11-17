## Description:

Provides multi-asset portfolio analysis with rolling-window risk-parity rebalancing, backtesting, and chart and report generation from local CSV market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzratgit](https://clawhub.ai/user/wzratgit)

### License/Terms of Use:

MIT

## Use Case:

Developers, financial analysts, and portfolio researchers use this skill to run local risk-parity portfolio backtests, inspect return and risk metrics, and produce supporting reports and visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions may affect reproducibility of portfolio calculations and generated charts.

Mitigation: Install the skill in an isolated Python environment and pin or review dependency versions before relying on repeated analyses.

Risk: API keys or local portfolio data may be exposed if stored in shared files or output locations.

Mitigation: Keep API keys out of shared files and write reports, JSON data, and charts to a controlled local directory.

Risk: Generated reports may contain local file paths and portfolio analysis data.

Mitigation: Review generated artifacts before sharing them outside the intended workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzratgit/skills/temp-skill)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Optimization usage guide](artifact/优化使用指南.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated text reports, JSON data, PNG charts, and console summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes analysis artifacts to a user-selected local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
