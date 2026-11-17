## Description:

根据指定账期的招商银行活期、理财及对公账户源数据生成包含明细和资金汇总的标准化交易记录 Excel 文件，并可从交易记录生成账目 Excel 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[courage-zen](https://clawhub.ai/user/courage-zen)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations users use this skill to transform monthly bank exports into standardized transaction and accounting workbooks for review, reconciliation, and archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill rewrites source CSV data during preprocessing, which can compromise original bank exports used as audit records.

Mitigation: Run the skill only on working copies and keep untouched backups of all original bank exports.

Risk: Formula-like text from untrusted spreadsheet inputs may be carried into generated workbooks.

Mitigation: Inspect generated workbooks before opening or sharing them, and add formula sanitization before routine use with untrusted inputs.

Risk: Unpinned Python dependencies can change parsing or workbook behavior over time.

Mitigation: Pin and review dependencies such as openpyxl and xlrd before regular operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/courage-zen/skills/transaction-records-cn)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces period-specific .xlsx workbooks such as transaction records and accounting ledgers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
