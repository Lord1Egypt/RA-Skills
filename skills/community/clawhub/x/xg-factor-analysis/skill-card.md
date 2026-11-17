## Description:

小果量化因子分析系统助手 helps agents guide quantitative factor researchers through factor data cleaning, IC analysis, layered returns, long-short evaluation, turnover analysis, Fama-MacBeth regression, visualization, and composite factor scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative researchers, and strategy analysts use this skill to evaluate stock factors, prepare factor and price data, run Alphalens-style diagnostics, and interpret generated metrics, charts, and optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and notebook-style examples may affect the user's Python environment.

Mitigation: Install and run the skill in an isolated virtual environment with reviewed, pinned dependencies.

Risk: Market-data examples may contact xtdata or yfinance providers and depend on third-party data availability and terms.

Mitigation: Run data-fetching examples only when external data access is intended and permitted.

Risk: Generated factor or trading signals can be mistaken for investment instructions.

Mitigation: Treat outputs as research artifacts and require human quantitative review before any trading or portfolio decision.

Risk: Force-recalculation workflows can overwrite local factor-output files.

Mitigation: Review output paths and back up local analysis files before enabling force recalculation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li152/skills/xg-factor-analysis)
- [Alphalens overview example](references/alphalens/examples/overview.txt)
- [xg_alphalens implementation reference](references/xg_alphalens/xg_alphalens.py)
- [Factor catalog](assets/因子表.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; execution examples may create local analysis data, charts, and reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are research artifacts and should be reviewed before use in trading or investment decisions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
