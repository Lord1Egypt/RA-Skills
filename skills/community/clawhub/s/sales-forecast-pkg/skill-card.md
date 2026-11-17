## Description:

AI销量预测助手。基于 Amazon Chronos-2 (120M) 零样本时序大模型，输入历史销量数据（CSV/Excel），自动生成多分位数概率预测、置信区间和交互式HTML可视化报告。当用户询问销量预测、销售预测、趋势预测、时序预测时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users use this skill to generate zero-shot sales and time-series forecasts from CSV or Excel history, including quantile predictions, confidence intervals, and an interactive HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package reviewed here includes only SKILL.md, while the documented workflow calls scripts that are not present in the artifact.

Mitigation: Confirm the actual forecasting and report-generation scripts, including their data-handling behavior, before using the skill on sensitive or production data.

Risk: The documented dependency installation does not pin Python package versions.

Mitigation: Install in an isolated virtual environment and pin reviewed dependency versions before operational use.

Risk: First use downloads a large external model from a configurable endpoint.

Mitigation: Review and approve the model endpoint and network access path before running the workflow in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/sales-forecast-pkg)
- [Project homepage](https://github.com/bettermen/sales-forecast)
- [Hugging Face mirror endpoint](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; the described workflow can produce JSON forecast data and an HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided sales or time-series files and configurable forecast horizon, quantiles, context length, and model endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
