## Description:

Quant Buddy Skill helps agents query A-share, Hong Kong, and U.S. market data, A-share financial metrics, recent trading-window statistics, screening results, factor calculations, backtests, industry aggregations, uploaded factor CSVs, and rendered charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pseudo-longinus](https://clawhub.ai/user/pseudo-longinus)

### License/Terms of Use:

MIT-0

## Use Case:

External users, market analysts, and agents use this skill to retrieve financial market data, compare recent performance, run quantitative finance workflows, and produce charts or exported datasets for research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive user queries may be sent during session setup or finance workflow execution.

Mitigation: Use the skill only where Quant Buddy service use is approved, and avoid entering unnecessary confidential details in prompts.

Risk: API keys may be stored locally and used for outbound requests.

Mitigation: Use limited-scope credentials where available, keep keys out of chat transcripts, and restrict endpoints to the intended Quant Buddy host.

Risk: Local logs, cache entries, session files, charts, CSVs, and other outputs may retain queried data.

Mitigation: Review retention expectations, redact or disable logs where possible, and clear local output or cache files after sensitive work.

Risk: CSV uploads and optional news-search workflows may send user-provided data or requests to external services.

Mitigation: Upload only approved datasets and enable the optional Bocha integration only when that service is permitted for the deployment.

Risk: Zip-based skill update behavior can replace local skill files if handled without verification.

Mitigation: Allow update workflows only for trusted administrators and verify package provenance and contents before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pseudo-longinus/skills/quant-buddy-skill)
- [Publisher profile](https://clawhub.ai/user/pseudo-longinus)
- [Quant Buddy skill API endpoint](https://www.quantbuddy.cn/skill)
- [Quant Buddy user API endpoint](https://www.quantbuddy.cn/user)
- [Quant Buddy API key login](https://www.quantbuddy.cn/login)
- [Bocha optional API key service](https://open.bochaai.com)
- [Environment](references/environment.md)
- [RU Billing](references/ru-billing.md)
- [Troubleshooting](references/troubleshooting.md)
- [Scripts Audit](references/scripts-audit.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown responses with tables, formulas, tool-call parameters, and saved CSV or PNG files when download or chart workflows are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a required Quant Buddy API key and optional Bocha API key; workflows can retain local session, cache, chart, and data files under the skill output paths.]

## Skill Version(s):

4.14.18 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
