## Description: <br>
Generates structured A-share stock review reports for midday or full-day analysis, including scoring, technical analysis, fundamentals, market context, strategy notes, risk disclosures, and optional charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MartinYan623](https://clawhub.ai/user/MartinYan623) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to generate local Markdown A-share stock review reports for a named stock code, report type, and date. The reports follow a standardized structure for scoring, market analysis, strategy notes, and risk disclosures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local stock-analysis report and chart files in the OpenClaw workspace. <br>
Mitigation: Use ordinary stock names and codes, avoid path-like names, and review generated file paths before relying on the output. <br>
Risk: Generated reports may include buy, sell, position, or strategy suggestions. <br>
Mitigation: Treat all generated market guidance as informational only and review it with appropriate financial judgment before acting. <br>
Risk: Reports rely on public market data that may be delayed, incomplete, or inaccurate. <br>
Mitigation: Verify important prices, fundamentals, and market signals against official or trusted market data sources. <br>


## Reference(s): <br>
- [Stock Report Generator on ClawHub](https://clawhub.ai/MartinYan623/stock-report-generator) <br>
- [Scoring Guide](references/scoring_guide.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report files with optional PNG chart files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local report files in the OpenClaw workspace; full-day reports may include a matplotlib radar chart.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact _meta.json, and changelog released 2026-03-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
