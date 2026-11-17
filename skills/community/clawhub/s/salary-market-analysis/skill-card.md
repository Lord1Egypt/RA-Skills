## Description:

Salary Market Analysis helps agents collect and normalize salary-market data, calculate annualized percentile benchmarks, and generate compensation reports in multiple formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

HR, compensation, recruiting, and people-analytics teams use this skill to benchmark market compensation for target roles and regions. Analysts and developers can run its Python utilities to clean salary CSV data, combine sources, calculate percentiles, and generate report artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted CSV values can be preserved as spreadsheet formulas when exported to Excel.

Mitigation: Use trusted or sanitized CSV inputs and neutralize formula-leading characters before Excel export.

Risk: Automated salary-data collection can conflict with website terms, robots policies, privacy obligations, or data-minimization requirements.

Mitigation: Confirm permission and applicable terms before collection, prefer manual or approved data sources, and keep automated collection rate-limited and scoped to necessary fields.

Risk: Salary benchmarks can be misleading when samples are small, stale, regionally narrow, or mixed across inconsistent compensation definitions.

Mitigation: Review sample size, source quality, collection date, geography, and compensation assumptions before relying on generated benchmark reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tuobadaidai/skills/salary-market-analysis)
- [Skill Documentation](artifact/SKILL.md)
- [Data Collection Guide](artifact/references/data-collection-guide.md)
- [Global Data Sources](artifact/references/global-data-sources.md)
- [Report Template](artifact/references/report-template.md)
- [Salary Methodology](artifact/references/salary-methodology.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and generated CSV, JSON, Excel, Word, and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; optional SALARY_DATA_DIR can point to a custom data directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
