## Description:

从测试执行结果、日志文件或测试框架输出中自动生成专业的测试分析报告，支持 Allure、Pytest、Jest、JUnit 等多种格式，并可导出 HTML、PDF、Excel 或 Markdown 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shylamb-token](https://clawhub.ai/user/shylamb-token)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and release teams use this skill to turn test framework outputs, logs, or manually supplied test data into readable quality reports with pass-rate statistics, failure analysis, trend summaries, and exportable dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute injected JavaScript or unsafe markup from untrusted test names, logs, or error messages.

Mitigation: Escape all HTML and JavaScript-bound values before writing reports, and review generated HTML before opening it in a browser.

Risk: Generated Excel reports may preserve spreadsheet formulas supplied through test data.

Mitigation: Neutralize cells that begin with formula-triggering characters before writing workbooks.

Risk: The sample HTML exporter references a third-party Chart.js CDN script.

Mitigation: Pin or bundle chart dependencies before using generated reports in controlled or offline environments.

Risk: Report output paths could overwrite unintended files if filenames are taken directly from user input.

Mitigation: Choose explicit report filenames inside a workspace report directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shylamb-token/skills/smart-test-report)
- [Publisher profile](https://clawhub.ai/user/shylamb-token)
- [Chart.js CDN dependency referenced by sample HTML exporter](https://cdn.jsdelivr.net/npm/chart.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance and report content, with generated Python exporter code and report files such as HTML, PDF, Excel, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes user-provided test results, logs, or manual test data and may generate browser- or spreadsheet-opened report artifacts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
