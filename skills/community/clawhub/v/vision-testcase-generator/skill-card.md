## Description:

Generates structured, traceable Excel test cases for machine-vision requirements, grouped by vision module with priority styling, module separators, and coverage statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to turn machine-vision requirements or requirement documents into standardized Excel test cases with requirement traceability, priority markings, and coverage summaries. It is intended for vision testing scenarios such as defect detection, AOI, localization, measurement, OCR, barcode reading, 3D vision, camera parameters, and image quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated test cases may contain incorrect assumptions, incomplete requirement interpretation, or unsuitable acceptance criteria.

Mitigation: Review the generated Excel workbook before importing it into a production test-management system.

Risk: The skill generates local Excel files using Python/openpyxl.

Mitigation: Run it only in an approved workspace and inspect generated files before sharing or using them operationally.

Risk: The source instructions are primarily Chinese-language.

Mitigation: Install and use the skill only when Chinese-language workflow instructions are acceptable for the team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kokxi/skills/vision-testcase-generator)
- [Vision domain knowledge](artifact/references/domain-knowledge.md)
- [Vision test case format specification](artifact/references/format-spec.md)
- [Example machine-vision requirements](artifact/examples/requirements.md)
- [Agent Skills standard](https://agentskills.io)
- [skills-ref validation reference](https://github.com/agentskills/agentskills/tree/main/skills-ref)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance and generated Python/openpyxl commands that produce an Excel workbook (.xlsx) containing test cases and coverage statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and openpyxl for Excel generation; output workbooks include a test case sheet and a coverage statistics sheet.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact frontmatter V1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
