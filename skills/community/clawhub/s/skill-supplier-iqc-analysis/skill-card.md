## Description:

企业SQE供应商来料质量分析工具；当用户需要分析IQC来料检验数据、供应商质量对标、生成质量报告时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Supplier quality engineers use this skill to analyze IQC Excel workbooks, compare supplier quality performance, calculate defect metrics, assign risk grades, and generate supplier-facing quality reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can execute spreadsheet-supplied markup.

Mitigation: Prefer Markdown output or sanitize workbook-derived fields before opening or sharing HTML reports; open generated HTML cautiously.

Risk: The report filename prefix can write outside the intended output folder.

Mitigation: Use a controlled output directory and a simple filename prefix without path separators.

Risk: The skill processes supplier or other untrusted workbooks.

Mitigation: Review the skill before installation and run workbook processing in a controlled environment.

## Reference(s):

- [Data schema and field mapping](references/data-schema.md)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-supplier-iqc-analysis)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-supplier-iqc-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON analysis output, and generated Markdown/HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes user-provided Excel workbooks and writes timestamped report files to a chosen output directory.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
