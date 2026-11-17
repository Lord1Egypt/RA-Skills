## Description:

Analyzes A-share stock PE and PB historical percentiles using BaoStock data to compare current valuation against 1-, 3-, 5-, and 10-year history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoyachao](https://clawhub.ai/user/caoyachao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up A-share stocks by name or code, retrieve public BaoStock valuation data, and generate PE/PB percentile analysis for valuation review. The results are informational and do not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation or unpinned packages could introduce supply-chain risk.

Mitigation: Install in an isolated Python environment and pin or review baostock, pandas, and numpy before running pip install.

Risk: The Python module export function writes local CSV and text summary files.

Mitigation: Use a safe local output filename and do not pass filenames from untrusted input.

Risk: Valuation reports could be mistaken for investment advice.

Mitigation: Present outputs as informational PE/PB percentile analysis only and keep the investment-risk disclaimer with generated reports.

## Reference(s):

- [BaoStock](http://www.baostock.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, console reports, CSV exports, text summaries, and Python dictionaries/DataFrames]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires baostock, pandas, and numpy; uses public BaoStock A-share valuation data and can export local CSV and text summary files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
