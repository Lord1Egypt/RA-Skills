## Description:

多项目（同批供应商、同一询价口径）报价对比看板生成器，输出中英双语可切换的自包含 HTML 看板和结构一致的 Excel，用于逐项目比较报价、工期、条款、澄清事项和定标建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzhe223-tech](https://clawhub.ai/user/chenzhe223-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, project, and commercial teams use this skill to turn same-scope supplier quotes across multiple subprojects into a bilingual decision dashboard and matching Excel workbook. It supports side-by-side review of quote status, per-project pricing, lead-time thresholds, commercial terms, clarification items, and recommendations that avoid cross-project aggregation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Python scripts run locally and the Excel generator executes the data-layer section copied from gen_board.py.

Mitigation: Review any copied gen_board.py before running gen_excel.py, and run the scripts only in a workspace where local file generation is expected.

Risk: Incorrect quote data, deadlines, or output filenames could lead to misleading procurement decisions.

Mitigation: Verify the configured lead-time deadline, filenames, and the RECON ALL OK output before using generated dashboards or workbooks for decisions.

Risk: The artifact enforces several data-shape assumptions, including supplier order alignment in TERMS and no cross-project total ranking.

Mitigation: Keep supplier order consistent across SUPPLIERS and TERMS, and validate that recommendations remain per-project rather than aggregated across projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenzhe223-tech/skills/quotationalyasize)
- [pitfalls.md](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Self-contained HTML dashboard, Excel workbook, and concise Markdown-oriented operating guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates board.html with Chinese/English switching and board.xlsx with six aligned sheets; Excel generation requires openpyxl and may need Pillow for embedded images.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
