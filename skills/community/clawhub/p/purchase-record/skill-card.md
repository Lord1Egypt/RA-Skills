## Description: <br>
Parses Chinese purchase commands and records the date, item name, and price into a local Excel purchase workbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbei2007](https://clawhub.ai/user/linbei2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who keep purchase logs use this skill to convert commands such as '采购 0312 螺丝 3 元' into structured purchase records. The skill is intended for simple local bookkeeping workflows that append date, item, and price fields to an Excel workbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs purchase text through a shell command before recording it. <br>
Mitigation: Replace shell-based execution with spawn or execFile argument arrays before using the skill with real records. <br>
Risk: The skill automatically modifies a local Excel workbook when a matching purchase command is issued. <br>
Mitigation: Add a confirmation or preview step and make the workbook path configurable before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbei2007/purchase-record) <br>
- [Publisher profile](https://clawhub.ai/user/linbei2007) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files] <br>
**Output Format:** [Markdown confirmation text plus appended Excel workbook rows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes date, item name, and price fields to purchase_record.xlsx when a matching purchase command is issued.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
