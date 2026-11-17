## Description:

Data Analyzer helps analyze CSV, Excel, and JSON datasets with basic statistics, optional group-by summaries, and HTML or JSON reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinanping-cpu](https://clawhub.ai/user/yinanping-cpu)

### License/Terms of Use:


## Use Case:

Developers, analysts, and sellers use this skill to summarize local CSV, Excel, or JSON datasets, run basic statistics and group-by analysis, and produce HTML or JSON reports for sales or e-commerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML reports may include values from input datasets and are best suited to trusted data.

Mitigation: Use trusted datasets for HTML output, prefer JSON for untrusted inputs, and review generated reports before sharing.

Risk: The output path is user supplied and may create or overwrite files.

Mitigation: Choose output filenames and directories carefully before running the analyzer.

Risk: Some advertised analytics features and helper scripts are not included in the artifact.

Mitigation: Rely on the included scripts/analyze_data.py workflow and verify any additional documented examples before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinanping-cpu/skills/yinan-data-analyzer)
- [Taobao Seller Center](https://myseller.taobao.com/home.htm/QnworkbenchHome/)
- [Douyin Seller Center](https://fxg.jinritemai.com/ffa/mshop/homepage/index?channel=zhaoshang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated reports are HTML or JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local CSV, Excel, or JSON input files. The optional pandas dependency enables Excel support and richer statistics.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
