## Description: <br>
Data Analyzer supports analysis and visualization of CSV, Excel, and JSON data for sales reports, charts, pivot-style summaries, statistical analysis, and automated reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinanping-CPU](https://clawhub.ai/user/yinanping-CPU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to inspect CSV, Excel, and JSON datasets, calculate summary statistics or grouped metrics, and generate HTML or JSON reports for sales and e-commerce workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports can include unescaped data values from input files. <br>
Mitigation: Prefer JSON output for untrusted datasets and treat generated HTML as unsafe until escaping is fixed or the report is reviewed in a controlled environment. <br>
Risk: The documentation references helper scripts that are not included in the artifact. <br>
Mitigation: Use the included scripts/analyze_data.py entry point rather than searching for or substituting missing helper scripts. <br>
Risk: Analyzing files from third parties or marketplaces may expose the user to unsafe or misleading input data. <br>
Mitigation: Review the skill before installing it for third-party data workflows and validate input files before generating reports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yinanping-CPU/yinan-data-analyzer) <br>
- [Taobao Seller Center](https://myseller.taobao.com/home.htm/QnworkbenchHome/) <br>
- [Douyin E-commerce Console](https://fxg.jinritemai.com/ffa/mshop/homepage/index?channel=zhaoshang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated reports may be HTML or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include local HTML or JSON report files generated from user-provided data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
