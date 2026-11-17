## Description:

中文论文格式检查工具，解析学校模板 DOCX、提取格式规则，并对比论文生成差异报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeyeeyeeee](https://clawhub.ai/user/yeyeeyeeee)

### License/Terms of Use:

MIT-0

## Use Case:

Students, academic writers, and agents assisting them use this skill to check Chinese thesis DOCX formatting against a school template and produce reviewable difference and risk reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing DOCX files from untrusted sources can expose the local parser and file system workflow to unsafe or malformed input.

Mitigation: Use the skill on documents you trust, and run it in a constrained environment when processing DOCX files from other people.

Risk: Generated reports or formatted DOCX outputs may miss issues or contain formatting guidance that still needs academic review.

Mitigation: Review generated reports and any formatted outputs before submitting academic work.

Risk: Using the same path for input and output can overwrite or confuse source documents.

Mitigation: Keep separate input and output paths and preserve original DOCX files.

## Reference(s):

- [论文排版规范参考](references/format_rules.md)
- [参考文献交叉引用体系](references/citation_crossref.md)
- [论文排版作战地图](references/作战地图.md)
- [python-docx styles documentation](https://python-docx.readthedocs.io/en/latest/user/styles-understanding.html)
- [python-docx-template documentation](https://docxtpl.readthedocs.io/)
- [Python-Redlines](https://github.com/JSv4/Python-Redlines)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown and JSON reports with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local DOCX files and writes local report files; users should review generated reports before relying on them.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
