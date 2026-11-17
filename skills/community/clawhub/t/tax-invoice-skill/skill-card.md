## Description:

本技能在本地使用 OCR 和本地多模态模型辅助定位字段，从图片或 PDF 发票中抽取票面信息并生成月度报销台账。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent-chao-lang](https://clawhub.ai/user/vincent-chao-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Small-business finance users and agent workflows use this skill to process user-selected invoice folders, extract invoice fields, classify invoice types, flag exceptions, and build a monthly tax ledger for reimbursement and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive financial documents and the local-only network boundary is not enforced by policy controls.

Mitigation: Run it only in an isolated virtual environment, keep OLLAMA_API fixed to a loopback Ollama endpoint, and avoid proxy inheritance.

Risk: Spreadsheet output handling may allow unsafe formulas or cell content from invoice data.

Mitigation: Do not process invoices from untrusted sources until spreadsheet formula sanitization is added and reviewed.

Risk: Runtime dependencies are not locked to exact versions.

Mitigation: Pin and review dependencies before deployment, then install from a controlled package source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincent-chao-lang/skills/tax-invoice-skill)
- [Publisher profile](https://clawhub.ai/user/vincent-chao-lang)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Text guidance with shell commands; generated Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a monthly ledger workbook and an exception sheet in the user-provided invoice directory.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
