## Description: <br>
根据指定账期的招商银行活期、理财及对公账户源数据生成包含明细和资金汇总的标准化交易记录 Excel 文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[courage-zen](https://clawhub.ai/user/courage-zen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance or operations users can convert copied bank exports for a monthly accounting period into standardized transaction workbooks and optional ledger workbooks for review and archival workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The transaction-record script can rewrite the source checking-account CSV while cleaning it. <br>
Mitigation: Run the skill only on copied bank exports and keep untouched backups of original bank files. <br>
Risk: Generated workbooks may be used for accounting decisions even if source files, dates, balances, or formulas are wrong. <br>
Mitigation: Use restricted input and output folders, inspect generated workbooks, and reconcile outputs against source records before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/courage-zen/transaction-records-cn) <br>
- [Publisher profile](https://clawhub.ai/user/courage-zen) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [Excel workbooks (.xlsx) with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a YYYYMM accounting period and local bank export files; optional parameters select input/output folders, initial balance, and accounting date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
