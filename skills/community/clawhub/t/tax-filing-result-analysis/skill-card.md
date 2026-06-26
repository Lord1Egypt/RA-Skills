## Description: <br>
分析Excel表中的申报失败信息，自动生成Word版本的申报运维报告，用于定位问题、统计趋势、提出整改建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houyalei](https://clawhub.ai/user/houyalei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and tax filing support teams use this skill to analyze Excel records of declaration failures, identify recurring causes and trends, and produce a Word operations report with remediation suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated Word report may contain sensitive operational or tax filing failure data. <br>
Mitigation: Process only approved Excel files in the local agent environment and handle the generated .docx report according to the organization's data handling rules. <br>
Risk: A chosen output_path may overwrite an existing report. <br>
Mitigation: Use a specific output_path and check whether the target file already exists before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/houyalei/tax-filing-result-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/houyalei) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance and local Word report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Simplified Chinese .docx report from a user-selected Excel file and prints the generated file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
