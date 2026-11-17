## Description:

Financial and operational KPI research for US public companies using Revelata deepKPI, including SEC metric retrieval, filing excerpts, derived KPI calculations, seasonality analysis, Excel exports, peer benchmarking, idea screening, and analyst-report pressure tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjt-at-revelata](https://clawhub.ai/user/sjt-at-revelata)

### License/Terms of Use:

MIT-0

## Use Case:

External users, financial analysts, investors, and developers use this skill to query Revelata deepKPI for SEC-backed KPI research on US public companies, including company KPI history, filing passages, peer benchmarks, analyst-report pressure tests, and Excel-ready analysis outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: REST fallback requires a Revelata deepKPI API key and sends company or KPI research queries to Revelata.

Mitigation: Configure the API key only in trusted environments and avoid placing secrets, non-public company information, or sensitive personal data in prompts.

Risk: Generated HTML reports may include Revelata branding, external setup links, and financial analysis intended for user review.

Mitigation: Review generated reports, source links, and branding before sharing them externally.

Risk: Financial outputs depend on deepKPI availability, authentication, credits, network access, and SEC-backed coverage.

Mitigation: If deepKPI access fails, stop and ask whether to proceed without deepKPI, and clearly label any alternate sources used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sjt-at-revelata/skills/revelata-deepkpi)
- [Revelata](https://www.revelata.com)
- [Revelata deepKPI API](https://deepkpi-api.revelata.com)
- [deepKPI Agents GitHub Reference](https://github.com/revelata/deepkpi-agents)
- [Analyst Report Pressure Test HTML Template](analyst-report-pressure-test/references/html-template.md)
- [Peer Benchmark HTML Template](peer-benchmark/references/html-template.md)
- [Chart Patterns Reference](analyst-report-pressure-test/references/chart-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files, API calls]

**Output Format:** [Markdown and text responses, curl commands, JSON API calls, HTML reports, and Excel workbook files depending on the workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [REST fallback requires DEEPKPI_API_KEY and curl; some workflows produce user-visible HTML reports with provenance links or .xlsx workbooks.]

## Skill Version(s):

1.0.21 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
