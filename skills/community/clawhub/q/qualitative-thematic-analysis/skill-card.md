## Description:

基于 Braun & Clarke 六阶段法，对本地质性资料（访谈、观察、文本）进行系统性主题归纳、编码及报告生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yipng05-max](https://clawhub.ai/user/yipng05-max)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and analysis teams use this skill to conduct AI-assisted thematic analysis of local qualitative materials such as interview transcripts, observation notes, focus group records, and text corpora. It guides the agent through intake questions, coding, theme development, theme review, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive interview or observation data and helper scripts may expose raw content in terminal or agent logs.

Mitigation: Use local files only, de-identify participant data where possible, confirm consent for AI-assisted analysis, and limit retention or sharing of terminal and agent logs.

Risk: Generated XLSX coding tables may contain unsafe spreadsheet cells derived from untrusted source text.

Mitigation: Review and sanitize spreadsheet cell values before opening or sharing exported XLSX files, especially values that begin with formula-triggering characters.

Risk: The DOCX report exporter is identified by security evidence as currently broken.

Mitigation: Treat DOCX export as unavailable until the exporter is fixed and tested; use Markdown or JSON report content as the reviewable intermediate output.

## Reference(s):

- [主题分析方法论详解](references/thematic-analysis-method.md)
- [编码操作指南](references/coding-guide.md)
- [研究伦理提示](references/ethics-note.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown analysis, coding-table data for XLSX export, and report data for DOCX export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local XLSX and DOCX files through helper scripts when dependencies are available.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
