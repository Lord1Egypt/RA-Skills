## Description: <br>
Comprehensive data analysis workflow for CSV files with interactive guidance and flexible output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users use this skill to inspect CSV datasets, choose cleaning strategies, generate exploratory analysis, and produce reports or dashboards with actionable recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python packages into the active Python environment. <br>
Mitigation: Run it in a sandbox or preinstall reviewed dependencies before use. <br>
Risk: The skill saves cleaned datasets, charts, reports, and dashboards, which may copy sensitive CSV content into new files. <br>
Mitigation: Use a controlled output directory and review generated files before sharing or retaining them. <br>
Risk: Interactive HTML output loads Chart.js and Tailwind CSS from third-party CDNs. <br>
Mitigation: Use Markdown output for sensitive datasets or replace CDN resources with reviewed local assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yz6214589-hash/yz6214589-hash-data-analysis) <br>
- [Chart.js CDN used for interactive reports](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js) <br>
- [Tailwind CSS CDN used for HTML reports](https://cdn.tailwindcss.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown report, interactive HTML report, dashboard files, PNG charts, cleaned CSV, and optional notebook code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write cleaned datasets, charts, reports, and dashboard assets to a timestamped data-analysis-results directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
