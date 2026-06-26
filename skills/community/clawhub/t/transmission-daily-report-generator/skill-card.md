## Description: <br>
生成传输单边故障日报报表，按考核周期统计，包含原始清单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wede375](https://clawhub.ai/user/wede375) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and network-reporting teams use this skill to turn local Excel fault data into assessment-period daily reports with annual totals, per-period sheets, timeout metrics, and a preserved raw-data sheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated workbook intentionally includes the complete raw source dataset, not only aggregate statistics. <br>
Mitigation: Treat generated workbooks as sensitive and restrict sharing, storage, and retention according to the source data's handling requirements. <br>
Risk: The workflow is specific to a local Excel fault-report process with configured input and output paths. <br>
Mitigation: Review and update the input and output paths before running the script on a new workstation or dataset. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wede375/transmission-daily-report-generator) <br>
- [Usage guide](artifact/references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated Excel workbook (.xlsx)] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated workbook includes summary sheets and a full raw-data sheet.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
