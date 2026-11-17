## Description:

基于 COSMIC 标准的工作量拆分工作流，将需求文档拆解为功能点与 E/R/W/X 数据移动明细，并生成拆解表格和 CSV 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wed840313](https://clawhub.ai/user/wed840313)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, product teams, and implementation engineers use this skill to turn Markdown or DOCX requirements documents into COSMIC CFP decomposition artifacts for review and estimation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied requirement document paths may be passed into shell commands during workspace preparation and CSV export.

Mitigation: Run the skill only in a restricted workspace, avoid paths or filenames containing shell metacharacters, and prefer a patched release that uses safe filesystem APIs for path handling.

Risk: Generated CSV files may reflect untrusted or malformed requirement content.

Mitigation: Review generated CSV files before opening them in spreadsheet software or sharing them downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wed840313/skills/wenwei-cosmic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown decomposition documents, progress text, shell commands, and CSV export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces requirements discovery and COSMIC decomposition Markdown files, then exports reviewed decomposition tables to UTF-8 BOM CSV.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
