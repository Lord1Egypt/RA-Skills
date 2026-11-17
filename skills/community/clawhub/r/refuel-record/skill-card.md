## Description:

达鑫车队加气记录录入技能。触发指令：「加气汇总」。当用户提供加气原始信息（日期、车牌、站点、升数、单价、金额、公里数）时，自动生成加气记录汇总表和扣卡记录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[v31981](https://clawhub.ai/user/v31981)

### License/Terms of Use:

MIT-0

## Use Case:

Fleet operations or administrative users use this skill to turn raw Chinese refueling entries into a CSV summary with a main refueling table and deduction-card records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fleet and payment reports may be written to a fixed Windows Desktop path without a user-selected destination.

Mitigation: Confirm the output location before use or modify the workflow to request an output folder.

Risk: Repeated runs may overwrite reports or make it hard to distinguish generated files.

Mitigation: Use unique filenames and add overwrite confirmation before saving generated CSV files.

Risk: Spreadsheet fields from untrusted records could trigger CSV formula injection.

Mitigation: Neutralize exported fields that begin with =, +, -, or @ before opening the CSV in spreadsheet software.

## Reference(s):

- [加气记录格式参考](references/format-examples.md)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [CSV file with Chinese-language refueling and deduction-card tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact instructs the agent to save 加气汇总_YYYY-MM-DD.csv to C:\Users\35794\Desktop.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
