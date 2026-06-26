## Description: <br>
Enterprise-grade data analysis assistant that cleans, analyzes, and visualizes CSV, Excel, JSON, and TSV data and generates summaries, charts, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyandong8](https://clawhub.ai/user/wuyandong8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and business analysts use this skill to inspect tabular data, clean data quality issues, produce statistical summaries, generate charts, and create Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated summaries, charts, cleaned CSVs, and reports may contain sensitive source data. <br>
Mitigation: Review outputs before sharing and keep confidential datasets in approved local or protected storage. <br>
Risk: The install script installs Python dependencies and changes executable permissions. <br>
Mitigation: Install in a virtual environment when possible and review install.sh before running it. <br>
Risk: Example workflows mention email, cloud-upload, or curl-style data movement that could expose confidential data if copied without review. <br>
Mitigation: Do not use external transfer examples with confidential data or untrusted sources without approval. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/wuyandong8/smart-data-insights) <br>
- [Data Cleaning Reference](references/data_cleaning.md) <br>
- [Data Analysis Reference](references/data_analysis.md) <br>
- [Visualization Reference](references/visualization.md) <br>
- [Report Generation Reference](references/report_generation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON summaries, CSV files, PNG charts, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written locally and may contain sensitive information from the source dataset.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
