## Description:

Generate a four-sheet Excel review summary from Guanglianda export data for budget review projects, with automatic classification into seven review adjustment categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lialia691691-alt](https://clawhub.ai/user/lialia691691-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External budget review teams use this skill to turn Guanglianda export folders into an Excel review package for project budget audit summaries and adjustment detail review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source spreadsheet text may include formulas that remain active in the generated workbook.

Mitigation: Use trusted source spreadsheets and review generated workbooks before sharing or opening in sensitive environments.

Risk: Keyword-based automatic classification can place budget adjustments in the wrong review category.

Mitigation: Review classification results, especially high-value Other entries and material-price items with quota or subitem language, then correct the classification inputs or rerun the workflow.

## Reference(s):

- [Classification Rules](references/classification.md)
- [Template Structure](references/template_structure.md)
- [ClawHub Skill Page](https://clawhub.ai/lialia691691-alt/skills/review-summary)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Excel workbook (.xlsx) plus terminal summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a four-sheet workbook from required Guanglianda export spreadsheets and optional project, company, notes, and building-area arguments.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
