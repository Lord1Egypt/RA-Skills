## Description: <br>
计算两个表格之间的 Spearman 相关性，并输出 FDR 校正后的结果。适用于微生物组数据（如 Family 丰度表与环境因子/功能基因表）的相关性分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zd200572](https://clawhub.ai/user/zd200572) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to run Spearman correlation analysis between paired tabular datasets, especially microbiome abundance tables and environmental or functional-gene tables. It supports single-file and batch folder workflows, applies Benjamini-Hochberg FDR correction, and summarizes significant positive and negative associations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected tables or folders and creates Excel result files. <br>
Mitigation: Run it only on intended input paths, use a trusted Python environment, and confirm output locations before batch runs. <br>
Risk: Batch output may overwrite existing analysis files if paths are reused. <br>
Mitigation: Choose a dedicated output directory or review filenames before writing results. <br>
Risk: Small sample sizes or constant feature rows can produce unstable correlations or NaN values. <br>
Mitigation: Review sample counts and NaN outputs before interpreting significant associations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zd200572/spearman-correlation) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, files, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown summary plus Excel (.xlsx) result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Excel workbooks contain correlation, pvalue, and FDR worksheets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
