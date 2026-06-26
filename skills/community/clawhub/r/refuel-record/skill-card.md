## Description: <br>
达鑫车队加气记录录入技能：当用户提供日期、车牌、站点、升数、单价、金额和公里数等原始加气信息时，生成加气记录汇总表和扣卡记录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[V31981](https://clawhub.ai/user/V31981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fleet operations and accounting users can use this skill to convert raw vehicle refueling messages into a standardized refueling CSV and matching card-deduction accounting records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves generated CSV files to a fixed Desktop path and the files may contain sensitive fleet refueling and accounting records. <br>
Mitigation: Confirm the save location before use and handle generated CSV files as sensitive business records. <br>


## Reference(s): <br>
- [加气记录格式参考](references/format-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [CSV file with refueling summary and card-deduction records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output as 加气汇总_YYYY-MM-DD.csv and uses the documented field order for both tables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
