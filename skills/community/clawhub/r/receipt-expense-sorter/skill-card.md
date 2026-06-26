## Description: <br>
Organizes receipts and expense records by period, category, and receipt completeness, and highlights missing documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, finance operations teams, and administrators use this skill to prepare reimbursement packets, archive expense materials, and coordinate review by turning receipt lists with dates, amounts, and categories into structured Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt and expense materials may contain personal or financial information. <br>
Mitigation: Provide only files or text intended for processing, redact sensitive details where practical, and review the generated Markdown before saving or sharing it. <br>
Risk: Generated reimbursement organization may be incomplete or unsuitable for a formal finance workflow. <br>
Mitigation: Treat outputs as review drafts and reminders, verify missing items against the source materials, and use the appropriate reimbursement system for final submission. <br>
Risk: The optional local Python helper reads input files and can write an output file. <br>
Mitigation: Run it only on intended local materials and use dry-run or stdout output when checking results before writing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/receipt-expense-sorter) <br>
- [README.md](artifact/README.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>
- [resources/template.md](artifact/resources/template.md) <br>
- [examples/example-output.md](artifact/examples/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Structured Markdown or JSON, with optional local Python command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include period grouping, category grouping, missing document reminders, naming suggestions, submission order, notes, and items needing confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
