## Description:

Create and troubleshoot Excel reporting workbooks with charts, dashboards, conditional formatting, print areas, PDF or image export, openpyxl or Office automation, and recurring data refresh while preserving workbook layout, formulas, and presentation-ready output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, finance teams, operations teams, and developers use this skill to build or repair recurring Excel reports that combine data sheets, formulas, charts, dashboards, print setup, and export workflows. It helps agents plan workbook architecture, produce implementation steps or code, and validate formulas, chart ranges, formatting, and exported output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workbook scripts may modify sensitive finance or operations files, especially during data refresh, desktop Excel automation, or PDF export workflows.

Mitigation: Review generated scripts before execution, run them on copies of workbooks, and validate source timestamps, row counts, totals, formulas, and exports before replacing production files.

Risk: Excel desktop automation and PDF or image exports can vary by local Excel version, fonts, printer settings, and operating environment.

Mitigation: Inspect exported files for clipping, missing labels, font substitution, page breaks, margins, orientation, and print-area accuracy before distribution.

Risk: Editing workbook packages or unsupported workbook parts can break templates, chart objects, cached chart data, or formulas.

Mitigation: Preserve template backups, prefer Excel Tables and named ranges, and re-check formulas, chart series references, conditional-format ranges, and cached chart behavior after changes.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [Skill README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-excel-chart-developer-helper-180322)
- [openpyxl Basic Operations Evidence](https://segmentfault.com/a/1190000018500569)
- [Conditional Formatting Evidence](https://segmentfault.com/t/conditional-formatting)
- [Excel-like Controls Evidence](https://segmentfault.com/q/1010000014786828/a-1020000014787108)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with implementation steps, code snippets, checklists, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workbook architecture, repair diagnosis, automation guidance, and export validation checks.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
