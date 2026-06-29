## Description: <br>
AI销量预测助手基于 Amazon Chronos-2 (120M) 零样本时序模型，从历史销售数据（CSV/Excel）生成多分位数概率预测、置信区间和交互式 HTML 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to forecast future sales or time-series trends from historical sales files and generate probabilistic outputs with an HTML visualization report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download Python dependencies and the Chronos model from PyPI, HuggingFace, or a configured mirror during setup or first use. <br>
Mitigation: Confirm outbound download policy before installation and use approved mirrors, cached packages, or pre-vetted model artifacts in controlled environments. <br>
Risk: Sales input files may contain sensitive business data. <br>
Mitigation: Run the skill only in approved environments and apply internal data handling controls to input files, generated forecast data, and HTML reports. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/bettermen/sales-forecast) <br>
- [ClawHub release page](https://clawhub.ai/bettermen/sales-forecast-pkg) <br>
- [HuggingFace mirror endpoint](https://hf-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated forecast data and HTML reports when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports CSV, Excel, JSON, and Parquet inputs; default forecast output includes 0.1, 0.5, and 0.9 quantiles.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
