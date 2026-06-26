## Description: <br>
Xihu Hiring fetches Feishu approval data for the Xihu Digital HR hiring template and generates a three-sheet recruiting progress Excel report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyqqj0](https://clawhub.ai/user/tyqqj0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized HR and recruiting operators use this skill to refresh a Xihu Digital hiring tracker from Feishu approvals, apply manual corrections, and produce an Excel report for applicant pipeline review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bulk-accesses and locally stores sensitive candidate information in Excel and temporary payload files. <br>
Mitigation: Install only for authorized HR or recruiting operators, run it in a private workspace, confirm the output directory, treat generated files as sensitive applicant data, and delete temporary payload files after report generation. <br>
Risk: The skill depends on Feishu approval access and a lark-cli bot context, so overbroad permissions could expose unrelated approval data. <br>
Mitigation: Use the correct Feishu bot permissions for the documented HR approval template and review access before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tyqqj0/xihu-hiring) <br>
- [Publisher profile](https://clawhub.ai/user/tyqqj0) <br>
- [Fetch approvals reference](artifact/references/fetch-approvals.md) <br>
- [Build Excel reference](artifact/references/build-excel.md) <br>
- [Normalization rules](artifact/references/normalization-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash and Python commands, JSON payloads, JSON summary output, and a generated Excel workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates 西湖数智-招聘进度.xlsx in the current workspace and may use /tmp/hiring_payload.json as an intermediate payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
