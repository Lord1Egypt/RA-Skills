## Description: <br>
Financial and operational KPI research for US public companies using Revelata deepKPI, including SEC-derived KPI retrieval, filing excerpts, implied metrics, seasonality analysis, peer benchmarks, analyst-report pressure tests, and Excel exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjt-at-revelata](https://clawhub.ai/user/sjt-at-revelata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agent developers use this skill to pull and analyze US public-company KPI data from Revelata deepKPI, inspect SEC filing markdown, benchmark peers, pressure-test analyst reports, and produce spreadsheet or HTML research artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends company, KPI, filing, and related research queries to Revelata deepKPI and requires a DEEPKPI_API_KEY for REST access. <br>
Mitigation: Install only when Revelata deepKPI is intended, use a dedicated API key where possible, and monitor credit usage. <br>
Risk: Uploaded analyst reports or sensitive research context may be reflected in local HTML or spreadsheet outputs. <br>
Mitigation: Avoid uploading sensitive reports unless the user is comfortable with local artifact creation and related deepKPI queries. <br>
Risk: Financial outputs can mislead if figures lack source traceability or derived values are not clearly identified. <br>
Mitigation: Review outputs before relying on them and require clickable deepKPI provenance links for reported numbers, including operands for derived metrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sjt-at-revelata/revelata-deepkpi) <br>
- [Revelata](https://www.revelata.com) <br>
- [deepKPI REST access](deepkpi-api/deepkpi-api.md) <br>
- [KPI retrieval workflow](retrieve-kpi-data/retrieve-kpi-data.md) <br>
- [SEC filing markdown workflow](retrieve-sec-filing/retrieve-sec-filing.md) <br>
- [Excel export format](format-deepkpi-for-excel/format-deepkpi-for-excel.md) <br>
- [Analyst report pressure test workflow](analyst-report-pressure-test/analyst-report-pressure-test.md) <br>
- [Pressure-test HTML template](analyst-report-pressure-test/references/html-template.md) <br>
- [Pressure-test chart patterns](analyst-report-pressure-test/references/chart-patterns.md) <br>
- [Peer benchmark HTML template](peer-benchmark/references/html-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown responses, API request examples, shell command snippets, HTML reports, and Excel workbook files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve deepKPI provenance links for reported numbers and may require DEEPKPI_API_KEY plus curl when using REST access.] <br>

## Skill Version(s): <br>
1.0.21 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
