## Description:

Research A-share stocks with fundamental and technical analysis, multi-factor scoring, daily reports, and quantitative recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-research users use this skill to analyze A-share and HS300 stocks, generate ranked stock reports, and summarize technical, fundamental, fund-flow, volume, and news factors. Outputs are for research support and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically requests market data from third-party services.

Mitigation: Review external data-source use before installation and run only in environments where those network requests are acceptable.

Risk: Python dependencies are not pinned.

Mitigation: Install and execute the scripts in a virtual environment with reviewed dependency versions.

Risk: Reports and logs may be written to fixed local paths or the current workspace.

Mitigation: Adjust output paths before execution and run the skill in a workspace where generated files are expected.

Risk: Stock rankings and position suggestions may be incorrect or stale.

Mitigation: Treat outputs as research support only and verify recommendations against current market data and qualified financial judgment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/stock-research)
- [Artifact skill documentation](artifact/SKILL.md)
- [Sample analysis result](artifact/analysis_result.json)
- [Sample weekly report](artifact/weekly_report.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text guidance with Python commands and JSON/report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create analysis_result.json, quant_result.json, weekly_report.txt, and task-summary records when scripts are executed.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact package metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
