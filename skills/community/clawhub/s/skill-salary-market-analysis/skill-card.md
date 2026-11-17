## Description:

薪酬市场调研分析技能（全球版）。支持国内+海外多源数据、28字段全球化模板、多币种自动换算（20+货币）、PPP购买力平价调整、分位值计算、17+章节专业报告、外派薪酬建议、多格式输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

HR, compensation, and talent teams use this skill to collect and normalize salary-market data across regions, calculate salary percentiles and currency or PPP adjustments, and produce compensation benchmarking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated or manual collection of salary data from websites can raise terms-of-use, privacy, or authorization issues.

Mitigation: Review website terms and privacy obligations before collection, and avoid collecting personal data unless authorized.

Risk: CSV or Excel outputs created from web-collected data can carry untrusted spreadsheet values.

Mitigation: Treat exported spreadsheet files as untrusted until formula-leading values are neutralized and reviewed.

Risk: Currency and PPP outputs depend on benchmark assumptions that may become stale or unsuitable for a specific compensation decision.

Mitigation: Review the exchange-rate date, PPP assumptions, data recency, and sample coverage before relying on generated salary guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/skill-salary-market-analysis)
- [Salary methodology](references/salary-methodology.md)
- [Global data sources](references/global-data-sources.md)
- [Data collection guide](references/data-collection-guide.md)
- [Report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON summaries, CSV or Excel-ready data, Word documents, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can depend on web-collected salary data, exchange-rate assumptions, PPP assumptions, and spreadsheet export handling.]

## Skill Version(s):

3.0.1 (source: server release metadata; artifact frontmatter is 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
