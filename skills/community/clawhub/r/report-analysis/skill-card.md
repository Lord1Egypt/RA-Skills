## Description:

分析渠道/合作伙伴评优激励通报 Excel 数据，诊断业务欠缺与整改重点，并支持销售合作伙伴政策 Word 文档的总结和检索问答。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxx580353-creator](https://clawhub.ai/user/zxx580353-creator)

### License/Terms of Use:

MIT-0

## Use Case:

渠道运营、合作伙伴管理和业务分析人员 use this skill to turn user-provided evaluation incentive spreadsheets into shortfall analysis, grid/channel remediation guidance, warning lists, charts, and reports. They can also use it to summarize and search related sales partner policy documents when those Word files are supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local business Excel files and optional policy Word documents that may contain sensitive operational data.

Mitigation: Run it in an isolated working folder and provide only the specific files needed for the requested analysis.

Risk: Weak path controls and environment-variable reuse can cause reports to be written to unexpected locations or based on a stale source file.

Mitigation: Set explicit input and output paths for each run and verify YJ_SRC, YJ_DOC_DIR, and output variables before executing scripts.

Risk: Generated XLSX exports have an Excel formula-injection risk.

Mitigation: Treat exported spreadsheets carefully and sanitize cells that begin with formula prefixes before sharing or opening them in high-trust environments.

Risk: Dependencies are not pinned in the artifact requirements.

Mitigation: Install dependencies in a dedicated environment and pin reviewed versions before production use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zxx580353-creator/skills/report-analysis)
- [Source skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Chinese Markdown responses plus generated DOCX, XLSX, self-contained HTML, JSON indexes, and chart assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided local Excel and optional Word policy files; outputs are written to configured local paths.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
