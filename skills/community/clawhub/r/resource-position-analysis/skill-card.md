## Description: <br>
Analyzes frontend resource-position conversion funnel data, decomposes exposure, CTR, and CVR fluctuations with the Sequential Substitution method, and generates Markdown findings and recommendations across day-over-day, week-over-week, or custom comparison periods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyi-ding](https://clawhub.ai/user/wuyi-ding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and operations teams use this skill to run local Excel-based conversion funnel attribution for banners, cards, popups, and other frontend resource positions. It helps compare periods, identify the main drivers behind conversion changes, and draft operational recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The analysis script may install missing Python dependencies at runtime. <br>
Mitigation: Run it in a virtual environment and consider installing reviewed versions of pandas and openpyxl before execution. <br>
Risk: Excel inputs may contain sensitive business metrics. <br>
Mitigation: Use approved local data-handling practices and verify that files are appropriate for local processing before running the script. <br>
Risk: Attribution and recommendations can be misleading if the input columns, date ranges, or funnel assumptions are wrong. <br>
Mitigation: Review the input schema, comparison periods, and generated findings before using the report for operational decisions. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [report-template.md](report-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wuyi-ding/resource-position-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables, factor contribution analysis, key findings, and prioritized recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local Excel input and may write the generated report to a user-specified Markdown file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
