## Description:

vbt-report generates VectorBT-based HTML backtesting reports for A-share stocks in single-stock or batch modes, with interactive charts, strategy rankings, and a searchable batch index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotuspaladin-lab](https://clawhub.ai/user/lotuspaladin-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative analysts use this skill to run A-share technical-strategy backtests from local or fetched market data and produce interactive HTML reports for review. The reports summarize indicators, strategy performance, drawdown, rankings, and batch-level filtering results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted stock data or names could execute browser code in generated HTML reports or batch index pages.

Mitigation: Run the skill only on trusted stock lists, keep generated reports in a dedicated location, and add HTML escaping before production use.

Risk: Unsafe filename handling could write reports outside the intended output folder.

Mitigation: Use an isolated output directory, avoid privileged paths, and sanitize filenames derived from stock names before production use.

Risk: Generated reports may load Plotly from a CDN and should not be served from an authenticated or privileged web origin.

Mitigation: Use offline Plotly bundling or review the hosting context before sharing generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lotuspaladin-lab/skills/vbt-report)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with command examples; generated HTML report files and index pages when scripts are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stock mode writes one HTML report; batch mode writes per-stock reports plus an index.html summary.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
