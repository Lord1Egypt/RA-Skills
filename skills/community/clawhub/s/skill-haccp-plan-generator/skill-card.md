## Description:

Generates Chinese-language HACCP hazard analysis and critical control point plan tables in a standard 11-column format, with optional Excel export support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Food safety and quality teams use this skill to draft HACCP plans from product and process-flow inputs, including hazard analysis, CCP identification, critical limits, monitoring, corrective actions, verification, and records. Generated plans are drafts that require qualified review before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HACCP plans can be incomplete or unsuitable for a specific facility, product, or regulatory context.

Mitigation: Treat generated HACCP plans as drafts and require review by qualified food safety or quality personnel before use.

Risk: Excel exports from untrusted JSON can carry spreadsheet-safety risks if cell values begin with formula characters.

Mitigation: Avoid exporting or opening workbooks created from untrusted JSON until formula-leading values are sanitized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-haccp-plan-generator)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-haccp-plan-generator)
- [HACCP knowledge reference](references/haccp-knowledge.md)
- [HACCP template guide](references/template-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown tables and optional Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts users for missing product or process-flow inputs and labels defaults or unconfirmed values.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
